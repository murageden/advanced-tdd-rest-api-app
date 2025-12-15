from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

def hash(password):
    return pwd_context.hash(password)

def verify(password, hashed_password):
    try:
        return pwd_context.verify(password, hashed_password)
    except:
        return False