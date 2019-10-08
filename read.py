import base64
import nacl.utils
import nfc
import nfc.snep
import ndef
import serial

from nacl.public import PublicKey, PrivateKey, Box

print('Waiting for NFC tag')

clf = nfc.ContactlessFrontend('usb')
tag = clf.connect(rdwr={'on-connect': lambda tag: False})

print('Reading')

uid = None
prv = None

for record in tag.ndef.records:
    if (record.name == 'touchkey:uid'):
        uid = record.text
    elif (record.name == 'touchkey:prv'):
        prv = PrivateKey(base64.b64decode(record.text))

if (uid == None or prv == None):
    print('Error: Invalid tag')
    exit()

print('Key ID: %s' %uid)
print('Loading key')

with open('./keys/%s.pub' %uid, 'rb') as reader:
    pub = PublicKey(reader.read())

with open('./keys/%s.key' %uid, 'rb') as reader:
    key = reader.read()

box = Box(prv, pub)

print('Decrypting')

plain = box.decrypt(key)

print('Sending to Arduino')

connection = serial.Serial('/dev/ttyS0', 9600)
connection.write(('%s\n' %(plain.decode())).encode())
connection.close()

print('All done!')

