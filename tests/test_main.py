import pytest
from argparse import Namespace
from unittest.mock import patch, MagicMock, call
from simpleservice.main import (
    parse_args,
    GunicornApp,
    main,
    EnvType,
    OptsType
)

class TestParseArgs:
    # Существующие тесты остаются без изменений
    ...

class TestGunicornApp:
    def test_load_config(self, monkeypatch):
        app = MagicMock()
        opts: OptsType = {
            "bind": ["[::]:3000"],
            "workers": 2,
            "timeout": 120,
            "unknown_option": "value"  # Должен быть проигнорирован
        }

        # Создаем реальный экземпляр вместо мока
        gapp = GunicornApp(app, opts)

        # Заменяем cfg на мок
        mock_cfg = MagicMock()
        mock_cfg.settings = {
            "bind": object(),
            "workers": object(),
            "timeout": object()
        }
        gapp.cfg = mock_cfg

        # Вызываем метод напрямую
        gapp.load_config()

        # Проверяем вызовы
        expected_calls = [
            call('bind', ["[::]:3000"]),
            call('workers', 2),
            call('timeout', 120)
        ]
        mock_cfg.set.assert_has_calls(expected_calls, any_order=True)
        assert mock_cfg.set.call_count == 3

    def test_load(self):
        app = MagicMock()
        gapp = GunicornApp(app, {})
        assert gapp.load() == app

class TestMain:
    @patch("simpleservice.main.create_app")
    def test_dev_env(self, mock_create_app, monkeypatch):
        # Мокаем sys.exit чтобы предотвратить выход из процесса
        monkeypatch.setattr("sys.exit", lambda x: None)

        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        args = Namespace(
            env=EnvType.DEV,
            port=4000,
            workers=1,
            timeout=30
        )

        main(args)

        mock_app.run.assert_called_once_with("::", port=4000, debug=True)
        mock_app.logger.info.assert_called_with("Start application in debug mode")

    @patch("simpleservice.main.create_app")
    def test_testing_env(self, mock_create_app, monkeypatch):
        monkeypatch.setattr("sys.exit", lambda x: None)

        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        args = Namespace(
            env=EnvType.TESTING,
            port=5000,
            workers=1,
            timeout=30
        )

        main(args)

        mock_app.run.assert_called_once_with("::", port=5000, debug=True)
        mock_app.logger.info.assert_called_with("Start application in debug mode")

    @patch("simpleservice.main.create_app")
    @patch("simpleservice.main.GunicornApp", autospec=True)
    def test_prod_env(self, mock_gapp, mock_create_app, monkeypatch):
        monkeypatch.setattr("sys.exit", lambda x: None)

        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        args = Namespace(
            env=EnvType.PROD,
            port=6000,
            workers=3,
            timeout=90
        )

        main(args)

        # Проверяем создание GunicornApp
        expected_opts: OptsType = {
            "bind": ["[::]:6000"],
            "workers": 3,
            "timeout": 90
        }
        mock_gapp.assert_called_once_with(mock_app, expected_opts)

        # Проверяем вызов run
        mock_gapp.return_value.run.assert_called_once()
        mock_app.logger.info.assert_called_with("Start application in production mode")

    @patch("simpleservice.main.create_app")
    def test_app_args_assignment(self, mock_create_app, monkeypatch):
        monkeypatch.setattr("sys.exit", lambda x: None)

        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        args = Namespace(env=EnvType.DEV, port=3000, workers=1, timeout=30)

        main(args)
        assert mock_app.args == args
