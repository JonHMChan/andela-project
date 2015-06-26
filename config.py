#default config

class BaseConfig(object):
    DEBUG = True
    SECRET_KEY='its a secret nope a code'
    SQLALCHEMY_DATABASE_URI = 'postgresql://demorole1:password1@localhost/nowwehere'

class DevelopmentConfig(object):
    DEBUG=True

class ProductionConfig(object):
    DEBUG=False