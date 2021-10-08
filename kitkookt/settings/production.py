from .base import *
import os

ALLOWED_HOSTS = ["0.0.0.0", "kitkookt.be", "localhost"]
SECRET_KEY = "_%!)ka%-khg!ckm6o$%2(0zcsn$@th%@gnm!q**@ozaq5*&((e"
DEBUG = False if "DEBUG" not in os.environ else os.environ["DEBUG"] == "TRUE"
