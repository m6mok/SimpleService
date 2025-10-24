from traceback import format_exc as traceback_format_exc

from flask import Flask, request, Response, make_response

from simpleservice.app.handlers import add_routes


WHITELIST_ORIGIN = ("http://localhost:3000",)


def create_app():
    app = Flask(__name__)
    app.logger.info("app enabled")
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    add_routes(app)
    app.logger.info("routes added")

    @app.after_request
    def set_default_headers(response: Response) -> Response:
        if (
            origin := request.headers.get("Origin")
        ) is not None and origin in WHITELIST_ORIGIN:
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Access-Control-Expose-Headers"] = "*"
            response.headers["Access-Control-Allow-Methods"] = (
                "GET, POST, PUT, DELETE, OPTIONS"
            )
        return response

    @app.errorhandler(Exception)
    def handle_exception(e: Exception) -> Response:
        app.logger.error(
            "".join(
                (
                    f"Error handling request '{request.url}':\n",
                    traceback_format_exc()
                )
            )
        )
        return make_response(
            {"code": 500, "name": type(e).__name__, "description": str(e)},
            500
        )

    @app.route("/ping")
    def ping() -> Response:
        return make_response("OK")

    return app
