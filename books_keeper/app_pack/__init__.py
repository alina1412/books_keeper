from flask import Flask

# Configure application
# sess = Session()
app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'my secret key'
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

