from urllib import request, error


def get_latest_version():
    url = "https://github.com/WANGPeisheng1997/JiaGuoMengCalculator"
    try:
        wp = request.urlopen(url)
        content = wp.read().decode()
    except error.HTTPError:
        print("网络连接错误，无法获取到最新版本")
        return "无法获取到最新版本"
    except error.URLError:
        print("网络连接错误，无法获取到最新版本")
        return "无法获取到最新版本"
    else:
        pos = content.find("当前最新版本：")
        if pos == -1:
            print("无法找到最新版本")
            return "无法获取到最新版本"
        else:
            version_rough = content[pos:pos + 100]
            version = version_rough.split("</h5>")[0]
            return version


get_latest_version()
