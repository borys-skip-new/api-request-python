import pytest
from utils.logger.logger import log

class BaseTest:
    test_name = None
    def setup_method(self, method, caplog, request):
        """
        Automatically sets up logging for each test method.

        Args:
            method: The test method being executed.
            caplog: The pytest caplog fixture for capturing logs.
            request: The pytest request fixture for accessing test metadata.
        """
        self.caplog = caplog
        self.request = request
        marker = request.node.get_closest_marker("step")
        self.test_name = marker.args[0] if marker and marker.args else method.__name__

        with caplog.at_level("INFO"):
            log.info(f"Starting {self.test_name}")