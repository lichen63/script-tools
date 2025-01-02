import os
from PIL import Image

def compress_images(folder_path, quality=80):
    """
    压缩文件夹中的所有图片并保存到 temp 文件夹中。

    :param folder_path: 输入的文件夹路径
    :param quality: 压缩质量，1-100，数值越小，压缩越高，图片越小
    """
    # 创建 temp 文件夹
    temp_folder = os.path.join(folder_path, "temp")
    os.makedirs(temp_folder, exist_ok=True)

    # 支持的图片格式
    supported_formats = (".jpg", ".jpeg", ".png", ".bmp", ".gif")

    for root, dirs, files in os.walk(folder_path):
        # 跳过 temp 文件夹
        if "temp" in dirs:
            dirs.remove("temp")

        for file in files:
            # 跳过目标文件夹中的文件
            if root.startswith(temp_folder):
                continue

            if file.lower().endswith(supported_formats):
                try:
                    # 原图片路径
                    image_path = os.path.join(root, file)
                    
                    # 打开图片
                    img = Image.open(image_path)
                    
                    # 保存到 temp 文件夹
                    temp_path = os.path.join(temp_folder, file)
                    
                    # 压缩并保存
                    img.save(temp_path, quality=quality, optimize=True)
                    print(f"压缩完成: {file} -> {temp_path}")
                except Exception as e:
                    print(f"跳过 {file}: {e}")

    print(f"所有图片已保存到: {temp_folder}")

# 示例调用
if __name__ == "__main__":
    folder = input("请输入文件夹路径: ")
    compress_quality = int(input("请输入压缩质量 (1-100，推荐80): "))
    compress_images(folder, compress_quality)