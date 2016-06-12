function __setup__(window_, xhr_) {
  function onMouseMove(event) {
    mailCoords(window_.location.pathname, event.clientX, event.clientY, Math.round(event.timeStamp));
  }

  var last_time_sent = 0;
  function mailCoords(page, x, y, t) {
    if (t - last_time_sent > .1*1000) {
      last_time_sent = t;
      console.log('page: '+page+' x: '+x+' y: '+y+' t: '+t);
      xhr_.open("GET", "/click?type=move&page="+page+"&x="+x+"&y="+y+"&t="+t+"#", true);
      xhr_.send(null);
    }
  }
  return onMouseMove;
}

function loadm(document_, window_, xhr_, debug) {
  onMouseMove = __setup__(window_, xhr_);
  console.log('loading click');
  if (debug == undefined || !(debug)) {
    console.log('replacing console.');
    console = {
      'log': function(toOutput) {}
    };
    console.log('no console output');
  }

  console.log('run setup.');
  document_.addEventListener("mousemove", onMouseMove);
}


