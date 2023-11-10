import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-gue55'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API = "http://localhost:8081/api"
    # swagger
    SWAGGER_URL = "/api/docs"
    API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)