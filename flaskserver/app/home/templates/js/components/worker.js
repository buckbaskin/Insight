var worker = {
  xhr: null,
  add: function add(queue_id) {
    console.log('adding q '+queue_id);
    worker.xhr.open("GET", "/worker/add/"+queue_id, true);
    worker.xhr.onload = function(e) {};
    worker.xhr.send(null);
  },
  remove: function remove(queue_id) {
    console.log('removing q '+queue_id);
    worker.xhr.open("GET", "/worker/rm/"+queue_id, true);
    worker.xhr.onload = function(e) {};
    worker.xhr.send(null);
  },
  loadm: function loadm(window_, xhr_, debug) {
    worker.xhr = xhr_;
    console.log('worker.js: loadm');
    window_.worker = worker;
    console.log('worker? '+window_.worker);
  }
}
