from web_app.app import app
from web_app.config.server_config import config as server_config

# === APP ===

app.config.update(server_config)
app.run()