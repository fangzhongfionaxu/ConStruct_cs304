
import bcrypt

passwd1 = 'secret'
hashed = bcrypt.hashpw(passwd1.encode('utf-8'), bcrypt.gensalt())
stored = hashed.decode('utf-8')

print (hashed)
print(stored)

passwd2 = 'secret'

hashed2 = bcrypt.hashpw(passwd2.encode('utf-8'), stored.encode('utf-8'))
hashed2_str = hashed2.decode('utf-8')
print(hashed2_str == stored)
