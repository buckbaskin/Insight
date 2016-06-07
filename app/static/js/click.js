function c(window_, xhr_, debug) {
  console.log('loading click');
  if (debug == undefined || !(debug)) {
    console.log('replacing console.');
    console = {
      'log': function(toOutput) {}
    };
    console.log('no console output');
  }

  function onMouseMove(event) {
    mailCoords(window_.location.pathname, event.clientX, event.clientY, Math.round(event.timeStamp));
  }

  var last_time_sent = 0;
  function mailCoords(page, x, y, t) {
    if (t - last_time_sent > .1*1000) {
      last_time_sent = t;
      if (debug)
        console.log('page: '+page+' x: '+x+' y: '+y+' t: '+t);
      xhr_.open("GET", "/click?type=move&page="+page+"&x="+x+"&y="+y+"&t="+t+"#", true);
      xhr_.send(null);
    }
  }
  console.log('run setup.');
  return onMouseMove;
}

