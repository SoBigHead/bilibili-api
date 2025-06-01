#!/usr/bin/env python3
"""
bilibili 视频下载示例
演示如何使用 bilibili-api 下载视频
"""

import os
import asyncio
from dotenv import load_dotenv
from bilibili_api import Credential, video, get_client, HEADERS

# 加载环境变量
load_dotenv()

def get_credential():
    """从环境变量获取认证信息"""
    return Credential(
        sessdata=os.getenv("BILI_SESSDATA"),
        bili_jct=os.getenv("BILI_CSRF"),
        buvid3=os.getenv("BILI_BUVID3"),
        buvid4=os.getenv("BILI_BUVID4"),
        dedeuserid=os.getenv("BILI_DEDEUSERID")
    )

async def download_file(url: str, output_path: str, description: str = "文件"):
    """下载文件的通用函数"""
    try:
        client = get_client()
        download_id = await client.download_create(url, HEADERS)
        total_size = client.download_content_length(download_id)
        
        print(f"开始下载 {description}...")
        print(f"文件大小: {total_size / 1024 / 1024:.2f} MB")
        
        downloaded = 0
        with open(output_path, "wb") as file:
            while True:
                chunk = await client.download_chunk(download_id)
                if not chunk:
                    break
                file.write(chunk)
                downloaded += len(chunk)
                
                # 显示进度
                progress = (downloaded / total_size) * 100
                print(f"\r{description} 下载进度: {progress:.1f}% [{downloaded}/{total_size}]", end="")
        
        print(f"\n✅ {description} 下载完成: {output_path}")
        return True
    except Exception as e:
        print(f"\n❌ {description} 下载失败: {e}")
        return False

async def get_video_info(bvid: str):
    """获取视频信息"""
    try:
        credential = get_credential()
        v = video.Video(bvid=bvid, credential=credential)
        info = await v.get_info()
        
        print(f"视频标题: {info['title']}")
        print(f"UP主: {info['owner']['name']}")
        print(f"时长: {info['duration']} 秒")
        print(f"分P数: {info['videos']}")
        
        return v, info
    except Exception as e:
        print(f"❌ 获取视频信息失败: {e}")
        return None, None

async def get_download_urls(v: video.Video, page_index: int = 0):
    """获取视频下载链接"""
    try:
        download_data = await v.get_download_url(page_index)
        detector = video.VideoDownloadURLDataDetecter(data=download_data)
        streams = detector.detect_best_streams()
        
        print(f"检测到 {len(streams)} 个流")
        
        # 检查是否为FLV或MP4流
        is_flv_mp4 = detector.check_flv_mp4_stream()
        print(f"流类型: {'FLV/MP4' if is_flv_mp4 else 'DASH (分离的音视频)'}")
        
        return streams, is_flv_mp4
    except Exception as e:
        print(f"❌ 获取下载链接失败: {e}")
        return None, None

async def download_video(bvid: str, output_dir: str = "downloads"):
    """下载视频主函数"""
    print(f"🎬 开始处理视频: {bvid}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取视频信息
    v, info = await get_video_info(bvid)
    if not v or not info:
        return False
    
    # 获取下载链接
    streams, is_flv_mp4 = await get_download_urls(v)
    if not streams:
        return False
    
    # 生成安全的文件名
    safe_title = "".join(c for c in info['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title[:50]  # 限制长度
    
    try:
        if is_flv_mp4:
            # FLV/MP4 流 - 单文件包含音视频
            print("📹 下载 FLV/MP4 流...")
            output_path = os.path.join(output_dir, f"{safe_title}.flv")
            success = await download_file(streams[0].url, output_path, "视频")
            
            if success:
                print(f"✅ 视频下载完成: {output_path}")
                print("💡 提示: 可以使用 ffmpeg 转换为 mp4 格式:")
                print(f"   ffmpeg -i \"{output_path}\" \"{output_path.replace('.flv', '.mp4')}\"")
        else:
            # DASH 流 - 音视频分离
            print("📹 下载 DASH 流 (音视频分离)...")
            
            # 下载视频流
            video_path = os.path.join(output_dir, f"{safe_title}_video.m4s")
            video_success = await download_file(streams[0].url, video_path, "视频流")
            
            # 下载音频流
            audio_path = os.path.join(output_dir, f"{safe_title}_audio.m4s")
            audio_success = await download_file(streams[1].url, audio_path, "音频流")
            
            if video_success and audio_success:
                output_path = os.path.join(output_dir, f"{safe_title}.mp4")
                print(f"✅ 音视频流下载完成")
                print("💡 提示: 使用 ffmpeg 合并音视频:")
                print(f"   ffmpeg -i \"{video_path}\" -i \"{audio_path}\" -c copy \"{output_path}\"")
                print("💡 合并后可删除临时文件:")
                print(f"   rm \"{video_path}\" \"{audio_path}\"")
        
        return True
    except Exception as e:
        print(f"❌ 下载过程出错: {e}")
        return False

async def main():
    """主函数"""
    print("🚀 bilibili 视频下载工具")
    
    # 检查环境变量
    required_vars = ["BILI_SESSDATA", "BILI_CSRF", "BILI_BUVID3", "BILI_DEDEUSERID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ 缺少环境变量: {', '.join(missing_vars)}")
        print("请检查 .env 文件是否正确配置")
        return
    
    # 示例视频 BV 号 (可以修改为你想下载的视频)
    test_bvid = "BV1uv411q7Mv"  # 一个较短的测试视频
    
    print(f"📺 将下载视频: {test_bvid}")
    print("⚠️  注意: 请确保你有权限下载该视频，并遵守相关法律法规")
    
    # 询问用户是否继续
    response = input("\n是否继续下载? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("❌ 用户取消下载")
        return
    
    # 开始下载
    success = await download_video(test_bvid)
    
    if success:
        print("\n🎉 下载任务完成！")
    else:
        print("\n❌ 下载任务失败")

if __name__ == "__main__":
    asyncio.run(main())
