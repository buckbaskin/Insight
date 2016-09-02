var main = {
  loadm: function loadm(window_, xhr_, debug) {
    {% include 'js/components/quiet.js' %}
    quiet.loadm(window_, xhr_, debug);
    {% include 'js/components/click.js' %}
    click.loadm(window_, xhr_, debug);
  }
}
