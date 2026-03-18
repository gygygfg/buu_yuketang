# 使用国内镜像源加速下载
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/selenium/standalone-chrome:latest

# 镜像信息
# 镜像ID: sha256:66d3196083caf1a88ce193e44efe72c2a6b43fbd684062654cb42d142ea5a1f7
# 大小: 1.44GB
# 创建时间: 2024-09-22
# 平台: linux/amd64

USER root

# 更新包管理器并安装必要的软件
RUN apt-get update && apt-get install -y \
  xfce4 \
  xfce4-terminal \
  vim \
  curl \
  wget \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# 设置环境变量
ENV SE_SCREEN_WIDTH=1920
ENV SE_SCREEN_HEIGHT=1080
ENV SE_SCREEN_DEPTH=24
ENV SE_SCREEN_DPI=96
ENV SE_START_XVFB=true
ENV SE_START_VNC=true
ENV SE_START_NO_VNC=true
ENV SE_NO_VNC_PORT=7900
ENV SE_VNC_PORT=5900
ENV DISPLAY=:99.0
ENV DISPLAY_NUM=99

# 暴露端口
EXPOSE 4444
EXPOSE 5900
EXPOSE 7900

# 设置工作目录
WORKDIR /home/seluser

# 切换回默认用户
USER seluser

# 启动命令 - 使用镜像自带的 entry_point.sh
CMD ["/opt/bin/entry_point.sh"]
