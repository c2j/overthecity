高空抛物监控 overthecity
=======================
这是在[英特尔创客大赛](http://huati.weibo.com/k/IntelMaker)的一个作品。基本的想法是
希望利用Edison强大的计算能力，对高空抛物作监控、报警和云端管理。

## 为什么要做高空抛物监控
据说上海人的第二大恶习是高空抛物，前不久，还看到新闻说有老人在公园散步，却被从天而降的啤酒
瓶砸中不治身亡。新闻中说后续将采取在小区中加强监控。而我这个Idea，是在大赛当天学习Edison功
能的时候突然想起来的。

## 怎么才能做到
### 开始的想法
一开始，想基于运动捕获来实现对高空抛物的感应：感应周边范围的物体移动，排除雨、雪、雹等天气因素，将高空抛物的起点和落点计算出来，并实时启动，高速摄影，同时将抛物纪录上传到监控中心。难点在于感应移动的范围最大有多大、灵敏度如何。
经过对Edison周边传感器的了解，这种想法不可行。因为目前的运动传感器必须安装在运动物体上，而不是像我一开始想象的那样，能实现运动感应。而红外、超声等传感器的作用范围有限，无法实现对一整栋楼或一个单元的监控。除非有一个类似于雷达那样的感应器，也不知是否存在这样的民用的雷达。

### 经过修正的想法
基于摄像头。摄像头总是处于启动状态，利用edison的计算能力，在本地进行图像识别和运算，将疑似抛物的影像（时间段等）上传到云监控中心，由云监控中心进行人工确认处理。
  需要：
   1、开发感应器终端的应用：计算移动，将影像片段上传至云端，注册感应器终端
   2、利用小区的wifi上传到云端
   3、云端应用：部署在Intel的云上，分管理功能和注册感应器、接收影像API等功能

## 环境准备
### 第一步 确认摄像头驱动安装成功
IMPORTANT：当使用摄像头时，不能使用USB供电，必须将拨片切换到右边，并且使用外接电源
新的edison已经有了video驱动了，无需重编译内核（如果重编译，会报错，只有重刷flash才能恢复）
```
modprobe uvcvideo
dmesg
ls /dev/video*
```

下载[edi_cam](https://github.com/drejkim/edi-cam)，按照文档要求，依次执行：
1 安装ffmpeg
2 安装node的几个组件：morgan、express、ws
3 修改client中硬编码的IP地址为Edison地址：10.255.1.47 edison_ip
4 启动Server
5 打开浏览器，输入http://edison_ip:8080/ 将能看到视频聊天图像。至此，说明摄像头已安装可用

### 确保Python可以访问摄像头
以下步骤均在Edison上执行：
1 安装pip

```
wget https://bootstrap.pypa.io/ez_setup.py -O - | python
```

```
wget "https://pypi.python.org/packages/source/p/pip/pip-7.1.2.tar.gz#md5=3823d2343d9f3aaab21cf9c917710196"

tar xzvf pip-7.1.2.tar.gz
cd pip-7.1.2
python setup.py install
```

2 安装numpy（编译opencv python库需要）
```
pip install numpy
pip install imutils
```

3 安装opencv
请忽略，跳到3.1执行，因为如下编译源码的方式一直不行，只好另寻他径
```
cmake -D WITH_IPP=OFF -D WITH_TBB=OFF -D BUILD_TBB=ON -D WITH_CUDA=OFF -D WITH_OPENCL=OFF -D BUILD_SHARED_LIBS=OFF -D BUILD_PERF_TESTS=OFF -D BUILD_TESTS=OFF -D BUILD_opencv_python2=ON .

make -j2

make install
```

确认是否安装成功，使用如下命令：
```
python -c "import cv2"
```
如果报错，则说明python opencv安装不成功

可以用的其他方法：
3.1 修改opkg配置文件/etc/opkg/base-feeds.conf，增加如下内容：
```
src/gz all http://repo.opkg.net/edison/repo/all
src/gz edison http://repo.opkg.net/edison/repo/edison
src/gz core2-32 http://repo.opkg.net/edison/repo/core2-32
```
然后执行：
```
opkg update
```

3.2 安装
```
opkg install opencv
opkg install python-opencv
```
后一步会安装很多包，耐心等待，完成后执行`python -c "import cv2" `应该就不会再报错了。
