from .base import *
import os

ALLOWED_HOSTS = ["0.0.0.0", "kitkookt.be"]
SECRET_KEY = "_%!)ka%-khg!ckm6o$%2(0zcsn$@th%@gnm!q**@ozaq5*&((e"
DEBUG = os.environ["DEBUG"] == "TRUE"
