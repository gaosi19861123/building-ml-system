import random
import string
import uuid


def get_uuid() -> str:
    return str(uuid.uuid4()).replace("-", "")
