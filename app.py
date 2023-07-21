from flask_smorest import Api
from flask import Flask, jsonify
from resources.vehicle import blp as VehicleBluePrint

def create_app():
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Tasks Management"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"

    api = Api(app)

    api.register_blueprint(VehicleBluePrint)


    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
