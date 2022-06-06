#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: app.py
@time: 2020/10/13
@email: coderflying@163.com
@desc: 
"""
import binascii
import json
import os
import platform
import random
import re
import subprocess
import time
import urllib.request

from flask import Flask, jsonify


def get_random_mc():
    mc = '{}:{}:{}:{}:{}:{}'.format("".join(random.choices(mc_random, k=2)), "".join(random.choices(mc_random, k=2)),
                                    "".join(random.choices(mc_random, k=2)), "".join(random.choices(mc_random, k=2)),
                                    "".join(random.choices(mc_random, k=2)), "".join(random.choices(mc_random, k=2)))
    return mc


def get_system():
    system = platform.system()
    if system.startswith("Win"):
        return "win" + platform.machine()[-2:]
    elif system.startswith("Lin"):
        return "linux" + platform.machine()[-2:]
    else:
        return "osx64"


def hexStr_to_str(hex_str):
    hexadecimal = hex_str.encode('utf-8')
    str_bin = binascii.unhexlify(hexadecimal)
    return str_bin


os.environ['WORKON_HOME'] = "value"
system = get_system()
nativate_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nativates")
jar_path = os.path.join(nativate_path, "unidbg.jar")
jni_path = os.path.join(os.path.join(nativate_path, "prebuilt"), system)
os.chdir(nativate_path)
mc_random = ["a", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
headers = {
    'Sdk-Version': '1',
    'Content-Type': 'application/octet-stream;tt-data=a',
    'X-Ss-Stub': 'E651E662F5735C205A16D3F81B13F86E',
    'User-Agent': 'com.ss.android.ugc.aweme/710 (Linux; U; Android 10; zh_CN; M2004J19C; Build/QP1A.190711.020; Cronet/58.0.2991.0)',
    'X-Khronos': '1654511777',
    # 'X-Gorgon':'xxx',
    'Accept-Encoding': 'gzip',
    'X-Ss-Queries': 'dGMCDr6ot3awANG2fsgrATtxtRzlM0idCowOV8iipanQXTxYYqaoj77zugBiomr4xg0LW77Cl7wSVayKyMyZVxwEPABnCuzsnqwgLlCM%2FjNc8fV7',
    'X-Ss-Req-Ticket': '1654511777248',
    'Connection': 'keep-alive',
    'X-Pods': '',
}
app = Flask(__name__)


@app.route("/", methods=['GET'])
def register():
    gen_time = str(int(time.time() * 1000))
    udid = str(random.randint(321480502743165, 921480502743165))
    openudid = "".join([random.choice("abcdefghijklmn1234567890") for i in range(16)])
    mc = get_random_mc()
    message = " ".join([gen_time, udid, openudid, mc])
    command = r"java -jar -Djna.library.path={} -Djava.library.path={} unidbg.jar {}".format(jni_path, jni_path,
                                                                                             message)
    stdout, stderr = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    hex_str = re.search(r'hex=([\s\S]*?)\nsize', stdout.decode()).group(1)
    astr = hexStr_to_str(hex_str)
    register_url = 'https://log.snssdk.com/service/2/device_register/?ac=wifi&channel=tianzhuo_dy_sg3&aid=1128&app_name=aweme&version_code=710&version_name=7.1.0&device_platform=android&ssmix=a' \
                   '&device_type=M2004J19C' \
                   '&device_brand=Redmi&language=zh&os_api=29&os_version=10' \
                   '&openudid=4f1a7a08c25b427a&manifest_version_code=710&resolution=1080*2134&dpi=440&update_version_code=7102' \
                   '&_rticket=1654511777235&app_type=normal&mcc_mnc=46011' \
                   '&ts=1654511777&tt_data=a'
    request = urllib.request.Request(url=register_url, data=astr, headers=headers)
    response = urllib.request.urlopen(request)
    return jsonify(json.loads(response.read()))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
