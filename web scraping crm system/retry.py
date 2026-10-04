class NotFoundError(Exception):
    pass


def retry(func):

    def wrapper(*args, **kwargs):
        last_error = None

        for attempt in range(3):
            try:
                return func(*args, **kwargs)

            except NotFoundError as error:
                last_error = error

                print(
                    f"Attempt {attempt + 1} failed: {error}"
                )

        raise last_error

    return wrapper