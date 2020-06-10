from flask_cors import CORS
from init import app
from AccountAPI import account_api
from ProductAPI import product_api
from init import db

app.register_blueprint(account_api)
app.register_blueprint(product_api)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Run Server
if __name__ == '__main__':
  app.run(debug=True)