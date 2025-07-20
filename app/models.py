from .db import get_db

# create new user 
def create_user(username,email,password):
    db = get_db()
    try:
        # check if the email already exists
        isEmail = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if isEmail:
            return{
                'success': False,
                'message': "Email already exists"
            }
        # check if the username already exists
        isUsername = db.execute('select * from users where username = ?', (username,)).fetchone()
        if isUsername:
            return {
                'success': False,
                'message' : "Username already exists"
            }
        db.execute('INSERT INTO users (username, email, password) VALUES (? , ? , ?)',
                (username, email, password))
        db.commit()
        return {
            'success': True,
            'message' : "User created successfully"
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'error creating user: {str(e)}'
        }
    

def login_user(email, password):
    db = get_db()
    try:
        user = db.execute('select * from users where email = ? and password = ?',
                          (email,password)).fetchone()
        if not user:
            return {
                'success': False,
                'message': "Invalid Email or Password"
            }
        return {
            'success': True,
            'message': "Login successful",
            'user' : dict(user)
        }
    except Exception as e:
        return {
            'success' : False,
            'message': f'Error logging in user: {str(e)}'
        }