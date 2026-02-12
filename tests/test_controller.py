from unittest import TestCase, mock

from controller import Controller


class ControllerTestCase(TestCase):
    def setUp(self):
        self.mock_session = mock.patch('controller.session', mock.MagicMock())
        self.mock_db_name = mock.patch('controller.DB_FILENAME', 'test.db')
        self.mock_view = mock.patch('controller.View', mock.MagicMock())
        self.mock_session.start()
        self.mock_db_name.start()
        self.mock_view.start()

        self.controller = Controller()

    def tearDown(self):
        self.mock_session.stop()
        self.mock_db_name.stop()
        self.mock_view.stop()

    def test_current_time_cat_value(self):
        from datetime import datetime
        with mock.patch('controller.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 2, 12, 0, 4)
            self.controller.set_cat_value = mock.MagicMock()

            self.controller.current_time_cat_value(1)

            args, _ = self.controller.set_cat_value.call_args
            passed_time = args[2]

            self.assertEqual(passed_time, "0:04")
