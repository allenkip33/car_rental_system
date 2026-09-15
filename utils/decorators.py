from functools import wraps


def login_required(auth_service):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if auth_service.current_user is None:
                print("\nPlease login first.")
                return None

            return function(*args, **kwargs)

        return wrapper

    return decorator


def admin_required(auth_service):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if auth_service.current_user is None:
                print("\nPlease login first.")
                return None

            if auth_service.current_user.role != "Admin":
                print("\nAdmin access required.")
                return None

            return function(*args, **kwargs)

        return wrapper

    return decorator