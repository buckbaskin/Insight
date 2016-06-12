function loadjs(document_, xhr_, file_name, debug) {
  xhr_.open("GET", "j/"+file_name+".js", true);
  xhr_.onload = function(e) {
    try {
      window.execScript(xhr_.responseText);
    } catch(err) {
      if (debug) { console.log('execScript had an error'); }
      try {
        if (debug) { console.log('window.eval instead'); }
        window.eval(xhr_.responseText);
      } catch(err) {
        if (debug) { console.log('all failed...'); }
        return undefined;
      }
    }
    loadm(document, window, new XMLHttpRequest(), debug);
  }
  xhr_.send(null);
}
