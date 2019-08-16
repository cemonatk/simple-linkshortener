class Config():
	SECRET_KEY = ''
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	
def return_db():
	return Config.SQLALCHEMY_DATABASE_URI
