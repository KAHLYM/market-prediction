import os


def is_gcp_instance() -> bool:
    for env in os.environ:
        if "X_GOOGLE" in env:
            return True

    return False
