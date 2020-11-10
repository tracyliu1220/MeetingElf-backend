import os

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'flask'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
)

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
MEETING_HASH_KEY = os.getenv('MEETING_HASH_KEY').encode() # must align to 8
