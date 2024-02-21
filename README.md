# 使用 Python 脚本 获取 Minecraft 官方源中的文件

## 依赖安装：

```Python
pip install requests
```

## 运行脚本:

```Python
python <Python文件名>.py
```

或者如果你使用的是 Python 3：

```Python
python3 <Python文件名>.py
```

如果你的服务器需要身份验证或使用特定的协议，你可能需要修改请求头或其他网络相关的信息。此项目中，请求是通过 HTTP GET 进行的，没有特殊的头信息。

如果你的服务器需要身份验证，可以在请求中添加相应的头信息。例如，如果需要添加用户代理信息，你可以修改请求头：

```
pythonCopy codeheaders = {
    'User-Agent': 'Your User Agent',
}

response = requests.get(version_info_url, headers=headers)
```

## 举个例子

### download_liteloader.py

```Python
# 创建版本号文件夹
version_folder = os.path.join('./versions/LiteLoader', version)
os.makedirs(version_folder, exist_ok=True)
# 下载并保存 jar 文件
jar_filename = f"{version}.jar"
download_file(f"{repo_url}/{jar_filename}", os.path.join(version_folder, jar_filename))
```

在此处，我默认将所有 Liteloader 文件存放到本项目 versions/Liteloader 文件夹中，如果你有其他需要，可以自定义该路径。例如，我想让他存放到服务器根目录下的 download_liteloader 文件夹，我就需要将

```python
version_folder = os.path.join('./versions/LiteLoader', version)
```

单引号的内容改为 '/download_liteloader' ，最后该行代码就像这样:

```python
version_folder = os.path.join('/download_liteloader', version)
```

而后面的 version 则代表了不同版本。例如我下载了一个liteloader 1.5.2版本，于是我的文件会被存放到 “/download_liteloader/1.5.2” 文件夹中，这个文件夹中也会存放 jar 本体以及 校验和文件

紧接着，为了确保文件的安全性和真实性，我引用了 Python 中的 hashlib 库，来计算文件的哈希值，哈希值算法为SHA-256

```python
# 计算文件的SHA-256哈希值
    with open(filename, 'rb') as file:
        bytes = file.read()  # 读取整个文件为字节
        readable_hash = hashlib.sha256(bytes).hexdigest()
        print(f'文件的SHA-256哈希值是: {readable_hash}')
    # 将哈希值保存到一个文件中
    with open(filename + '.txt', 'w') as file:
        file.write(readable_hash)
```

这里就是计算哈希值的代码块，当然，如果你不需要它们，除了将这段计算删除掉外，还需要将下面的下载并保存校验和文件模块删除

```python
# 下载并保存校验和文件（假设存在）
                if 'checksum' in version_info and 'url' in version_info['checksum']:
                    checksum_filename = f"{version}.checksum"
                    download_file(f"{repo_url}/{version_info['checksum']['url']}", os.path.join(version_folder, checksum_filename))
                else:
                    print(f"版本 {version} 没有校验和文件。")
```

其他文件的结构都与之类似，这里不做任何阐述。

## 注意

需要注意的是，由于我们使用 解析JSON 的方法来获取信息，所以每个文件中几乎都包含了

```python
def download_xxx_versions():
    response = requests.get('http://launchermeta.mojang.com/mc/game/version_manifest.json')
    version_manifest = json.loads(response.text)
```

这一段语句适用于获取了明确的 JSON 文件链接，但如同 Optifine 这种没有给出明确 JSON 文件地址，但是官方给出了 API文档 ，我们就需要仔细查阅文档，并且用另外一种方式来解析。

例如，Optifine API文档 中提供给我们一个示例

请求示例：

```http
GET https://optifine.cn/download/OptiFine_1.10.2_HD_U_C1.jar
```

其中的 OptiFine_1.10.2_HD_U_C1.jar 就代表了文件名称。

然后我们再翻阅 https://optifine.cn/api 这个链接中的 JSON 文档，其中有 versions，代表了所有支持的游戏版本。files 中，也有 name、md5、time、version 这四个键值。反映到代码中，我们是这样利用的

```python
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
```

当然，BMCLAPI 也为我们提供了一套调用标准，你也可以根据这些来修改文件中的解析方法。

```http
https://bmclapi2.bangbang93.com/optifine/:mcversion/:type/:patch
```

| 字段      | 类型   | 描述                                                         |
| :-------- | :----- | :----------------------------------------------------------- |
| mcversion | String | mc版本                                                       |
| type      | String | optifine的种类，不过从bmclapi2开始提供optifine开始，似乎只能下载到OptiFine HD Ultra这一个类型了，所以 这里应该会一直保持为HD_U |
| patch     | String | optifine的补丁版本号，就是后面常见的A1A2,B1B2和C1C2之类的    |

(302) 跳转下载地址

```json
HTTP/1.1 302 Redirect
```

(404) 没有找到匹配的optifine

```json
{
    "msg": "no such optifine"
}
```

## One More Thing……

如果你喜欢本项目，麻烦点一个star（，也希望大佬能够多多指点。如果你在使用过程中遇到了问题，请确认不是自己的问题之后，再提交issue。

更多的内容会持续更新，敬请期待……
