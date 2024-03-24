import os
import requests
from tqdm import tqdm
from urllib.parse import urlparse, urljoin

def get_forge_versions(minecraft_version):
    url = f"https://bmclapi2.bangbang93.com/forge/minecraft/{minecraft_version}"
    response = requests.get(url)
    if response.ok:
        versions = response.json()
        return versions
    else:
        print("获取Forge版本失败")
        return None

def get_existing_forge_versions(subfolder):
    existing_versions = set()
    for root, dirs, files in os.walk(subfolder):
        for file in files:
            if file.startswith("forge-") and file.endswith("-installer.jar"):
                version = file.split("-")[2]
                existing_versions.add(version)
    return existing_versions

def download_forge_installer(minecraft_version, forge_version, subfolder):
    url = f"https://bmclapi2.bangbang93.com/forge/download"
    params = {
        "mcversion": minecraft_version,
        "version": forge_version,
        "category": "installer",
        "format": "jar"
    }
    response = requests.get(url, params=params)
    if response.ok:
        download_url = response.url
        print(f"重定向链接: {download_url}")
        filename = f"forge-{minecraft_version}-{forge_version}-installer.jar"
        download_url = urljoin(download_url, filename)
        print(f"下载链接: {download_url}")
        response_download = requests.get(download_url, stream=True)
        if response_download.ok:
            if not os.path.exists(subfolder):
                os.makedirs(subfolder)
            filepath = os.path.join(subfolder, filename)
            total_size = int(response_download.headers.get('content-length', 0))
            with open(filepath, 'wb') as file, tqdm(
                desc=filename,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response_download.iter_content(chunk_size=1024):
                    size = file.write(chunk)
                    bar.update(size)
            print(f"{filepath} 下载成功。")
        else:
            print(f"下载Forge安装器失败：{download_url}")
    else:
        print(f"获取Forge下载链接失败：{url}")

minecraft_version = "1.20.1"  # 此处输入您要下载的Minecraft版本
versions = get_forge_versions(minecraft_version)
if versions:
    subfolder = f"versions/Forge/{minecraft_version}"
    existing_versions = get_existing_forge_versions(subfolder)
    for version_info in versions:
        forge_version = version_info['version']
        if forge_version not in existing_versions:
            download_forge_installer(minecraft_version, forge_version, subfolder)
        else:
            print(f"版本 {forge_version} 已存在，跳过下载。")
else:
    print(f"{minecraft_version} 版本没有找到Forge版本。")
