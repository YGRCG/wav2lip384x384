import os
import sys

def batch_rename(directory='./raw_data', sort_by='name'):
    """
    批量重命名目录中的文件为顺序编号格式（如00001, 00002）
    
    :param directory: 目标目录路径
    :param sort_by: 排序方式 ('name'按文件名, 'time'按修改时间)
    """
    # 获取文件列表（排除目录）
    files = [f for f in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, f))]
    
    if not files:
        print("错误：目录中没有可重命名的文件")
        return

    # 文件排序
    if sort_by == 'name':
        files.sort()
    elif sort_by == 'time':
        files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    else:
        files.sort()  # 默认按文件名排序

    total_files = len(files)
    # 计算编号位数（至少5位）
    total_digits = max(5, len(str(total_files)))

    # 生成新文件名列表
    new_names = []
    for i in range(total_files):
        ext = os.path.splitext(files[i])[1]  # 保留原始扩展名
        new_name = f"{str(i+1).zfill(total_digits)}{ext}"
        new_names.append(new_name)

    # 检查文件名冲突
    existing_files = set(os.listdir(directory))
    conflicts = set(new_names) & (existing_files - set(files))
    if conflicts:
        print(f"错误：以下文件名已存在，请先移除：{', '.join(conflicts)}")
        return

    # 倒序重命名（避免覆盖问题）
    print(f"开始重命名 {total_files} 个文件...")
    for i in range(total_files-1, -1, -1):
        old_path = os.path.join(directory, files[i])
        new_path = os.path.join(directory, new_names[i])
        try:
            os.rename(old_path, new_path)
            print(f"✓ {files[i]} → {new_names[i]}")
        except Exception as e:
            print(f"✕ 重命名失败 {files[i]}: {str(e)}")
    
    print("操作完成！")

if __name__ == '__main__':

    print("默认处理 ./raw_data目录下文件")
    print("示例: python rename.py [/path/to/folder] [sort_type]")
    print("可选排序方式: name (默认), time (按修改时间)")

   
    batch_rename()