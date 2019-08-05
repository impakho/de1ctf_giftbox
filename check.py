#!/usr/bin/python2
#coding:utf-8

from sys import *
from base64 import *
import requests
import urllib
import os
import pyotp

timeout = 1.0
retry_count = 5

shell_url = '/shell.php?a=%s&totp=%s'
totp = pyotp.TOTP("GAXG24JTMZXGKZBU", digits=8, interval=5)
preset_password = 'aGludHtHMXZlX3VfaGkzM2VuX0MwbW0zbmQtc2gwd19oaWlpbnR0dHRfMjMzMzN9'
s = requests.session()


# get method
def get(session, url):
    retry = 0
    while True:
        retry += 1
        try:
            if session:
                r = s.get(url, timeout=timeout)
            else:
                r = requests.get(url, timeout=timeout)
        except:
            if retry >= retry_count:
                return ''
            continue
        break
    return r.text


# post method
def post(session, url, data):
    retry = 0
    while True:
        retry += 1
        try:
            if session:
                r = s.post(url, data=data, timeout=timeout)
            else:
                r = requests.post(url, data=data, timeout=timeout)
        except:
            if retry >= retry_count:
                return ''
            continue
        break
    return r.text


# send command
def send(session, url, command, data=''):
    url = url + shell_url
    payload = urllib.quote(command)
    payload = url % (payload, totp.now())
    if data == '':
        res = get(session, payload)
    else:
        res = post(session, payload, data)
    return res


# check index
def check1(url):
    try:
        url = url + '/'
        res = get(0, url)
        passed = 1
        if 'input-text' not in res: passed = 0
        if 'yin' not in res: passed = 0
        if 'tlt' not in res: passed = 0
        if 'bgm' not in res: passed = 0
        if 'de1ta' not in res: passed = 0
        if 'totp' not in res: passed = 0
        if 'main' not in res: passed = 0
        if 'console' not in res: passed = 0
        if not passed:
            raise Exception
    except Exception as e:
        raise Exception, "Check1 error, index page is not complete."
    return True


# check main.js
def check2(url):
    try:
        url = url + '/js/main.js'
        res = get(0, url)
        passed = 1
        if 'de1ta' not in res: passed = 0
        if 'sandbox' not in res: passed = 0
        if 'pyotp' not in res: passed = 0
        if 'digits' not in res: passed = 0
        if 'interval' not in res: passed = 0
        if 'window' not in res: passed = 0
        if 'ajax' not in res: passed = 0
        if 'message' not in res: passed = 0
        if 'data' not in res: passed = 0
        if not passed:
            raise Exception
    except Exception as e:
        raise Exception, "Check2 error, main.js is not complete."
    return True


# check totp.min.js
def check3(url):
    try:
        url = url + '/js/totp.min.js'
        res = get(0, url)
        passed = 1
        if 'SHA-1' not in res: passed = 0
        if 'genOTP' not in res: passed = 0
        if ']:5' not in res: passed = 0
        if 'BYTES' not in res: passed = 0
        if 'TEXT' not in res: passed = 0
        if 'HOTP' not in res: passed = 0
        if 'TOTP' not in res: passed = 0
        if not passed:
            raise Exception
    except Exception as e:
        raise Exception, "Check3 error, totp.min.js is not complete."
    return True


# check common commands
def check4(url):
    try:
        res = send(0, url, 'ls')
        passed = 1
        if 'missiles' not in res: passed = 0
        if 'modules' not in res: passed = 0
        if 'usage.md' not in res: passed = 0
        if not passed:
            raise Exception, "`ls` not work"
        res = send(0, url, 'cat', {'filename':'usage.md'})
        if 'Nuclear' not in res: raise Exception, "`cat` not work."
        res = send(0, url, 'logout')
        if 'logout' not in res: raise Exception, "`logout` not work."
        res = send(0, url, 'sh0w_hiiintttt_23333')
        if 'eval' not in res: raise Exception, "`hint` not work."
        res = send(0, url, 'getflag')
        if 'flag{' not in res: raise Exception, "`getflag` not work."
    except Exception as e:
        raise Exception, "Check4 error, %s" % e
    return True


# check login
def check5(url):
    try:
        username = 'admin'
        try:
            password = b64decode(preset_password)
        except:
            password = ''
        command = 'login %s %s' % (username, password)
        res = send(1, url, command)
        if 'succ' not in res:
            raise Exception
    except Exception as e:
        raise Exception, "Check5 error, login failed."
    return True


# check destruct
def check6(url):
    try:
        res = send(1, url, 'destruct')
        if 'destructed' not in res:
            raise Exception
    except Exception as e:
        raise Exception, "Check6 error, destruct failed."
    return True


# check targeting and launch
def check7(url):
    try:
        rands = []
        for i in range(5):
            rands.append(os.urandom(4).encode('hex'))
            res = send(1, url, 'targeting z%d %s' % (i, rands[-1]))
            if 'marked' not in res: raise Exception, "targeting failed."
        res = send(1, url, 'launch')
        for i in range(5):
            if res.count(rands[i]) < 2: raise Exception, "launch failed."
    except Exception as e:
        raise Exception, "Check7 error, %s" % e
    return True


# checker
def checker(host, port):
    try:
        url = "http://" + ip + ":" + str(port)
        if check1(url) and check2(url) and check3(url) and check4(url) and check5(url) and check6(url) and check7(url):
            return "IP: " + host + " OK"
    except Exception as e:
        return "IP: " + host + " is down.\n" + str(e)


if __name__ == '__main__':
    if len(argv) != 3:
        print("wrong params.")
        print("example: python %s %s %s" % (argv[0], '127.0.0.1', '80'))
        exit()
    ip = argv[1]
    port = int(argv[2])
    print(checker(ip, port))
