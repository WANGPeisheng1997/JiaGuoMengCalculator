# JiaGuoMengCalculator
#### 家国梦建筑最优化计算器(2019.10.3更新)

##### 当前最新版本：V2.0 Beta 2



## 功能：

- 按照当前的建筑星级、等级、各项加成枚举计算收益最高的建筑排布
- 按照现有的金钱余额贪心搜索最佳的升级方案（即将更新）
- 可视化界面随时保存并读取建筑的各项信息以及计算的结果



## 界面截图：

![](/screenshot.png)



## 使用方法：

- #### 发布版：

  百度网盘链接：[点击下载](https://pan.baidu.com/s/1DMN2axXw-Pvf-ltf3b9niA)

  提取码：zchw 

  打开**main.exe**即可畅享所有功能

  填入所有建筑的星级、等级以及各项加成，**将未解锁或作用非常小的建筑加入黑名单（建议至少将7个建筑加入黑名单）**，随后点击**保存并计算最优排布**按钮

  

- #### 源代码版：
	
	1. 在github页面右上角找到clone or download，点击download ZIP将源代码下载到本地并解压（顺便可以点击一下star支持一下我哦）
	
	2. 访问[python官网](https://www.python.org/downloads/windows/)下载python
	
	3. 在导航栏中依次点击Downloads----Windows
	
	4. 在Stable Releases条目下选择最新版的windows安装程序（后缀executable installer）下载（32位64位自行选择）
	
	5. 安装首页勾选 Add Python to Path 点击Install Now（推荐）或自定义路径

	6. 打开cmd，输入python -V，出现版本号为安装成功
	
	7. （安装依赖模块之方法一）在cmd中输入`python -m pip install --user numpy scipy tqdm pandas pyqt5`
	
	8. （安装依赖模块之方法二）在解压后的源代码文件夹中打开cmd（在顶部导航栏输入cmd即可），然后输入`pip install requirements.txt`
	
	9. 在解压后的源代码文件夹中打开cmd，输入`python main.py`
	
	   
	
- #### 可能出现的问题

  出现类似:`ModuleNotFoundError: No module named 'XXX'`的提示，参照环境搭建第七条输入`python -m pip install --user XXX`安装依赖模块

  **界面卡死可能是运算能力不够，请将更多建筑加入黑名单，或者耐心等待**

  默认黑名单下，需要约15-45秒计算时间（取决于电脑的性能）

  黑名单建筑数量达到10个左右时，则只需要约5-15秒计算时间（取决于电脑的性能）

  所有加成均填写在游戏内实际显示的数值，如游戏内增加200%就填写200%

  不需要或未解锁的建筑星级和等级**不要填写成0**，家国之光与国庆100%的buff**加起来**填写在政策加成中

  

## 作者：

- 本项目由我（nga: 温火融冰）和校友SQRPI（nga: 根派）合作完成

- SQRPI的后端源代码工程在：[点击访问](https://github.com/SQRPI/JiaGuoMeng)，大家不要忘记去支持一下点个star哦！

- SQRPI的nga原帖链接：[写了个计算建筑摆放最优策略的脚本](https://bbs.nga.cn/read.php?tid=18677204)

- 公式参考：[单建筑收益公式及一些tips](https://bbs.nga.cn/read.php?tid=18675554)

- 数据来源：[[攻略] 建筑收益及升级消耗数据](https://nga.178.com/read.php?tid=18741305)
- 另外关于火车机制的测评可以参考我在nga发布的攻略贴[[攻略] 火车机制探索与数据测试](https://nga.178.com/read.php?tid=18729321)
- 感谢一起参与修bug、提供数据、发布综述以及给我们点star的朋友们，你们的支持就是我们最大的动力！



## 更新记录：

2019.10.3更新：

- Ver 2.0 Beta 2 星级输入修改成SpinBox，界面更新金币和模式框（下版本实装）
- Ver 2.0 Beta 1 增加了黑名单功能，修复了不点击保存直接计算会闪退的bug
- Ver 1.2 修复了打开后闪退的bug
- Ver 1.1修复了发布版打不开exe的bug

2019.10.2更新：

- Ver 1.0 发布源代码版本

