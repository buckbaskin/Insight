var click = {
  __setup__: function __setup__(window_, xhr_) {
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
  },

  loadm: function loadm(document_, window_, xhr_, debug) {
    console.log('click.js: loadm');
    onMouseMove = click.__setup__(window_, xhr_);
    document_.addEventListener("mousemove", onMouseMove);
  }
}
