import logging
import unittest
from unittest.mock import MagicMock, patch
from opencensus.trace.span import SpanKind
from opencensus.trace.tracer import Tracer

from src.app_insights_logger import AppInsightsLogger


class RealAppInsightsLogger(AppInsightsLogger):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.env = MockEnv("")
        self.tracer = Tracer()


class MockRun:
    def __init__(self, run_id):
        self.id = run_id
        self.parent = MagicMock()
        self.name = run_id
        self.experiment = MagicMock()


class MockEnv:
    def __init__(self, run_id):
        self.build_id = run_id


class MockSpan:
    def __init__(self, name):
        self.span_kind = None
        self.attributes = {}


class TestObservability(unittest.TestCase):
    @patch("src.app_insights_logger.AppInsightsLogger")
    def setUp(self, mock_app_insights_logger):
        self.concert_app_insights_logger = RealAppInsightsLogger()
        self.mock_app_insights_logger = mock_app_insights_logger

    def test_get_run_id_having_online_context(self):
        expected = "FOO"

        response = self.concert_app_insights_logger.\
            get_run_id_and_set_context(MockRun("FOO"))

        self.assertEqual(expected, response)

    def test_get_run_id_having_online_context_using_build_id(self):
        self.concert_app_insights_logger.env.build_id = expected = "FOO"

        response = self.concert_app_insights_logger.\
            get_run_id_and_set_context(MockRun("OfflineRun"))

        self.assertEqual(expected, response)

    def test_get_run_id_having_online_context_using_uuid(self):
        self.concert_app_insights_logger.env.build_id = ""

        response = self.concert_app_insights_logger.\
            get_run_id_and_set_context(MockRun("OfflineRun"))

        self.assertIsNotNone(response)

    def test_log_called_with_parameters(self):
        self.mock_app_insights_logger.log("FOO", "BAZ")

        self.mock_app_insights_logger.log.assert_called_with("FOO", "BAZ")

    def test_log_metric_called_with_parameters(self):
        self.mock_app_insights_logger.log_metric("FOO", "BAZ", "BAR", False)

        self.mock_app_insights_logger.log_metric.assert_called_with(
            "FOO", "BAZ", "BAR", False
        )

    def test_exception_called_with_parameters(self):
        self.mock_app_insights_logger.exception("FOO")

        self.mock_app_insights_logger.exception.assert_called_with("FOO")

    def test_set_view_is_called_with_parameters(self):
        self.mock_app_insights_logger.set_view("FOO", "BAR", "BAZ")
        self.mock_app_insights_logger.set_view.\
            assert_called_with("FOO", "BAR", "BAZ")

    @patch.object(Tracer, "start_span")
    def test_start_span_having_online_context(self, mock_tracer):
        name = "foo"
        mock_tracer.return_value = MockSpan(name)
        test_span = self.concert_app_insights_logger.start_span(name)
        mock_tracer.assert_called_with(name)
        self.assertEqual(test_span.span_kind, SpanKind.SERVER)
        self.assertEqual(test_span.attributes['http.method'], 'START')
        self.assertEqual(test_span.attributes['http.route'], name)


if __name__ == "__main__":
    unittest.main()