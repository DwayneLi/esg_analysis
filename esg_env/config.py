USERNAME = "admin"
PASSWORD = "esglidonghuai123"
HOST = 'esgdb.cqvmsusqrmb3.us-east-2.rds.amazonaws.com'
PORT = '3306'
DATABASE = 'esg_analysis'  #database name
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True


#SQLALCHEMY_DATABASE_URI = ‘mysql+pymysql://admin:esglidonghuai123@esgdb.cqvmsusqrmb3.us-east-2.rds.amazonaws.com:3306/esg_db’