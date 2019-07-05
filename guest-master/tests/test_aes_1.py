#!/usr/bin/env.python
# coding=utf-8
from Cryptodome.Cipher import AES
from binascii import b2a_hex , a2b_hex

class PrpCrypt(object):

    def __init__(self , key):
        self.key = 'This in a key123'

    def encryptAES(self, key):
        iv = 'This is an IV456'
        self.obj = AES.new(self.key, AES.MODE_CBC, iv)
        key = self.key
        self.ciphertext = self.obj.encrypt(key)
        return b2a_hex(self.ciphertext)

if __name__ == '__mian__':
    message = PrpCrypt("keys")
    a = message.encryptAES("The answer is keys")
    print("加密：", a)

'''
from Cryptodome.Cipher import AES
obj = AES.new('This is a key123', AES.MODE_CBC,'This is an IV456') 报错 <class 'str'>
key = 'This is a key123'
obj = AES.new(key.encode('utf-8'), AES.MODE_CBC,'This is an IV456') 报错 <class 'str'>
iv = b'This is an IV456'
obj = AES.new(key.encode('utf-8'), AES.MODE_CBC,iv.encode('utf-8'))
message = "The answer is no"
ciphertext = obj.encrypt(message)   报错 <class 'str'>
ciphertext = obj.encrypt(message.encode('utf-8'))
ciphertext
输入结果：b'\xd6\x83\x8dd!VT\x92\xaa`A\x05\xe0\x9b\x8b\xf1'

解密：
obj2 = AES.new(key.encode('utf-8'), AES.MODE_CBC,iv.encode('utf-8'))    如果iv不是bytearray需要转一下
obj2.decrypt(ciphertext)



# TypeError: Object type <class 'str'> cannot be passed to C code 
# 经过Debug发现，是因为传入参数的参数类型存在问题，需要更换为 bytearray
# 以下是总结哪些参数类型需要更换为bytearray《b'This is a key123'》

AES.new(key, AES.MODE_CBC, iv)
key需要变更为key.encode('utf-8')
iv需要变更为iv.encode('utf-8')
如果iv参数就是bytearray《b'This is a key123'》，则不需要更改
encrypt(message)方法内的参数message也要转为bytearray《b'The answer is no'》
ciphertext = obj.encrypt(message.encode('utf-8'))

哪几个方法内的参数需要为bytearray：
1.  AES.new(key, AES.MODE_CBC, iv) 这个方法内的参数必须是bytearray
2.  encrypt(message) 这个方法内的参数必须是bytearray

所有需要转的参数都在加密和解密方法内！！！！！！！！！

views_if_sec.py接口里解密的方法不是bytearray还是需要转，这里很容易出错，即使用例里都对了，解密的方法也会导致报错
AES.new(key.encode, AES.MODE_CBC, iv)   报错 <class 'str'>
AES.new(key.encode('utf-8'), AES.MODE_CBC, iv) 方法内的参数key和iv不是bytearray注意一定需要用.encode('utf-8')转一下

'''