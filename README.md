# 说明

- 本项目是一些自己编写的生信脚本，还在不断完善中

# Python脚本

## 环境安装

- 单独安装：可以独立安装对应脚本中用到的模块，直接看Pipfile最上面导入的模块即可
- 统一安装
    - 使用pipenv安装所有脚本需要的模块
        - `pip install pipenv`
        - `pipenv install`
    - 使用poetry管理
        - `pip install poetry`
        - `conda activate env_name`
        - `poetry install`
        - poetry环境安装文件参考：<https://github.com/diklios5768/Algorithm>

## 脚本说明

### tools:真正使用的脚本

- ncbi:NCBI数据库接口调用，只需要根据官方文档中提供的参数改写相应的函数即可
    - snp.py: 获取snp信息
        - 脚本是根据基因名称获得snp
        - 后续会扩展为拥有各式各样的数据库和查询条件
        - 后续会使用命令行输入和配置文件共用的形式给与方便简单的调用
- fastq
    - compare.py：比对双端的fastq文件每四行的key（或者叫id）是否一一对应
    - filter.py：过滤掉fastq文件中的符合过滤规则的部分
- encode:爬取encode数据库和下载相应文件的脚本
- wes：遗传相关的脚本

### utils:通用工具

# R语言脚本

## 环境安装

- 建议使用conda

```shell
# 必须先在conda的base环境下面安装一个R，解决jetbrains的R语言插件选择解释器的时候依赖问题
# 也可以参考这篇文章解决：https://zhuanlan.zhihu.com/p/546788455，但是比较麻烦
# 注意r和conda-forge两个channel的R语言版本是不一样的，如果需要UTF8编码，必须是4.2.0以上，但是目前两个都没有Windows 64的4.2.0以上版本提供
conda install -c r r-base -y
# 或者 conda install -c conda-forge r-base -y
# 然后就可以创建新的环境进行使用 
conda create -n bio python=3.10 -y
conda activate bio
conda install jupyterlab -y
conda install jupyter notebook -y
# 使用jetbrains的IDE时，由于很多情况下，IDE或者插件不是最新版本，R环境最好是4.1（不包含）以下，能够解决控制台的字符集警告问题：Warning in (function (file = "", n = NULL, text = NULL, prompt = "?", keep.source = getOption("keep.source"), :argument encoding="UTF-8" is ignored in MBCS locales
# 还能够解决图片不在工具包的图展示栏里，而是保存为了PDF文件的问题
conda install -c r r-base=4.0.5 -y
#安装R的jupyter内核
conda insyall -c r r-irkernel -y
```

- 如果Python包conda装不了就用pip安装
- 如果Pycharm提示下载索引或者补全包尽量全部下载

## 创建R语言内核ipynb文件

- 只能通过jupyter选择R内核进行创建，Pycharm目前没有找到方法手动切换到R内核
- 启动jupyter：`jupyter lab`或者`jupyter notebook`

## UTF8编码问题（不使用Rstudio的时候会遇到，但Rstudio其实也没有解决这个问题，只是他进行了转码让所有的程序都能正常运行）

- 一般在使用中文的时候会遇到，不使用中文可以不用关注
- R4.2.0之前无法彻底解决，建议还是使用Rstudio，别浪费时间
    - conda目前没有哪个channel提供Windows64的4.2.0版本，只能自己手动下载
    - 使用了R4.2.0，必须先开启**Windows 系统需要开启utf8支持（实仍然是验性特性）**
    - 更新Pycharm 2022.2版本并安装最新的R语言插件，否则可能会有很多错误
    - 参考：<https://www.zhihu.com/question/47618253/answer/2482936156>
- jetbrains IDE的R语言插件画图中文不显示
    - 图形不使用IDE模式，本身显示中文
    - 黑边需要关闭黑夜模式
    // 
    - 不需要showtext加载字体，会变得很粗