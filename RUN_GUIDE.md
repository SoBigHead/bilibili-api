# bilibili-api 运行指南

## 🚀 快速开始

### 1. 环境准备

确保你的系统满足以下要求：
- Python 3.9 或更高版本
- 网络连接正常

### 2. 安装依赖

运行环境设置脚本：

```bash
python setup_environment.py
```

或者手动安装：

```bash
# 安装基础依赖
pip install python-dotenv aiohttp

# 安装 bilibili-api 依赖
pip install -r requirements.txt
```

### 3. 配置认证信息

你已经在 `.env` 文件中配置了认证信息，格式如下：

```env
BILI_SESSDATA=你的SESSDATA
BILI_CSRF=你的bili_jct
BILI_BUVID3=你的buvid3
BILI_BUVID4=你的buvid4
BILI_DEDEUSERID=你的DedeUserID
```

## 📋 运行示例

### 1. 基础功能测试

运行综合测试脚本：

```bash
python test_bilibili_api.py
```

这个脚本会测试：
- ✅ 视频信息获取（无需登录）
- ✅ 搜索功能（无需登录）
- ✅ 用户信息获取（需要登录）
- ✅ 视频点赞功能（需要登录）

### 2. 视频下载示例

运行视频下载脚本：

```bash
python download_video_example.py
```

这个脚本会：
- 获取视频信息
- 分析下载链接
- 下载视频文件
- 提供 ffmpeg 转换建议

### 3. 自定义使用

创建你自己的脚本：

```python
import asyncio
import os
from dotenv import load_dotenv
from bilibili_api import Credential, video, user

# 加载环境变量
load_dotenv()

def get_credential():
    return Credential(
        sessdata=os.getenv("BILI_SESSDATA"),
        bili_jct=os.getenv("BILI_CSRF"),
        buvid3=os.getenv("BILI_BUVID3"),
        buvid4=os.getenv("BILI_BUVID4"),
        dedeuserid=os.getenv("BILI_DEDEUSERID")
    )

async def main():
    # 你的代码逻辑
    credential = get_credential()
    
    # 获取用户信息
    u = user.User(credential=credential)
    info = await u.get_self_info()
    print(f"用户名: {info['name']}")
    
    # 获取视频信息
    v = video.Video(bvid="BV1uv411q7Mv")
    video_info = await v.get_info()
    print(f"视频标题: {video_info['title']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔧 常见问题

### 1. 认证失败

如果出现认证相关错误：

1. 检查 `.env` 文件格式是否正确
2. 确认 Cookie 值是否有效（可能已过期）
3. 重新从浏览器获取最新的 Cookie 值

### 2. 网络请求失败

如果出现网络相关错误：

```python
from bilibili_api import request_settings

# 设置代理（如果需要）
request_settings.set_proxy("http://your-proxy.com")

# 增加超时时间
request_settings.set_timeout(10.0)

# 禁用 SSL 验证（不推荐）
request_settings.set_verify_ssl(False)
```

### 3. 反爬虫限制

如果遇到 412 错误：

1. 降低请求频率
2. 使用代理
3. 设置随机延迟

```python
import random
import asyncio

# 在请求之间添加延迟
await asyncio.sleep(random.uniform(1, 3))
```

### 4. 依赖安装问题

如果依赖安装失败：

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ package_name

# 如果是 M1 Mac，可能需要特殊处理
pip install --no-binary :all: package_name
```

## 📚 更多功能

### 可用的模块

- `video` - 视频相关操作
- `user` - 用户相关操作
- `live` - 直播相关操作
- `dynamic` - 动态相关操作
- `comment` - 评论相关操作
- `search` - 搜索功能
- `bangumi` - 番剧相关操作
- `article` - 专栏文章操作
- 更多模块请查看 `docs/examples/` 目录

### 示例代码位置

- 基础示例：`docs/examples/`
- 测试代码：`tests/`
- 工具脚本：`scripts/`

## ⚠️ 重要提醒

1. **合法使用**：仅用于学习和个人使用，不要用于商业用途
2. **频率控制**：避免高频请求，防止触发反爬虫机制
3. **数据安全**：不要泄露你的认证信息
4. **遵守条款**：遵守 B站 的使用条款和相关法律法规

## 🆘 获取帮助

- 查看项目文档：`docs/`
- 查看示例代码：`docs/examples/`
- 查看测试代码：`tests/`
- GitHub Issues：项目的 GitHub 页面

祝你使用愉快！🎉
