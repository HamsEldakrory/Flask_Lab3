import os
class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    Debug = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
class Developmentconfig(BaseConfig):
    SECRET_KEY="LOCAL_SECRET_KEY"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'

class ProductionConfig(BaseConfig):
    DEBUG=False

config = {
    'development': Developmentconfig,
    'production': ProductionConfig,
}