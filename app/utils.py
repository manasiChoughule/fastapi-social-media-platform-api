from passlib.context import CryptContext

#encrypt user password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = 'auto')

def hash(password : str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    '''
        function checks if the user provided password is equal to the hashed password stored in the database.
        input:
            plain_password: user provided password at the time of login
            hashed_password : password from User table 
        output : 
            boolean value
    '''
    return pwd_context.verify(plain_password, hashed_password)