var index = {
  loadm: function loadm(document_, window_, xhr_, debug) {
    {% include 'js/components/quiet.js' %}
    quiet.loadm(document_, window_, xhr_, debug);
    {% include 'js/components/click.js' %}
    click.loadm(document_, window_, xhr_, debug);
  }
}
