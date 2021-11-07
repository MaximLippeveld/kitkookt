from .base import *
import os

ALLOWED_HOSTS = ["0.0.0.0", "kitkookt.be", "localhost"]
DEBUG = False if "DEBUG" not in os.environ else True
