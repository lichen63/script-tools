import os

def remove_z_library_suffix(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if "(Z-Library)" in file_name:
                old_path = os.path.join(root, file_name)
                new_name = file_name.replace(" (Z-Library)", "").strip()
                new_path = os.path.join(root, new_name)
                
                os.rename(old_path, new_path)
                print(f'Renamed: {file_name} -> {new_name}')

if __name__ == "__main__":
    folder_path = "/Users/lichenliu/Library/Mobile Documents/com~apple~CloudDocs/EngFiction"
    remove_z_library_suffix(folder_path)
