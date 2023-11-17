import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask

from conf import ApiConfig
from api.routes import api_bp
from db import engine

from flask_swagger_ui import get_swaggerui_blueprint

api_app = Flask(__name__)
api_app.config.from_object(ApiConfig)

engine.init_app(api_app)

swaggerui_blueprint = get_swaggerui_blueprint(
    ApiConfig.SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    ApiConfig.API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Todo application"
    },
)
api_app.register_blueprint(swaggerui_blueprint)
api_app.register_blueprint(api_bp)

if __name__ == "__main__":
    api_app.run(port=5001, host="0.0.0.0")



