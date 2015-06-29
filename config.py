#default config

class BaseConfig(object):
    DEBUG = True
    SECRET_KEY='I\xa9\x1b\x96Ll\x00\x18i\tf\xde\xab\xa4\xb2bD8\xdbL'
    SQLALCHEMY_DATABASE_URI = 'postgresql://demorole1:password1@localhost/nowwehere'
    CLOUDINARY_URL = 'cloudinary://847864466172127:mE-JAQMj5qYrmZDgYggZqlC3m2w@dkgsqu3ym'


class DevelopmentConfig(object):
    DEBUG=True

class ProductionConfig(object):
    DEBUG=False