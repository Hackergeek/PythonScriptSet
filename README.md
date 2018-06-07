# Python脚本集合

## kugou.py——获取酷狗TOP500歌曲信息

## autofillconfig.py

### 介绍
获取免费代理服务器页面信息，并自动填写gui-config.json

### 环境配置
* pip install requests
* pip install fire
* pip install bs4

### 用法
python autofillconfig.py fill_config path

（path是gui-config.json文件的路径）

例如：python autofillconfig.py fill_config E:\ssr-4.1.4-win\gui-config.json