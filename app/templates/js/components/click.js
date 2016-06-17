var click = {
  __setup__: function __setup__(window_, document_, screen_, xhr_) {
    var pagePath = window_.location.pathname;

      // information about the size of the user screen. send once
      var screen_x = screen_.height;
      var screen_y = screen_.width;
      // information about window position relative to screen, window size
      var window_x = window_.screenX;
      var window_y = window_.screenY;
      var window_w = window_.innerWidth;
      var window_h = window_.innerHeight;
      mailSetup(pagePath, screen_x, screen_y, window_x, window_y, window_w, window_h);

    function onMouseMove(event) {
      // information about the scroll position and mouse position
      // send every time
      // Send as:
      // Scroll position (x, y from top left of page)
      // Relative mouse position (x, y in visible window)
      // This will allow for rendering of where the user was.
      var window_x = window_.screenX;
      var window_y = window_.screenY;
      var window_w = window_.innerWidth;
      var window_h = window_.innerHeight;
      var docEl = document_.documentElement;
      var scroll_across = (window_.pageXOffset || docEl.scrollLeft) - (docEl.clientLeft || 0);
      var scroll_down = (window_.pageYOffset || docEl.scrollTop) - (docEl.clientRight || 0);

      mailCoords(pagePath, scroll_across, scroll_down, event.clientX, event.clientY, Math.round(event.timeStamp));
    }

    var last_time_sent = 0;
    function mailCoords(page, scroll_x, scroll_y, mouse_x, mouse_y, t) {
      if (t - last_time_sent > .1*1000) {
        last_time_sent = t;
        console.log('page: '+page+' px: '+scroll_x+' py: '+scroll_y+
            ' mx: '+mouse_x+' my: '+mouse_y+' t: '+t);
        xhr_.open("GET", "/click/m?type=move&page="+page+"&sx="+scroll_x+
            "&sy="+scroll_y+"&mx="+mouse_x+"&my="+mouse_y+"&t="+t+"#", true);
        xhr_.send(null);
      }
    }
    function mailSetup(page, screen_x, screen_y, window_x, window_y, window_w, window_h) {
      xhr_.open("GET", "click/l?type=load&page="+page+"&sx="+screen_x+"&sy="+screen_y+"&wx="+window_x+"&wy="+window_y+"&ww="+window_w+"&wh="+window_h"#");
      xhr_.send(null);
    }
    return onMouseMove;
  },

  loadm: function loadm(window_, xhr_, debug) {
    console.log('click.js: loadm');
    onMouseMove = click.__setup__(window_, window_.document, window_.screen, xhr_);
    document_.addEventListener("mousemove", onMouseMove);
  }
}
