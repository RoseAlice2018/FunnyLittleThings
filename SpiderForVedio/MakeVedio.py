import os
import subprocess
import threading
import m3u8
import m3u8_To_MP4

## step1 读取文件的标题 根据文件的vodname 创建文件夹（如果不存在文件夹的情况下）
## step2 读取文件内容的m3u8地址
## step3 根据m3u8 地址 下载mp4 然后存储到对应的文件中
## step4 因为单个下载速度太慢实现并行下载
## step5 import m3u8tomp4 库来处理

def create_folder(vodname):
    # check if already exist
    if not os.path.exists(vodname):
        os.makedirs(vodname)
        print(f"create folder: {vodname}")
    else:
        print(f"alreay exist: {vodname}")

def readfile_in_subdir():
    # 获取File子文件夹
    subfolders = [f.path for f in os.scandir('.') if f.is_dir() and f.name == 'FileTest']

    for subfolder in subfolders:
        file_paths = [f.path for f in os.scandir(subfolder) if f.is_file]

        for file_path in file_paths:
            # 读取文件内容
            with open(file_path, 'r') as file:
                content = file.read()

            # 获取文件名
            file_name = os.path.basename(file_path)

            # 获取vodname
            parts = file_name.split(' ')
            vodname = parts[0]
            create_folder(vodname)

            # convert to mp4
            convert_m3u8_to_mp4(content, vodname, file_name)

def download_segment(url, output_file):
    command = f"ffmpeg -i {url} -c copy -bsf:a aac_adtstoasc -y {output_file}"
    subprocess.call(command, shell=True)

def parallel_download_m3u8(m3u8_url, output_file):
    playlist = m3u8.load(m3u8_url)
    segments = playlist.segments
    print(output_file)

    threads = []
    for i, segment in enumerate(segments):
        segment_url = segment.absolute_uri
        thread = threading.Thread(target=download_segment, args=(segment_url, f"segment_{i}.ts"))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    command = f"ffmpeg -i concat:{'|'.join([f'segment_{i}.ts' for i in range(len(segments))])} -c copy -bsf:a aac_adtstoasc -y {output_file}"
    subprocess.call(command)
    for i in range(len(segments)):
        os.remove(f"segment_{i}.ts")

def convert_m3u8_to_mp4(m3u8_url, output_folder, filename):
    # 确保输出的文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 构建输出文件路径
    print(m3u8_url)
    print(output_folder)
    print(filename)
    #output_file = os.path.join(output_folder, 'aaa.mp4')

    #ffmpeg.input(m3u8_url).output(output_file).run()
    #subprocess.call(['ffmpeg', '-i', m3u8_url, '-c', 'copy', output_file, '-stats'])
    #parallel_download_m3u8(m3u8_url, output_file)
    m3u8_To_MP4.multithread_download(m3u8_url, mp4_file_dir=output_folder, mp4_file_name=filename)

readfile_in_subdir()