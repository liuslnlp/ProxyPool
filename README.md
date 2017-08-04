# ProxyPool
[![Build Status](https://travis-ci.org/WiseDoge/ProxyPool.svg?branch=master)](https://travis-ci.org/WiseDoge/ProxyPool)   
跨语言高性能IP代理池，Python实现。    

注意：请运行程序前先更新一下抓取代理的爬虫。

## 运行环境

* Python 3.6

  (请务必保证Python的版本在3.6以上，否则异步检验无法使用。)

* Redis 

  Redis官网并没有提供Windows的安装版，Windows用户可以[点击此处](http://pan.baidu.com/s/1kVe6lc7)下载一个我自己编译的二进制版本(3.2版本2.7MB，VS 2015编译)。

## 安装

### ① 直接使用

#### 安装依赖

`$ pip install -r requirements.txt`

*Windows用户如果无法安装lxml库请[点击这里](http://www.lfd.uci.edu/~gohlke/pythonlibs/)*。

#### 打开代理池和API

`$ cd proxypool`

`$ python3 run.py `

### ② 安装使用

#### 安装

`$ cd proxypool`

`$ python setup.py install`

#### 打开代理池和API

`$ proxypool_run`


## 使用API获取代理

访问`http://127.0.0.1:5000/`进入主页，如果显示'Welcome'，证明成功启动。

![pic](docs/1.png)

访问`http://127.0.0.1:5000/get`可以获取一个可用代理。  

![pic](docs/3.png)

访问`http://127.0.0.1:5000/count`可以获取代理池中可用代理的数量。  

![pic](docs/2.png)

也可以在程序代码中用相应的语言获取，例如:

```
import requests
from bs4 import BeautifulSoup
import lxml

def get_proxy():
    r = requests.get('http://127.0.0.1:5000/get')
    proxy = BeautifulSoup(r.text, "lxml").get_text()
    return proxy
```
## 文件结构
![picture](docs/5.png)
![picture](docs/4.png)
