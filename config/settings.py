# Flask Configs
DEBUG = True
SECRET_KEY = 'mysecretkey'
SERVER_NAME = 'localhost:5000'

# Setting posts per page for pagination
POSTS_PER_PAGE = 5

HOST = 'mongodb://localdev:devpassword@ds141264.mlab.com:41264/keep-api'
# MONGODB_HOST = 'mongodb'  # use 'mongodb' if using Docker
# DB = 'keepAPI'
MONGODB_SETTINGS = {
    'host': HOST
}
