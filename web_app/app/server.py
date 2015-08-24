from web_app.app import app
from web_app.config import server_config

# === APP ===

app.config.from_object(server_config)
app.run()