import base64
import uuid
import getpass
import nacl.utils
import nfc
import nfc.snep
import ndef

from nacl.public import PrivateKey, Box

uid = str(uuid.uuid4())
passphrase = getpass.getpass('Passphrase: ')

print('Generating keypair')

prv = PrivateKey.generate()
pub = prv.public_key
box = Box(prv, pub)

print('Encrypting')

encrypted = box.encrypt(passphrase.encode())

print('Storing key')

with open('./keys/%s.pub' % uid, 'wb') as writer:
    writer.write(bytearray(pub.encode()))

with open('./keys/%s.key' % uid, 'wb') as writer:
    writer.write(bytearray(encrypted))

print('Disposing unnecessary data')

del passphrase
del pub

print('Waiting for NFC tag')

clf = nfc.ContactlessFrontend('usb')
tag = clf.connect(rdwr={'on-connect': lambda tag: False})

print('Writing')

uid_record = ndef.TextRecord(uid)
uid_record.name = 'touchkey:uid'

prv_record = ndef.TextRecord(base64.b64encode(prv.encode()))
prv_record.name = 'touchkey:prv'

tag.ndef.records = [uid_record, prv_record]

print('Cleaning up')

del uid_record
del prv_record
del prv
del uid

print('All done!')
