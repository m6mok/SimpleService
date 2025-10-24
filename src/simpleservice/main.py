from argparse import ArgumentParser, Namespace as ArgsNamespace
from enum import Enum

from gunicorn.app.base import BaseApplication

from simpleservice.app import create_app


class EnvType(Enum):
    DEV = "DEV"
    TESTING = "TESTING"
    PROD = "PROD"


class GunicornApp(BaseApplication):
    def __init__(self, app, opts):
        self._app = app
        self._opts = opts
        super(GunicornApp, self).__init__()

    def load_config(self):
        for k, v in self._opts.items():
            if k in self.cfg.settings and v is not None:
                self.cfg.set(k.lower(), v)

    def load(self):
        return self._app


def parse_args() -> ArgsNamespace:
    parser = ArgumentParser()

    parser.add_argument(
        "--port",
        type=int,
        default=3000,
        help="Port to listen, default: %(default)s"
    )
    parser.add_argument(
        "--env",
        type=EnvType,
        choices=tuple(EnvType),
        default=EnvType.PROD,
        help="What env to run",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=2,
        help="Number of workers (should be n_cores * 2 + 1)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="requests timeout"
    )

    namespace, unknown_args = parser.parse_known_args()
    if len(unknown_args) > 0:
        _args = ", ".join(unknown_args)
        raise ValueError(f"Unknown args are not accepted: {_args}")

    return namespace


def main(args: ArgsNamespace) -> None:
    app = create_app()
    app.args = args
    if app.args.env != EnvType.PROD:
        app.logger.info("Start application in debug mode")
        app.run("::", port=app.args.port, debug=True)
        return

    app.logger.info("Start application in production mode")

    opts = dict(
        bind=["{host}:{port}".format(host="[::]", port=app.args.port)],
        workers=app.args.workers,
        timeout=app.args.timeout,
    )

    gunicorn_app = GunicornApp(app, opts)
    gunicorn_app.run()


if __name__ == "__main__":
    main(parse_args())
