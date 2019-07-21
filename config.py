import os

# Base Config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = "\xc6\xd3T\x94%\xc7%\xc8\xd7klA\xf5\xcb\x19\x0bt\xce\xf6_X"
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class DevConfig(BaseConfig):
    DEBUG = True

class ProdConfig(BaseConfig):
    DEBUG = False
