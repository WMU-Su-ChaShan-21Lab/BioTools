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

```shell
# 必须先在conda的base环境下面安装一个R，解决jetbrains的R语言插件选择解释器的时候依赖问题
conda install -c r r-base -y
# 然后就可以创建新的环境进行使用 
conda create -n bio python=3.10 -y
conda activate bio
conda install jupyterlab -y
conda install jupyter notebook -y
conda install -c r r-base=4.0.5 -y
conda insyall -c r r-irkernel -y
```

如果Python包conda装不了就用pip安装
如果Pycharm提示下载索引或者补全包尽量全部下载

## 创建R语言内核脚本

只能通过jupyter选择R内核进行创建，Pycharm目前没有找到方法手动切换到R内核
启动jupyter：`jupyter lab`或者`jupyter notebook`