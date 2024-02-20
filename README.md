# 使用 Python 脚本 获取 Minecraft 官方源中的文件

## 依赖安装：

```Python
pip install requests
```

## 运行脚本:

```Python
python download_game_version.py
```

或者如果你使用的是 Python 3：

```Python
python3 download_game_version.py
```

## 自定义内容

1. **文件路径：**

   ```
   pythonCopy code# 创建版本目录
   version_directory = os.path.join("/path/to/your/server/versions", latest_version)
   ```

   将 `"/path/to/your/server/versions"` 替换为你存储游戏版本的目录的实际路径。确保你有写入权限，并且该目录存在。

2. **服务器信息：**

   如果你的服务器需要身份验证或使用特定的协议，你可能需要修改请求头或其他网络相关的信息。此项目中，请求是通过 HTTP GET 进行的，没有特殊的头信息。

   如果你的服务器需要身份验证，可以在请求中添加相应的头信息。例如，如果需要添加用户代理信息，你可以修改请求头：

   ```
   pythonCopy codeheaders = {
       'User-Agent': 'Your User Agent',
   }
   
   response = requests.get(version_info_url, headers=headers)
   ```
