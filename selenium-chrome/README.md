# Selenium Standalone Chrome Docker 镜像

基于 [selenium/standalone-chrome](https://hub.docker.com/r/selenium/standalone-chrome) 镜像的增强版本，添加了桌面环境和 VNC 支持。

## 镜像信息

- **基础镜像**: `selenium/standalone-chrome:latest`
- **国内镜像源**: `swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/selenium/standalone-chrome:latest`
- **镜像ID**: `sha256:66d3196083caf1a88ce193e44efe72c2a6b43fbd684062654cb42d142ea5a1f7`
- **大小**: 1.44GB
- **平台**: linux/amd64
- **创建时间**: 2024-09-22

## 功能特性

1. **Selenium WebDriver**: 完整的 Selenium WebDriver 服务器
2. **Chrome 浏览器**: 预安装 Chrome 浏览器
3. **桌面环境**: 添加 XFCE4 桌面环境
4. **VNC 支持**: 支持 VNC 远程访问
5. **终端**: 包含 xfce4-terminal

## 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| SE_SCREEN_WIDTH | 1920 | 屏幕宽度 |
| SE_SCREEN_HEIGHT | 1080 | 屏幕高度 |
| SE_SCREEN_DEPTH | 24 | 屏幕色深 |
| SE_SCREEN_DPI | 96 | 屏幕DPI |
| SE_START_XVFB | true | 启动 Xvfb |
| SE_START_VNC | true | 启动 VNC 服务器 |
| SE_START_NO_VNC | true | 启动 noVNC |
| SE_NO_VNC_PORT | 7900 | noVNC 端口 |
| SE_VNC_PORT | 5900 | VNC 端口 |
| DISPLAY | :99.0 | 显示设置 |
| DISPLAY_NUM | 99 | 显示编号 |

## 暴露端口

- **4444**: Selenium WebDriver 端口
- **5900**: VNC 端口
- **7900**: noVNC 端口

## 使用方法

### 1. 构建镜像
```bash
docker build -t selenium-chrome-vnc .
```

### 2. 运行容器
```bash
docker run -d \
  -p 4444:4444 \
  -p 5900:5900 \
  -p 7900:7900 \
  --name selenium-chrome \
  selenium-chrome-vnc
```

### 3. 访问服务

- **Selenium WebDriver**: http://localhost:4444
- **VNC 客户端**: 连接 localhost:5900 (密码: secret)
- **noVNC 网页版**: http://localhost:7900

### 4. 使用 Python 测试脚本
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
)

driver.get("https://www.google.com")
print(driver.title)
driver.quit()
```

## 镜像构建历史

从爬取的信息中获取的构建历史：

```
# 2024-09-22 20:34:48 - 声明容器运行时监听的端口
EXPOSE map[4444/tcp:{}]

# 2024-09-22 20:34:48 - 设置环境变量
ENV SE_SESSION_REQUEST_TIMEOUT=300 SE_SESSION_RETRY_INTERVAL=15 SE_HEALTHCHECK_INTERVAL=120 SE_RELAX_CHECKS=true SE_REJECT_UNSUPPORTED_CAPS=true SE_OTEL_SERVICE_NAME=selenium-standalone

# 2024-09-22 20:34:48 - 复制配置文件
COPY --chown=1200:1201 generate_config /opt/bin/generate_config
COPY selenium.conf /etc/supervisor/conf.d/
COPY --chown=1200:1201 start-selenium-standalone.sh /opt/bin/start-selenium-standalone.sh

# 2024-09-22 20:34:48 - 设置用户
USER 1200

# 2024-09-22 20:34:48 - 添加元数据标签
LABEL authors=SeleniumHQ
```

## 注意事项

1. 镜像较大（1.44GB），请确保有足够的磁盘空间
2. 使用国内镜像源加速下载
3. VNC 默认密码为 "secret"
4. 建议在生产环境中设置更强的密码

## 许可证

基于 SeleniumHQ 的镜像，遵循相应的开源许可证。