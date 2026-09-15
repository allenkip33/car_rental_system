from functools import wraps


def login_required(function):
    # Check that a user is logged in
    @wraps(function)
    def wrapper(auth_service, *args, **kwargs):
        if auth_service.current_user is None:
            print("Please login first.")
            return None

        return function(auth_service, *args, **kwargs)

    return wrapper
