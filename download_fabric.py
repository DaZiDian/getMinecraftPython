import os
import requests
import hashlib

# 创建目录
if not os.path.exists('versions/Fabric'):
    os.makedirs('versions/Fabric')

# 获取游戏版本信息
response = requests.get("https://meta.fabricmc.net/v2/versions")
data = response.json()

# 检查'game'键是否存在
if 'game' not in data:
    print(f"没有找到任何游戏版本。响应数据: {data}")
    exit()

# 遍历每个游戏版本
for game_version in data['game']:
    game_version_number = game_version['version']
    print(f"正在处理游戏版本: {game_version_number}")

    # 获取Fabric加载器版本信息
    loader_response = requests.get("https://meta.fabricmc.net/v2/versions/loader")
    loader_data = loader_response.json()

    # 遍历每个加载器版本
    for loader_version in loader_data:
        loader_version_number = loader_version['version']
        print(f"正在处理加载器版本: {loader_version_number}")

        # 选择一个安装器版本（根据实际需求，可能需要调整）
        installer_version_number = "1.0.0"  # 示例值
        print(f"选择的安装器版本: {installer_version_number}")

        # 拼接最终的下载链接
        download_url = f"https://meta.fabricmc.net/v2/versions/loader/{game_version_number}/{loader_version_number}/{installer_version_number}/server/jar"
        print(f"正在从以下地址下载: {download_url}")

        # 下载文件
        file_response = requests.get(download_url)
        if file_response.status_code == 200:
            file_path = f"versions/fabric/{game_version_number}/{loader_version_number}/{installer_version_number}/server.jar"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(file_response.content)
            print(f"成功下载到: {file_path}")

            # 计算md5
            md5 = hashlib.md5()
            md5.update(file_response.content)
            md5_value = md5.hexdigest()

            # 保存md5到txt文件
            with open(f"{file_path}.md5.txt", 'w') as f:
                f.write(md5_value)
            print(f"MD5值为: {md5_value}")
        else:
            print(f"下载失败，状态码: {file_response.status_code}")
