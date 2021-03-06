function ScenarioAPI(osc){
	
	// perdiod of which we ask for sensor values over osc
	var eventPollingPeriod = 160;//ms
	var self = this;
	
	// main communication object
	this.osc = osc;
	
	/** Generic commands **/
	
	// console print method
	this.print = function(what){
			console.log("\x1B[32m"+what+"\x1B[39m");
	}
	
	this.setTimeout = function(callback,time){
		return setTimeout(callback,time);
	}
	this.clearTimeout = function(handler){
		clearTimeout(handler);
	}
	this.setInterval = function(callback,time){
		return setInterval(callback,time);
	}
	this.clearInterval = function(handler){
		clearInterval(handler);
	}
	
	/** Raspiomix commands **/
	
	// read a digital value once. callback is called when we receive the value
	this.readDigital = function(channel,callback){
			self.osc.getDigital(channel,callback);
	}

	// write a digital value.
	this.writeDigital = function(channel,value){
			self.osc.writeDigital(channel,value);
	}
	
	// pseudo event listener for digital value. callback is called on every value received
	this.onDigital = function(channel,handler){
			var h = setInterval(function(){
					self.osc.getDigital(channel,handler);		
			},eventPollingPeriod);
	}

	// pseudo event listener for digital value. callback is called on value change
	this.onDigitalChange = function(channel,handler){
			var lastValue = null;
			var h = setInterval(function(){
					self.osc.getDigital(channel,function(val){
							if(val != lastValue && lastValue !== null)
								handler(val);
							lastValue = val;
					});		
			},eventPollingPeriod);
	}	
	
	// read an analog value once. callback is called when we receive the value
	this.readAnalog = function(channel,callback){
			self.osc.getAnalog(channel,callback);
	}
	
	// pseudo event listener for analog value. callback is called on every value received
	this.onAnalog = function(channel,handler){
			var h = setInterval(function(){
					self.osc.getAnalog(channel,handler);		
			},eventPollingPeriod);
	}
	
	/** Arduino - Firmata commands **/

	// pseudo event listener for analog value. callback is called on every value received
	this.fonAnalog = function(pin,handler){
			self.osc.fgetAnalog(pin,handler);
	}
	
	// pseudo event listener for digital value. callback is called on value change
	this.fonDigitalChange = function(pin,handler){
			self.osc.fgetDigital(pin,handler);
	}	
	// write a digital value.
	this.fwriteDigital = function(pin,value){
			self.osc.fwriteDigital(pin,value);
	}
	// write a servo value.
	this.fwriteServo = function(pin,value){
			self.osc.fwriteServo(pin,value);
	}
	// write a PWM value.
	this.fwritePWM = function(pin,value){
			self.osc.fwritePWM(pin,value);
	}
	
	/** Media - Player commands **/
	
	// play a media
	this.playMedia = function(media){
			self.osc.play(media);
	}
	
	// play a media on loop mode
	this.playMediaLoop = function(media){
			self.osc.playloop(media);
	}
	
	// pause a media
	this.pauseMedia = function(){
			self.osc.pause();
	}
	
	//resume a media
	this.resumeMedia = function(){
			self.osc.resume();
	}
	//stop a media
	this.stopMedia = function(){
			self.osc.stop();
	}
	
	/** DMX Commands **/
	
	this.sendDmx = function(channel,value){
			self.osc.sendDmx(channel,value);
	}
	/*this.sendDmxM = function(valueString){
			self.osc.sendDmxM(valueString);
	}*/
	this.sendDmxBlackout = function(){
			self.osc.sendDmxBlackout();
	}

	
}

module.exports = ScenarioAPI;
