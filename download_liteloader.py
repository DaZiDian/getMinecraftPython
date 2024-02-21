import os
import requests
import hashlib
import json

def download_file(url, filename):
    # 下载文件
    response = requests.get(url)

    # 检查目录是否存在，不存在则创建
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # 将文件保存到硬盘
    with open(filename, 'wb') as file:
        file.write(response.content)

    # 计算文件的SHA-256哈希值
    with open(filename, 'rb') as file:
        bytes = file.read()  # 读取整个文件为字节
        readable_hash = hashlib.sha256(bytes).hexdigest()
        print(f'文件的SHA-256哈希值是: {readable_hash}')
    # 将哈希值保存到一个文件中
    with open(filename + '.txt', 'w') as file:
        file.write(readable_hash)

def download_liteloader_versions():
    # 下载并解析 JSON 文件
    response = requests.get('http://dl.liteloader.com/versions/versions.json')
    liteloader_data = json.loads(response.text)

    # 确保版本信息存在且是一个字典
    if 'versions' in liteloader_data and isinstance(liteloader_data['versions'], dict):
        # 遍历所有版本
        for version, version_info in liteloader_data['versions'].items():
            print(f"正在下载版本 {version}...")

            # 获取版本详细信息
            if 'repo' in version_info and 'url' in version_info['repo']:
                repo_url = version_info['repo']['url']

                # 创建版本号文件夹
                version_folder = os.path.join('./versions/LiteLoader', version)
                os.makedirs(version_folder, exist_ok=True)

                # 下载并保存 jar 文件
                jar_filename = f"{version}.jar"
                download_file(f"{repo_url}/{jar_filename}", os.path.join(version_folder, jar_filename))

                # 下载并保存校验和文件（假设存在）
                if 'checksum' in version_info and 'url' in version_info['checksum']:
                    checksum_filename = f"{version}.checksum"
                    download_file(f"{repo_url}/{version_info['checksum']['url']}", os.path.join(version_folder, checksum_filename))
                else:
                    print(f"版本 {version} 没有校验和文件。")
            else:
                print(f"版本 {version} 的信息中缺少 'repo' 字段或 'url' 字段。")
    else:
        print("版本信息不是一个字典。")

if __name__ == "__main__":
    download_liteloader_versions()
