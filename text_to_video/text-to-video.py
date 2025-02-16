import re
import textwrap
from PIL import Image, ImageDraw, ImageFont
import moviepy as mpy
import edge_tts
import asyncio
import os
import numpy as np

# 配置参数
CONFIG = {
    "input_md": "input.md",  # 输入的 markdown 文件路径
    "output_mp4": "output.mp4",  # 输出的视频文件路径
    "font_path": "SourceHanSansSC-Regular.otf",  # 字体文件路径
    "font_size": 24,  # 字体大小
    "bg_color": (0, 0, 0),  # 背景颜色（黑色）
    "text_color": (255, 255, 255),  # 字体颜色（白色）
    "resolution": (1280, 720),  # 视频分辨率
    "margin": 80,  # 边距
    "fps": 24,  # 帧率
    "tts_voice": "zh-CN-XiaoxiaoNeural",  # Edge TTS 中文女声
    "tts_rate": "+20%",  # 语速加快 20%
}

async def generate_tts(text, audio_path):
    """使用 edge-tts 生成语音并保存"""
    tts = edge_tts.Communicate(text, CONFIG["tts_voice"], rate=CONFIG["tts_rate"])
    await tts.save(audio_path)

def process_markdown():
    """处理Markdown并生成分段文本和音频"""
    with open(CONFIG["input_md"], "r", encoding="utf-8") as f:
        text = f.read()
    
    # 清理Markdown语法，保留链接文本部分
    patterns = [
        r'#{1,6}\s*',  # 标题
        r'!\[.*?\]\(.*?\)',  # 图片
        r'`{3}.*?`{3}',  # 代码块
        r'[-\*]{3,}',  # 横线
        r'`(.*?)`',  # 行内代码
        r'^\s*[\-\*\+]\s+',  # 列表项
        r'>\s*',  # 引用
        r'\[([^\]]+)\]\(.*?\)'  # 链接，保留文本部分
        r'(\*\*|\*)\s*(.*?)\s*(\*\*|\*)',  # 去除加粗或斜体的 *
        r'(__|_)\s*(.*?)\s*(__|_)'  # 去除加粗或斜体的 _
    ]
    
    # 替换掉链接URL部分，只保留链接文本
    text = re.sub(r'\[([^\]]+)\]\(.*?\)', r'\1', text)

    # 去除加粗和斜体的 * 和 _
    text = re.sub(r'(\*\*|\*)\s*(.*?)\s*(\*\*|\*)', r'\2', text)
    text = re.sub(r'(__|_)\s*(.*?)\s*(__|_)', r'\2', text)

    # 清理其他Markdown部分
    clean_text = re.sub('|'.join(patterns), '', text, flags=re.DOTALL|re.MULTILINE)
    
    # 分段处理
    paragraphs = [p.strip() for p in clean_text.split('\n\n') if p.strip()]
    
    # 生成TTS音频
    audio_clips = []
    tasks = []
    for idx, para in enumerate(paragraphs):
        audio_path = f"temp_audio_{idx}.mp3"
        tasks.append(generate_tts(para, audio_path))
    
    # 异步生成音频
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))

    # 加载音频
    for idx in range(len(paragraphs)):
        audio_path = f"temp_audio_{idx}.mp3"
        audio_clips.append(mpy.AudioFileClip(audio_path))
    
    return paragraphs, audio_clips

def create_text_image(text):
    """创建居中排版的文字图片"""
    font = ImageFont.truetype(CONFIG["font_path"], CONFIG["font_size"])
    img = Image.new("RGB", CONFIG["resolution"], CONFIG["bg_color"])
    draw = ImageDraw.Draw(img)
    
    # 计算最大文本区域
    max_width = CONFIG["resolution"][0] - 2 * CONFIG["margin"]
    max_height = CONFIG["resolution"][1] - 2 * CONFIG["margin"]
    
    # 自动换行处理
    lines = []
    for line in text.split('\n'):
        wrapped = textwrap.wrap(line, width=40)
        lines.extend(wrapped)
    
    # 计算总文本高度
    line_heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
    total_height = sum(line_heights) + 10 * (len(lines)-1)
    
    # 垂直居中起始位置
    y = (CONFIG["resolution"][1] - total_height) // 2
    
    # 绘制每行文字
    for line, line_height in zip(lines, line_heights):
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        x = (CONFIG["resolution"][0] - text_width) // 2
        draw.text((x, y), line, font=font, fill=CONFIG["text_color"])
        y += line_height + 10
    
    return np.array(img)

def generate_video():
    """生成完整视频"""
    paragraphs, audio_clips = process_markdown()
    
    video_clips = []
    for para, audio in zip(paragraphs, audio_clips):
        img = create_text_image(para)
        clip = mpy.ImageClip(img).with_duration(audio.duration).with_audio(audio)
        video_clips.append(clip)
    
    final_clip = mpy.concatenate_videoclips(video_clips)
    
    final_clip.write_videofile(
        CONFIG["output_mp4"],
        fps=CONFIG["fps"],
        codec="libx264",
        audio_codec="aac",
        threads=4
    )
    
    # 清理临时文件
    for clip in audio_clips:
        clip.close()
    for i in range(len(paragraphs)):
        os.remove(f"temp_audio_{i}.mp3")

if __name__ == "__main__":
    generate_video()