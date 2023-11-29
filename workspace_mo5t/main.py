from login_logout import *
from home import *


bcrypt = Bcrypt(app)


if __name__ == '__main__':
    app.run(debug=True)
