# 说明

* 本项目是一些自己编写的生信脚本，还在不断完善中

## 环境安装

* 单独安装：可以独立安装对应脚本中用到的模块，直接看最上面导入的模块即可
* 统一安装：使用pipenv安装所有脚本需要的模块
    * `pip install pipenv`
    * `pipenv install`
* 更多生信需要用的软件使用conda安装：`conda env create -f conda.yaml`

## 脚本说明

* ncbi:NCBI数据库接口调用，只需要根据官方文档中提供的参数改写相应的函数即可
    * snp.py: 获取snp信息
        * 脚本是根据基因名称获得snp
        * 后续会扩展为拥有各式各样的数据库和查询条件
        * 后续会使用命令行输入和配置文件共用的形式给与方便简单的调用
* fastq
    * compare.py：比对双端的fastq文件每四行的key（或者叫id）是否一一对应
    * filter.py：过滤掉fastq文件中的符合过滤规则的部分
* encode:爬取encode数据库和下载相应文件的脚本
* wes：遗传相关的脚本