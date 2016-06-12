function loadjs(document_, xhr_, file_name, debug) {
  if (debug == undefined) {
    console.log('default debug');
    debug = false;
  } else {
    console.log('debug? '+debug);
  }
  xhr_.open("GET", "/static/js/"+file_name+".js", true);
  xhr_.onload = function(e) {
    console.log('got xhr back');
    try {
      window.execScript(xhr_.responseText);
    } catch(err) {
      console.log('execScript had an error');
      try {
        console.log('window.eval instead');
        window.eval(xhr_.responseText);
      } catch(err) {
        console.log('all failed...');
        return undefined;
      }
    }
    loadm(document, window, new XMLHttpRequest(), debug);
  }
  xhr_.send(null);
  console.log('xhr sent;');
}
