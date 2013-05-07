# Douban FM GUI

啊……我还没想好这个APP叫什么好，暂时简称为GUI
本[分支](https://github.com/mckelvin/doubanfm-cli-for-linux/tree/gui)正在努力开发中……目前处于**能用**状态。

## 演示

界面高仿Web版Douban FM

![preview](https://github.com/mckelvin/doubanfm-cli-for-linux/raw/gui/misc/preview.png)


## 依赖

这个APP主要使用Python语言开发，PyQt4用于GUI，Qt自带的Phonon用于播放。

System Packages:

- qt4 ([extra/qt4](https://www.archlinux.org/packages/extra/x86_64/qt4/) for ArchLinux)
- pyqt ([extra/python2-pyqt](https://www.archlinux.org/packages/extra/x86_64/python2-pyqt/) for ArchLinux)
- atleast one [phonon-backend](http://zh.wikipedia.org/wiki/Phonon_(KDE)) (`aur/phonon-mplayer-git` 
or `extra/phonon-gstreamer` or `extra/phonon-vlc` for ArchLinux, 
also see [the wiki](https://wiki.archlinux.org/index.php/KDE#Which_backend_should_I_choose.3F))

Python Modules(also see `requirements.txt`):

- requests >= 1.2.0
- BeautifulSoup >= 3.2.1

Python Modules(Optional):

- Skype4Py
- pynotify

## 如何使用

    ## 建议先软链接到某一PATH目录
    $ sudo ln -sf `pwd`/bin/doubanfm /usr/local/bin/doubanfm

    ## 然后就可以这样了：
    $ doubanfm http://dou.bz/143WMS
    $ doubanfm http://t.cn/aNs4Tx
    $ doubanfm http://douban.fm/?start=181910g2440g0&cid=0
    $ doubanfm http://douban.fm/?context=channel:0|musician_id:103766

### 登录

目前登录的方式非常简陋，你需要将douban.fm的cookie填入`src/.cookie`文件中。
**注意**：由于豆瓣FM cookie安全限制，`document.cookie`并不能得到完整的Cookie，
请抓包或者使用Chrome打开 http://douban.fm ，打开控制台 - Network - Headers - Request
Headers，人工复制粘贴，确保Cookie中包含了`dbcl2`。
Example:

    $ cat .cookie 
    bid="ggggggggggg"; ck="Mklm"; dbcl2="1000103:A01024n8964"; flag="ok"; openExpPan=Y; show_pro_init_tip=N

登录之后tray icon上右键你会发现你的id，否则会提示未登录。


![登录后是这样的](https://github.com/mckelvin/doubanfm-cli-for-linux/raw/gui/misc/login.png)


