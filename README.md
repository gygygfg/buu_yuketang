# BUU 雨课堂自动化学习工具

一个基于 Selenium 的自动化工具，用于自动完成北京联合大学雨课堂平台上的课程学习任务。

## ✨ 功能特性

- ✅ **自动登录**：支持账号密码登录雨课堂平台
- ✅ **课程选择**：自动选择指定课程并进入学习页面
- ✅ **章节遍历**：自动查找并处理所有未完成的章节
- ✅ **视频播放**：自动点击播放按钮并监控视频进度
- ✅ **进度监控**：实时监控学习进度，确保视频完整播放
- ✅ **智能重试**：内置多种重试机制，提高稳定性
- ✅ **Docker 支持**：提供完整的 Docker 环境，一键部署
- ✅ **VNC 远程控制**：支持通过 VNC 远程监控自动化过程

## 📋 系统要求

- Python 3.12 或更高版本
- Docker 和 Docker Compose（推荐使用 Docker 方式）
- 稳定的网络连接

## 🚀 快速开始

### 方法一：使用 Docker（推荐）

1. **克隆项目**
   ```bash
   git clone <项目地址>
   cd buu_yuketang
   ```

2. **配置账号信息**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填写您的雨课堂账号密码
   ```

3. **启动 Selenium Chrome 容器**
   ```bash
   cd selenium-chrome
   docker-compose up -d
   ```

4. **运行自动化脚本**
   ```bash
   cd ..
   python main.py
   ```

### 方法二：本地运行

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **配置账号信息**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填写您的雨课堂账号密码
   ```

3. **启动 Selenium Chrome**
   ```bash
   # 需要先安装并启动 Selenium Chrome 服务
   # 或者使用 Docker 方式启动 Selenium
   ```

4. **运行自动化脚本**
   ```bash
   python main.py
   ```

## ⚙️ 配置说明

### 环境变量配置（.env 文件）

```env
# 雨课堂账号密码配置
YUKETANG_USERNAME=您的手机号
YUKETANG_PASSWORD=您的密码

# 可选：设置代理（如果需要）
# HTTP_PROXY=http://proxy.example.com:8080
# HTTPS_PROXY=http://proxy.example.com:8080
```

### 课程配置（main.py 中修改）

在 `main.py` 文件中找到以下配置行，修改为您要学习的课程名称：

```python
COURSE_NAME = "创业:道与术(创新创业基础)"  # 要选择的课程名称
```

## 🐳 Docker 环境说明

### Selenium Chrome 容器

项目提供了完整的 Docker 环境，包含：

- **Selenium Grid**：在端口 4444 提供 WebDriver 服务
- **VNC 服务**：在端口 5900 提供 VNC 远程桌面
- **noVNC Web 界面**：在端口 7900 提供 Web 版 VNC

### 访问 VNC 远程桌面

1. **使用 VNC 客户端**
   - 地址：`localhost:5900`
   - 密码：`secret`（可在 docker-compose.yml 中修改）

2. **使用 Web 浏览器**
   - 地址：`http://localhost:7900`
   - 密码：`secret`

### 容器管理命令

```bash
# 启动容器
cd selenium-chrome
docker-compose up -d

# 查看容器状态
docker-compose ps

# 查看容器日志
docker-compose logs -f

# 停止容器
docker-compose down

# 重启容器
docker-compose restart
```

## 📝 使用说明

### 基本使用流程

1. **启动 Selenium Chrome 容器**
2. **配置账号和课程信息**
3. **运行自动化脚本**
4. **通过 VNC 监控自动化过程**
5. **脚本自动完成所有未完成章节**

### 脚本工作流程

1. **登录阶段**：自动登录雨课堂平台
2. **课程选择**：根据配置的课程名称选择对应课程
3. **章节遍历**：进入学习内容页面，查找所有未完成章节
4. **视频播放**：对每个未完成章节，自动播放视频并监控进度
5. **进度监控**：等待视频播放完成，记录学习进度
6. **循环处理**：处理完一个章节后，继续处理下一个未完成章节

### 监控和调试

- **控制台输出**：脚本会实时输出当前操作状态
- **截图功能**：在关键步骤会自动截图保存，便于调试
- **VNC 监控**：可以通过 VNC 实时查看自动化过程
- **日志记录**：所有操作都会在控制台详细记录

## 🔧 故障排除

### 常见问题

#### 1. 连接 Selenium 失败
```
正在连接到 Selenium Hub...
连接失败
```

**解决方案**：
- 确保 Selenium Chrome 容器已启动：`docker-compose ps`
- 检查端口 4444 是否被占用
- 等待容器完全启动（可能需要 30-60 秒）

#### 2. 登录失败
```
登录失败，停止执行后续操作
```

**解决方案**：
- 检查 `.env` 文件中的账号密码是否正确
- 查看 `login_debug.png` 截图了解登录页面状态
- 尝试手动登录确认账号状态

#### 3. 找不到课程
```
错误: 未找到课程: 课程名称
```

**解决方案**：
- 检查 `main.py` 中的 `COURSE_NAME` 配置
- 确保课程名称完全匹配（包括标点符号）
- 脚本会列出当前页面所有可见课程，请核对

#### 4. 找不到章节或视频
```
未找到章节项
未找到播放按钮
```

**解决方案**：
- 通过 VNC 查看页面实际结构
- 检查是否有弹窗或提示需要手动处理
- 尝试刷新页面后重新运行脚本

### 调试技巧

1. **启用详细日志**：脚本默认会输出详细的操作日志
2. **查看截图**：关键步骤会自动截图，保存在项目根目录
3. **使用 VNC 监控**：实时查看自动化过程，了解页面状态
4. **手动测试**：先手动完成一次操作，了解页面流程

## 📁 项目结构

```
buu_yuketang/
├── main.py                    # 主程序文件
├── pyproject.toml            # Python 项目配置
├── uv.lock                   # 依赖锁定文件
├── README.md                 # 项目说明文档
├── .env.example              # 环境变量示例
├── .gitignore                # Git 忽略文件
├── selenium-chrome/          # Docker 环境配置
│   ├── Dockerfile           # Docker 镜像构建文件
│   ├── docker-compose.yml   # Docker Compose 配置
│   ├── README.md            # Docker 环境说明
│   └── USAGE.md             # 使用说明
└── __pycache__/             # Python 缓存目录
```

## ⚠️ 注意事项

1. **账号安全**：请妥善保管您的账号密码，不要泄露 `.env` 文件
2. **合规使用**：本工具仅用于学习目的，请遵守学校相关规定
3. **网络稳定**：确保网络连接稳定，避免自动化过程中断
4. **时间安排**：建议在网络空闲时段运行，避免影响正常使用
5. **监控运行**：首次使用时建议通过 VNC 监控整个过程
6. **更新维护**：雨课堂平台可能会更新，如遇问题请及时更新脚本

## 🔄 更新和维护

### 更新依赖
```bash
# 使用 uv 更新依赖
uv sync

# 或使用 pip
pip install -r requirements.txt --upgrade
```

### 更新 Docker 镜像
```bash
cd selenium-chrome
docker-compose pull
docker-compose up -d
```

### 代码更新
```bash
git pull origin main
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目。

### 开发环境设置

1. Fork 项目到您的账户
2. 克隆您的 fork
3. 创建新的分支
4. 进行修改并测试
5. 提交 Pull Request

### 代码规范

- 遵循 Python PEP 8 编码规范
- 添加适当的注释和文档
- 确保代码可读性和可维护性

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 感谢 Selenium 项目提供的浏览器自动化框架
- 感谢 Docker 社区提供的容器化解决方案
- 感谢所有贡献者和用户的支持

## 📞 支持与反馈

如果您在使用过程中遇到问题或有改进建议，请：

1. 查看 [故障排除](#故障排除) 部分
2. 提交 [Issue](https://github.com/your-repo/issues)
3. 通过邮件联系维护者

---

**免责声明**：本工具仅供学习和研究使用，使用者需自行承担使用风险。请遵守相关法律法规和学校规定。