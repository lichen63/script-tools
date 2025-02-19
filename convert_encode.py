import os
import chardet

# 删除所有 _temp 结尾的文件
def remove_temp_files(folder_path):
    print("开始删除 _temp 结尾的文件...")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('_temp.txt'):
                temp_file_path = os.path.join(root, file)
                try:
                    os.remove(temp_file_path)
                    print(f"已删除临时文件: {temp_file_path}")
                except Exception as e:
                    print(f"删除文件 {temp_file_path} 失败: {e}")

# 检测文件编码
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

# 去除 UTF-8 BOM
def remove_bom(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    if content[:3] == b'\xef\xbb\xbf':  # 检测 BOM
        print(f"检测到 BOM，移除 BOM...")
        content = content[3:]
        with open(file_path, 'wb') as file:
            file.write(content)
        print(f"BOM 移除成功。")

# 转换为 UTF-8 编码
def convert_to_utf8(file_path):
    temp_name = file_path[:-4] + '_temp.txt'
    encoding = detect_encoding(file_path)
    
    print(f"检测文件: {file_path}")
    if encoding is None:
        print(f"无法检测文件编码: {file_path}，尝试使用 GB18030 作为默认编码")
        encoding = 'GB18030'
    else:
        print(f"文件编码: {encoding}")
    
    # 如果文件是 UTF-8-SIG，先去除 BOM
    if encoding.lower() == 'utf-8-sig':
        remove_bom(file_path)
        encoding = 'utf-8'

    if encoding.lower() != 'utf-8':
        try:
            print(f"将文件 {file_path} 转换为 UTF-8 格式...")
            # 使用 iconv 并添加 -c 选项来跳过非法字符
            os.system(f"iconv -f {encoding} -t UTF-8 -c {file_path} > {temp_name}")
            print(f"转换成功，临时文件: {temp_name}")
            
            # 检测转换后文件的大小
            source_size = os.path.getsize(file_path)
            temp_size = os.path.getsize(temp_name)
            
            print(f"源文件大小: {source_size} 字节，临时文件大小: {temp_size} 字节")
            
            # 如果转换后的文件大小大于源文件，移除源文件并重命名
            if temp_size > source_size:
                print(f"临时文件大于源文件，移除源文件并重命名临时文件...")
                os.remove(file_path)  # 删除源文件
                os.rename(temp_name, file_path)  # 重命名临时文件
                print(f"重命名成功: {temp_name} -> {file_path}")
            else:
                print(f"临时文件大小不大于源文件，保留两个文件。")
        except Exception as e:
            print(f"转换失败: {e}")
    else:
        print(f"文件 {file_path} 已经是 UTF-8 编码，无需转换。")

# 处理文件夹中的所有文件
def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                convert_to_utf8(file_path)

if __name__ == "__main__":
    folder = input("Please enter the folder path: ")
    
    # 前置步骤：删除所有 _temp 结尾的文件
    remove_temp_files(folder)
    
    # 执行文件转换
    process_folder(folder)