import os

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'flask'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
)

# SECRET_KEY = os.getenv('SECRET_KEY', 'secret')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_MEETING_HASH_KEY = os.getenv('JWT_MEETING_HASH_KEY')
