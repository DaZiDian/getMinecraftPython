import os
import requests
import hashlib


def get_optifine_files():
    url = "https://optifine.cn/api"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get("files", [])
    else:
        print(f"获取OptiFine文件信息失败。状态码：{response.status_code}")
        return []


def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def download_optifine_file(file_info):
    file_name = file_info['name']
    version = file_info['version']
    download_url = f"https://optifine.cn/download/{file_name}"
    response = requests.get(download_url)

    if response.status_code == 200:
        directory = f"versions/Optifine/{version}"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, file_name)
        with open(file_path, 'wb') as f:
            f.write(response.content)

        md5_value = calculate_md5(file_path)
        with open(os.path.join(directory, "md5.txt"), 'a') as f:
            f.write(f"{file_name}: {md5_value}\n")

        print(f"下载文件 {file_name} 成功！")
    else:
        print(f"下载文件 {file_name} 失败。状态码：{response.status_code}")


if __name__ == "__main__":
    optifine_files = get_optifine_files()

    if optifine_files:
        for file_info in optifine_files:
            download_optifine_file(file_info)
    else:
        print("没有找到OptiFine文件。")
