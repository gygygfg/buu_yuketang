# 使用说明

## 快速开始

### 方法一：使用 Docker Compose（推荐）

1. **启动服务**：
   ```bash
   docker-compose up -d
   ```

2. **查看日志**：
   ```bash
   docker-compose logs -f
   ```

3. **停止服务**：
   ```bash
   docker-compose down
   ```

### 方法二：使用 Docker 命令

1. **构建镜像**：
   ```bash
   docker build -t selenium-chrome-vnc .
   ```

2. **运行容器**：
   ```bash
   docker run -d \
     -p 4444:4444 \
     -p 5900:5900 \
     -p 7900:7900 \
     -e VNC_PASSWORD=your_password \
     --name selenium-chrome \
     --shm-size=2g \
     selenium-chrome-vnc
   ```

3. **查看容器状态**：
   ```bash
   docker ps
   docker logs selenium-chrome
   ```

4. **进入容器**：
   ```bash
   docker exec -it selenium-chrome bash
   ```

5. **停止容器**：
   ```bash
   docker stop selenium-chrome
   docker rm selenium-chrome
   ```

## 访问服务

### 1. Selenium WebDriver
- **URL**: http://localhost:4444
- **WebDriver 端点**: http://localhost:4444/wd/hub
- **状态页面**: http://localhost:4444/status

### 2. VNC 远程桌面
- **端口**: 5900
- **密码**: secret（默认）或您设置的密码
- **使用 VNC 客户端连接**：
  - 地址: `localhost:5900`
  - 使用 TigerVNC、RealVNC 等客户端

### 3. noVNC 网页版
- **URL**: http://localhost:7900
- **无需安装客户端，直接在浏览器中访问**

## 测试 Selenium

### Python 测试
1. 安装依赖：
   ```bash
   pip install selenium
   ```

2. 运行测试脚本：
   ```bash
   python test_selenium.py
   ```

### 手动测试
1. 访问 Selenium Grid 控制台：http://localhost:4444
2. 查看可用节点和会话
3. 使用浏览器开发者工具测试 API

## 配置说明

### 环境变量
可以在 `docker-compose.yml` 或 `docker run` 命令中设置：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| VNC_PASSWORD | VNC 连接密码 | secret |
| SE_SCREEN_WIDTH | 屏幕宽度 | 1920 |
| SE_SCREEN_HEIGHT | 屏幕高度 | 1080 |
| SE_SCREEN_DEPTH | 屏幕色深 | 24 |
| SE_NO_VNC_PORT | noVNC 端口 | 7900 |
| SE_VNC_PORT | VNC 端口 | 5900 |

### 性能优化
1. **共享内存**：使用 `/dev/shm` 挂载提高性能
2. **SHM 大小**：设置为 2GB 以支持多标签页
3. **网络模式**：使用桥接网络确保容器间通信

## 故障排除

### 常见问题

1. **容器启动失败**
   ```bash
   # 检查日志
   docker-compose logs
   
   # 检查端口占用
   netstat -tulpn | grep :4444
   ```

2. **Selenium 连接失败**
   - 确保容器正在运行：`docker ps`
   - 检查端口映射：`docker port selenium-chrome`
   - 测试连接：`curl http://localhost:4444/status`

3. **VNC 连接失败**
   - 检查 VNC 密码是否正确
   - 确保防火墙允许端口 5900
   - 尝试使用 noVNC（网页版）

4. **浏览器崩溃或内存不足**
   ```bash
   # 增加共享内存
   docker run --shm-size=2g ...
   
   # 或修改 docker-compose.yml
   shm_size: '2gb'
   ```

### 日志查看
```bash
# 实时查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs selenium-chrome

# 查看容器内部日志
docker exec selenium-chrome cat /tmp/supervisord.log
```

## 扩展使用

### 多浏览器测试
可以扩展支持 Firefox、Edge 等其他浏览器。

### 集成到 CI/CD
将 Selenium 容器集成到 Jenkins、GitLab CI 等持续集成系统中。

### 集群部署
使用 Selenium Grid 部署多个节点进行并行测试。

## 安全建议

1. **修改默认密码**：生产环境中务必修改 VNC_PASSWORD
2. **限制网络访问**：使用防火墙限制对端口的访问
3. **定期更新**：定期更新基础镜像以获取安全补丁
4. **日志监控**：监控容器日志，及时发现异常