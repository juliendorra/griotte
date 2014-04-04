#
# (c) 2013-2014 ERASME
#
# This file is part of griotte
#
# griotte is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# griotte is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with griotte. If not, see <http://www.gnu.org/licenses/>.

import json
import socket
import time
import logging

import fnmatch

import threading
import websocket

from tornado.options import options
from copy import deepcopy

from griotte.config import Config

class WebSocket:
    """ WebSocket client """

    def __init__(self,
                 uri=None,
                 watchdog_interval=5):

        self.callbacks = dict()

        # So caller doesn't have to check if URI is set or not when it's received as an argument
        if not uri:
            uri = "ws://%s:%s/ws" % (options.default_server, options.default_port)

        self._uri = uri
        self._ws_ready = False

        logging.info("Using server at %s" % uri)
        self.ws = websocket.WebSocketApp(uri,
                                         on_open = self.on_open,
                                         on_message = self.on_message,
                                         on_error = self.on_error,
                                         on_close = self.on_close)

        self.ws.on_open = self.on_open
        self.watchdog_interval = watchdog_interval
        self.websocket_thread = None


    def start(self, detach=True):
        logging.info("Starting websocket watchdog thread with interval %ss" % self.watchdog_interval)
        self.watchdog_thread = threading.Thread(target=self._watchdog, args=(detach,))
        self.watchdog_thread.start()


    def stop(self):
        self.watchdog_interval=0
        logging.info("Closing websocket")
        if self._ws_ready:
            self.ws.close()

    def is_ready(self):
        return self._ws_ready

    def add_listener(self, channel, callback, *args):
        """ Adds a listener to a specific or wildcard channel

        :param channel: Channel to watch
        :param callback: Callback method
        :param args: Callback additionnal arguments
        :type args: array

        .. note:: There can be only one listener on a specific channel
        """

        logging.debug("Adding callback for channel %s", channel)
        self.callbacks[channel] = callback
        # We rely on the fact the server uses a per-channel set with subscribers
        # We can thus safely subscribe to the same channel several times

        # If the thread is running, we can subscribe immediately
        # It doesn't matter if the websocket is not ready
        # When it will be, subscriptions will be resent
        if self._ws_ready:
            logging.debug("Websocket is ready, sending subscription")
            self._subscribe(channel)

    def remove_listener(self, channel):
        logging.debug("Removing callback for channel %s", channel)
        self._unsubscribe(channel)
        self.callbacks.pop(channel)

    def send(self, channel, message):
        """ Send a message in a channel over a websocket

        :param
        """
        if type(message) == str:
            message = json.loads(message)

        data = json.dumps( { 'channel': channel,
                             'timestamp': time.time(),
                             'data': message } )

        while not self._ws_ready:
            logging.info("Websocket not ready, waiting...")
            time.sleep(0.1)

        self.ws.send(data)

    def on_open(self, ws):
        logging.info("Websocket opened")
        # Subscribe (or re-subscribe) to requested channels
        self._ws_ready = True
        for channel in self.callbacks.keys():
            self._subscribe(channel)

    def on_message(self, ws, message):
        """ Decodes incoming message and dispatches to local callback """
        logging.debug("Received : %s" % message)
        decoded = json.loads(message)

        # We have to check the wildcards
        message_channel = decoded['channel']

        # Clients can watch wildcard channels
        for watched_channel in self.callbacks.keys():
            if fnmatch.fnmatch(message_channel, watched_channel):
                # We had a match for watched_channel key
                logging.debug("Dispatching message for channel %s" % message_channel)
                self.callbacks[watched_channel](decoded['channel'], decoded['data'])

    def on_error(self, ws, error):
        logging.error("Websocket error : %s" % error)

    def on_close(self, ws):
        logging.warning("websocket closed")
        self._ws_ready = False

    def _start_websocket(self, detach):
        logging.info("Starting websocket client thread with detach = %s" % detach)
        self.websocket_thread = threading.Thread(target=self.ws.run_forever, args=())
        self.websocket_thread.daemon = detach
        self.websocket_thread.start()

    def _watchdog(self, detach_websocket=False):
        while self.watchdog_interval > 0:
            if not self.websocket_thread:
                logging.info("No websocket thread, starting")
                self._start_websocket(detach_websocket)
            elif not self.websocket_thread.is_alive():
                logging.warning("Websocket thread is dead, restarting")
                self._start_websocket(detach_websocket)

            time.sleep(self.watchdog_interval)

    def _subscribe(self, channel):
        logging.debug("Sending subscribe for channel %s" % channel)
        self.send('meta.subscribe', { 'channel': channel })

    def _unsubscribe(self, channel):
        logging.debug("Sending unsubscribe for channel %s" % channel)
        self.send('meta.unsubscribe', { 'channel': channel })
