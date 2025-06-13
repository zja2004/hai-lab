#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站视频下载器
使用yt-dlp库下载B站视频
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('download.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """检查并安装必要的依赖"""
    try:
        import yt_dlp
        logger.info("yt-dlp 已安装")
        return True
    except ImportError:
        logger.info("正在安装 yt-dlp...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            logger.info("yt-dlp 安装成功")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"安装 yt-dlp 失败: {e}")
            return False

def download_bilibili_video(url, output_dir="./downloads"):
    """下载B站视频"""
    try:
        import yt_dlp
        
        # 创建下载目录
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 配置下载选项
        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # 尝试更通用的格式
            'writesubtitles': True,  # 下载字幕
            'writeautomaticsub': True,  # 下载自动字幕
            'subtitleslangs': ['zh-CN', 'zh-Hans'],  # 中文字幕
            'ignoreerrors': True,
            'no_warnings': False,
            'extractaudio': False,
            'audioformat': 'mp3',
            'embed_subs': True,
            'writeinfojson': True,  # 保存视频信息
        }
        
        # 添加进度钩子
        def progress_hook(d):
            if d['status'] == 'downloading':
                percent = d.get('_percent_str', 'N/A')
                speed = d.get('_speed_str', 'N/A')
                logger.info(f"下载进度: {percent} - 速度: {speed}")
            elif d['status'] == 'finished':
                logger.info(f"下载完成: {d['filename']}")
        
        ydl_opts['progress_hooks'] = [progress_hook]
        
        # 开始下载
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"开始下载视频: {url}")
            ydl.download([url])
            logger.info("视频下载完成！")
            
    except Exception as e:
        logger.error(f"下载失败: {str(e)}")
        return False
    
    return True

def main():
    """主函数"""
    # B站视频URL
    video_url = "https://www.bilibili.com/video/BV1WzTCzcEmu/?share_source=copy_web&vd_source=59b9715f6debaa33c5dd388dcbd5a20a"
    
    # 下载目录
    download_dir = "./downloads"
    
    logger.info("B站视频下载器启动")
    logger.info(f"目标URL: {video_url}")
    logger.info(f"下载目录: {os.path.abspath(download_dir)}")
    
    # 检查依赖
    if not check_dependencies():
        logger.error("依赖检查失败，程序退出")
        return
    
    # 下载视频
    success = download_bilibili_video(video_url, download_dir)
    
    if success:
        logger.info("所有任务完成！")
    else:
        logger.error("下载过程中出现错误")

if __name__ == "__main__":
    main()