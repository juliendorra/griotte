'use strict';

goog.provide('Blockly.Python.dmx');
goog.require('Blockly.Python');

Blockly.Python['dmx_send_single'] = function(block) {
  Blockly.Python.definitions_['from_griotte_scenario_dmx_send_single'] = 'from griotte.scenario.dmx import dmx_send_single';

  var value = Blockly.Python.quote_(block.getTitleValue('VALUE'));
  var channel = Blockly.Python.quote_(block.getTitleValue('CHANNEL'));
  var code = 'dmx_send_single(' + channel + ', ' + value + ')\n'

  return code;
};



