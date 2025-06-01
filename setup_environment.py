#!/usr/bin/env python3
"""
环境设置脚本
自动安装必要的依赖包
"""

import subprocess
import sys
import os

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 成功")
        if result.stdout:
            print(f"输出: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败")
        print(f"错误: {e.stderr.strip()}")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"🐍 Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ bilibili-api 需要 Python 3.9 或更高版本")
        return False
    
    print("✅ Python 版本符合要求")
    return True

def install_dependencies():
    """安装依赖包"""
    print("📦 开始安装依赖包...")
    
    # 基础依赖
    basic_deps = [
        "python-dotenv",  # 用于读取 .env 文件
        "aiohttp",        # 异步HTTP客户端
    ]
    
    # bilibili-api 的依赖
    bilibili_deps = [
        "beautifulsoup4~=4.13.4",
        "colorama~=0.4.6", 
        "lxml~=5.4.0",
        "pyyaml~=6.0",
        "brotli~=1.1.0",
        "qrcode~=8.2",
        "APScheduler~=3.11.0",
        "pillow~=11.2.1",
        "yarl~=1.20.0",
        "pycryptodomex~=3.23.0",
        "qrcode_terminal~=0.8",
        "PyJWT~=2.10.1"
    ]
    
    all_deps = basic_deps + bilibili_deps
    
    for dep in all_deps:
        if not run_command(f"pip install {dep}", f"安装 {dep}"):
            return False
    
    return True

def test_imports():
    """测试导入"""
    print("🧪 测试模块导入...")
    
    test_modules = [
        ("dotenv", "python-dotenv"),
        ("aiohttp", "aiohttp"),
        ("bilibili_api", "bilibili-api (本地)"),
    ]
    
    for module, description in test_modules:
        try:
            __import__(module)
            print(f"✅ {description} 导入成功")
        except ImportError as e:
            print(f"❌ {description} 导入失败: {e}")
            return False
    
    return True

def main():
    """主函数"""
    print("🚀 bilibili-api 环境设置")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return
    
    print("\n" + "=" * 50)
    
    # 安装依赖
    if not install_dependencies():
        print("❌ 依赖安装失败，请检查网络连接和权限")
        return
    
    print("\n" + "=" * 50)
    
    # 测试导入
    if not test_imports():
        print("❌ 模块导入测试失败")
        return
    
    print("\n" + "=" * 50)
    print("🎉 环境设置完成！")
    print("\n📋 接下来你可以:")
    print("1. 运行测试脚本: python test_bilibili_api.py")
    print("2. 运行下载示例: python download_video_example.py")
    print("3. 查看项目文档: docs/")
    
    print("\n⚠️  重要提醒:")
    print("- 请确保 .env 文件中的认证信息正确")
    print("- 使用时请遵守 B站 的使用条款")
    print("- 控制请求频率，避免触发反爬虫机制")

if __name__ == "__main__":
    main()
