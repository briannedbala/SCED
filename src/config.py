class DevelopmentConfig():
    DEBUG = True
    SECRET_KEY = 'Blqtv6jyHp'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'departamento_maipu'


config = {
    'development': DevelopmentConfig
}
