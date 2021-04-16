from cryptography.fernet import Fernet

file=open('key.key', 'rb')
key=file.read()
f=Fernet(key)
file.close()

def encrypt(message):
    return f.encrypt(message.encode()).decode()

def decrypt(message):
    return f.decrypt(message.encode()).decode()