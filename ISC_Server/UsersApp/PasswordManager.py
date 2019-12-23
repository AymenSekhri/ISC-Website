import bcrypt
import base64

WORKING_FACTOR = 10
class PasswordManager(object):

    def hashPassword(password,work = WORKING_FACTOR):
        myHash = bcrypt.gensalt(work)
        encoded_pass = bytes(password, 'utf-8')
        hashedPassBytes = bcrypt.hashpw(encoded_pass,myHash)
        return str(base64.b64encode(hashedPassBytes),'utf-8')

    def chekPassword(password,hashedPassword):
        decoded_hashed_pass = base64.b64decode(hashedPassword)
        encoded_pass = bytes(password, 'utf-8')
        return bcrypt.checkpw(encoded_pass,decoded_hashed_pass)