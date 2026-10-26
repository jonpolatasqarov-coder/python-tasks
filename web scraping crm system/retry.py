
import time
from functools import wraps

import requests


class NotFoundError(Exception):
    pass


def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for attempt in range(3):
            try:
                return func(*args, **kwargs)

            except NotFoundError:
                raise

            except requests.HTTPError as error:
                if (
                    error.response is not None
                    and error.response.status_code == 404
                ):
                    raise NotFoundError(
                        "Page not found"
                    ) from error

                if attempt == 2:
                    raise

                print(f"Retry {attempt + 1}/2...")
                time.sleep(1)

            except requests.RequestException:
                if attempt == 2:
                    raise

                print(f"Retry {attempt + 1}/2...")
                time.sleep(1)

    return wrapper
