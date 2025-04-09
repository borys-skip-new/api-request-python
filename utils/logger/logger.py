import logging
import os

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "api_requests.log")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("API Logger")

def log_request(method: str, url: str, payload: dict = None):
    """
    Logs the details of an API request.

    Args:
        method (str): The HTTP method (e.g., GET, POST, PUT, DELETE).
        url (str): The URL of the request.
        payload (dict, optional): The request payload. Defaults to None.
    """
    log.info(f"Request: {method} {url}")
    if payload:
        log.info(f"Payload: {payload}")

def log_response(response):
    """
    Logs the details of an API response.

    Args:
        response (requests.Response): The response object.
    """
    log.info(f"Response: {response.status_code} {response.url}")
    log.info(f"Response Body: {response.text}")

