function loadjs(document_, window_, xhr_, file_name, debug) {
  xhr_.open("GET", "j/"+file_name+".js", true);
  xhr_.onload = function(e) {
    try {
      window_.execScript(xhr_.responseText);
    } catch(err) {
      if (debug) { console.log('execScript had an error'); }
      try {
        if (debug) { console.log('window.eval instead'); }
        window_.eval(xhr_.responseText);
      } catch(err) {
        if (debug) { console.log('all failed...'); }
        return undefined;
      }
    }
    window_[file_name].loadm(document_, window_, new XMLHttpRequest(), debug);
  }
  xhr_.onerror = function(e) {
    console.log(e);
  }
  xhr_.send(null);
}
