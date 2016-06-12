var quiet = {
  loadm: function loadm(document_, window_, xhr_, debug) {
    console.log('quiet.js: loadm');
    if (debug == undefined || !(debug)) {
      console.log('quiet.js: silencing console.');
      console = {
        'log': function(toOutput) {}
      };
      console.log('no console output');
    }
  }
}
