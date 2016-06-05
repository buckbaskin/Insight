function getCoords(event) {
  mailCoords(window.location.pathname, event.clientX, event.clientY, Math.round(event.timeStamp));
}

var last_time_sent = null;
function mailCoords(page, x, y, t) {
  if (t - last_time_sent > .1*1000) {
    last_time_sent = t;
    console.log('page: '+page+' x: '+x+' y: '+y+' t: '+t);
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "/click?type=move&page="+page+"&x="+x+"&y="+y+"&t="+t+"#", true);
    xmlHttp.send(null);
  }
}
