from DB_connect import app
from flask_bcrypt import Bcrypt
from login_logout import *
from home import *
from subject import *
from news import *
from grades import *
from chat import *
from quiz import *
from edit_profile import *
from lecture import *

# bcrypt = Bcrypt(app)


if __name__ == '__main__':
    app.run(debug=True)
