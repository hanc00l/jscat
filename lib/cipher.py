#!/usr/bin/env python3
# coding:utf-8


class ARC4(object):
    def __init__(self):
        pass

    '''
    RC4加密：text和key的type为 byte
    '''
    @classmethod
    def encrypt(cls, text, key):
        s = [0] * 256
        for i in range(256):
            s[i] = i
        j = 0
        for i in range(256):
            j = (j + s[i] + key[i % len(key)]) % 256
            s[i], s[j] = s[j], s[i]
        i = 0
        j = 0
        res = []
        for c in text:
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            s[i], s[j] = s[j], s[i]
            res.append(bytes([c ^ s[(s[i] + s[j]) % 256]]))
        return b''.join(res)

    '''
    RC4解密：text和key的type为 str
    '''
    @classmethod
    def decrypt(cls, text, key):
        s = []
        j = 0
        res = ''

        for i in range(256):
            s.append(i)
        for i in range(256):
            j = (j + s[i] + ord(key[i % len(key)])) % 256
            s[i], s[j] = s[j], s[i]

        i = j = 0
        for x in range(len(text)):
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            s[i], s[j] = s[j], s[i]

            res += chr(ord(text[x]) ^ s[(s[i] + s[j]) % 256])
        return res


if __name__ == '__main__':
    data = '使用RC4 cipher进行加解密测试'
    key = b'deadbeaf'

    print(data)

    x = ARC4().encrypt(data.encode(), key)
    y = ARC4().encrypt(x, key)

    print(y.decode())

    data = '使用RC4 cipher进行加解密测试'
    key = 'deadbeaf'
    x = ARC4().decrypt(data, key)
    y = ARC4().decrypt(x, key)

    print(y)
