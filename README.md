# B站视频下载器

这是一个用于下载B站视频的Python脚本，使用yt-dlp库实现。

## 功能特性

- 自动下载B站视频（最高1080p质量）
- 下载中文字幕
- 显示下载进度
- 保存视频信息
- 错误处理和日志记录
- 自动安装依赖

## 安装依赖

### 方法1：使用requirements.txt
```bash
pip install -r requirements.txt
```

### 方法2：手动安装
```bash
pip install yt-dlp
```

## 使用方法

### 直接运行脚本
```bash
python bilibili_downloader.py
```

脚本会自动下载指定的B站视频到 `./downloads` 目录。

### 修改下载URL

如果需要下载其他视频，请编辑 `bilibili_downloader.py` 文件中的 `video_url` 变量：

```python
video_url = "你的B站视频URL"
```

## 输出文件

下载完成后，会在 `downloads` 目录中生成以下文件：
- 视频文件（.mp4格式）
- 字幕文件（.srt格式）
- 视频信息文件（.info.json格式）
- 下载日志（download.log）

## 注意事项

1. 请确保网络连接稳定
2. 某些视频可能需要登录才能下载
3. 请遵守B站的使用条款和版权规定
4. 下载的视频仅供个人学习使用

## 故障排除

如果遇到下载失败，请检查：
1. 网络连接是否正常
2. 视频URL是否有效
3. 是否有足够的磁盘空间
4. 查看 `download.log` 文件获取详细错误信息

## 依赖说明

- **yt-dlp**: 强大的视频下载工具，支持多个视频网站
- **requests**: HTTP库，用于网络请求

## 许可证

本项目仅供学习和研究使用。