import os
import requests
import hashlib
import json

def download_file(url, filename):
    # 检查文件是否已经存在
    if os.path.exists(filename):
        print(f"文件 {filename} 已经下载.")
        return

    # 下载文件
    response = requests.get(url)

    # 创建文件的目录
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # 将文件保存到硬盘
    with open(filename, 'wb') as file:
        file.write(response.content)

    # 计算文件的SHA-256哈希值
    with open(filename, 'rb') as file:
        bytes = file.read() # 读取整个文件为字节
        readable_hash = hashlib.sha256(bytes).hexdigest()
        print(f'文件的SHA-256哈希值是: {readable_hash}')

    # 将哈希值保存到一个文件中
    with open(filename + '.txt', 'w') as file:
        file.write(readable_hash)

def download_minecraft_versions():
    # 下载并解析JSON文件
    response = requests.get('http://launchermeta.mojang.com/mc/game/version_manifest.json')
    version_manifest = json.loads(response.text)

    # 遍历所有的版本
    for version_info in version_manifest['versions']:
        print(f"正在下载版本 {version_info['id']}...")
        # 获取每个版本的详细信息
        response = requests.get(version_info['url'])
        version_detail = json.loads(response.text)
        # 下载jar文件
        download_file(version_detail['downloads']['server']['url'], f'minecraft/versions/{version_info["id"]}/{version_info["id"]}.jar')

def download_fabric_versions():
    # 下载并解析JSON文件
    response = requests.get('https://meta.fabricmc.net/v2/versions/loader')
    fabric_versions = json.loads(response.text)

    # 遍历所有的版本
    for version_info in fabric_versions:
        print(f"正在下载Fabric版本 {version_info['version']}...")
        # 获取每个版本的详细信息
        response = requests.get(version_info['stable'][-1]['url'])
        version_detail = json.loads(response.text)
        # 下载jar文件
        download_file(version_detail['downloads']['server']['url'], f'fabric/versions/{version_info["version"]}/{version_info["version"]}.jar')

if __name__ == "__main__":
    download_minecraft_versions()
    download_fabric_versions()
