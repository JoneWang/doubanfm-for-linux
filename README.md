# Douban FM

*GUI版本正在努力开发中，见[gui branch](https://github.com/mckelvin/doubanfm-cli-for-linux/tree/gui)。*

一个会自动同步播放信息到Skype签名的终端豆瓣FM客户端 :musical_note:

## 系统环境

* 支持notify-osd的Linux桌面
* Skype 

## 依赖安装

1. 安装不同发行版下的[gst-python](http://gstreamer.freedesktop.org/modules/gst-python.html)，
   如Archlinux下为[gstreamer0.10-python](https://www.archlinux.org/packages/extra/x86_64/gstreamer0.10-python/)
   确保能在python中`import pygst; import gst`
2. 安装不同发行版下的[notify-python](http://www.galago-project.org/news/index.php)，
   如Archlinux下为[python2-notify](https://www.archlinux.org/packages/extra/x86_64/python2-notify/)
   确保能在python中`import pynotify`
3. 安装其他依赖`pip install -r requirements.txt`

## 使用
    
    # 安装
    chmod +x ./doubanfm
    sudo ln -sf ./doubanfm /usr/local/bin/doubanfm
    
    # 登录(可选)
    # 创建 .cookie 文件，将http://douban.fm/的cookie的结果写入其中

    # 运行 
    $ doubanfm 
    $ doubanfm http://douban.fm/?start=756523g8452g-3&cid=-3
    $ doubanfm http://douban.fm/?cid=1002215
    $ doubanfm http://douban.fm/?context=channel:0|musician_id:103874

# 命令

*注意: 大小写敏感*

* Q : 退出
* n : 下一首
* b : 垃圾桶
* r : 红心
* u : 取消红心
* p : 暂停
* P : 播放
* h : 帮助

# 演示

http://ascii.io/a/2585 乱码是ascii.io的bug :wink:
