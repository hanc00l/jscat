#!/usr/bin/env python3
# coding:utf-8
# Forked from Koadic linter.py && loader.py

import requests
import base64
import rjsmin
import binascii
import random
import string


'''
调用在线混淆工具进行JS混淆
'''


def online_obfuscate(script):
    try:
        based_data = base64.b64encode(script).decode()

        url = "https://www.online-toolz.com:443/functions/JS-OBFUSCATE.php"
        headers = {"Connection": "close",
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                   "Content-Type": "application/x-www-form-urlencoded",
                   "Accept": "*/*",
                   "Origin": "https://www.online-toolz.com",
                   "Referer": "https://www.online-toolz.com/tools/javascript-obfuscator.php",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,da;q=0.6"}
        data = {"input": based_data}
        r = requests.post(url, headers=headers, data=data, timeout=5)

        return r.text.strip().encode()
    except:
        return script


'''
对JS进行XOR混淆，代码fork自Koadic
'''


def create_xor_key():
    return "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(10, 20)))


def xor_data(data, key):
    while len(key) < len(data):
        key += key

    return binascii.hexlify("".join([chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(data.decode(), key)]).encode())


def xor_js_file(script, key):
    function_name = "".join(random.choice(
        string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(10, 20)))
    var_encoded = "".join(random.choice(string.ascii_uppercase +
                                        string.ascii_lowercase) for _ in range(random.randint(10, 20)))
    var_decoded = "".join(random.choice(string.ascii_uppercase +
                                        string.ascii_lowercase) for _ in range(random.randint(10, 20)))
    var_key = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase)
                      for _ in range(random.randint(10, 20)))
    var_s = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase)
                    for _ in range(random.randint(10, 20)))
    var_e_len = "".join(random.choice(
        string.ascii_uppercase + string.ascii_lowercase) for _ in range(101))
    var_e_var = "".join(random.choice(string.ascii_uppercase +
                                      string.ascii_lowercase) for _ in range(random.randint(10, 20)))
    var_v_len = "".join(random.choice(
        string.ascii_uppercase + string.ascii_lowercase) for _ in range(118))
    var_v_var = "".join(random.choice(string.ascii_uppercase +
                                      string.ascii_lowercase) for _ in range(random.randint(10, 20)))
    var_a_len = "".join(random.choice(
        string.ascii_uppercase + string.ascii_lowercase) for _ in range(97))
    var_a_var = "".join(random.choice(string.ascii_uppercase +
                                      string.ascii_lowercase) for _ in range(random.randint(10, 20)))
    var_l_len = "".join(random.choice(
        string.ascii_uppercase + string.ascii_lowercase) for _ in range(108))
    var_l_var = "".join(random.choice(string.ascii_uppercase +
                                      string.ascii_lowercase) for _ in range(random.randint(10, 20)))
    var_eval_arr = "".join(random.choice(string.ascii_uppercase +
                                         string.ascii_lowercase) for _ in range(random.randint(10, 20)))
    var_eval = "".join(random.choice(string.ascii_uppercase +
                                     string.ascii_lowercase) for _ in range(random.randint(10, 20)))
    js = """function """+function_name+"""("""+var_encoded+""", """+var_key+""") {
var """+var_decoded+""" = '';
while ("""+var_key+""".length < """+var_encoded+""".length) {
"""+var_key+""" += """+var_key+""";
}
for (i = 0; i < """+var_encoded+""".length; i+=(80/40)) {
var """+var_s+""" = String.fromCharCode(parseInt("""+var_encoded+""".substr(i, 103-101), 9+7) ^ """+var_key+""".charCodeAt(i/(20-18)));
"""+var_decoded+""" = """+var_decoded+""" + """+var_s+""";
}
return """+var_decoded+""";
}

var """+var_e_var+""" = \""""+var_e_len+"""\";
var """+var_v_var+""" = \""""+var_v_len+"""\";
var """+var_a_var+""" = \""""+var_a_len+"""\";
var """+var_l_var+""" = \""""+var_l_len+"""\";
var """+var_eval_arr+""" = [String.fromCharCode("""+var_e_var+""".length), String.fromCharCode("""+var_v_var+""".length), String.fromCharCode("""+var_a_var+""".length), String.fromCharCode("""+var_l_var+""".length)];
var """+var_eval+""" = this["""+var_eval_arr+"""[13-13]+"""+var_eval_arr+"""[24-23]+"""+var_eval_arr+"""[94-92]+"""+var_eval_arr+"""[46-43]];
"""+var_eval+"""("""+function_name+"""('"""+script+"""', '"""+key+"""'));"""
    return js


def xor_obfuscate(script):
    key = create_xor_key()
    data = xor_data(script, key)
    result = xor_js_file(data.decode(), key)

    return result.encode()


def Obfuscator(script):
    script_ob = xor_obfuscate(script)
    script_ob_min = rjsmin.jsmin(script_ob)

    #script_ob_min = online_obfuscate(script)

    return script_ob_min
