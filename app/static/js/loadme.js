function loadjs(document_, window_, xhr_, file_name, debug) {
  if (!window_.hasOwnProperty('__speedTest__')) {
    window_['__speedTest__'] = {}
  }

  xhr_.open("GET", "j/"+file_name+".js", true);
  xhr_.onload = function(e) {
    var response_time = new Date().getTime() - window_['__speedTest__'][file_name+'_start'];
    console.log(file_name+' request time: '+response_time+' ms');
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
    var load_time = new Date().getTime() - window_['__speedTest__'][file_name+'_start'];
    console.log(file_name+' load time: '+load_time+' ms');

    xhr_.open("GET", "performance/jsload?page="+window_.location.pathname+
        "&m="+file_name+
        "&resp="+Math.round(response_time)+
        "&load="+Math.round(load_time)+"#", true);
    xhr_.send(null);
  }
  xhr_.onerror = function(e) {
    console.log(e);
  }
  window_['__speedTest__'][file_name+'_start'] = new Date().getTime(); // in millisec
  xhr_.send(null);
}
