from py2neo import Graph
graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="123456"
)


SECRET_KEY = "asdfasdfjasdfjasd;lf"

# 数据库的配置信息
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'cbr'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI



# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "1530003469@qq.com"
MAIL_PASSWORD = "rbrdokdevbwzfecd"
MAIL_DEFAULT_SENDER = "1530003469@qq.com"