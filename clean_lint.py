#!/usr/local/bin/python
# -*-coding:utf-8-*-
#################################################
# 环境: win + python2.7
# Author: changqiang
# Email: hcq0618@163.com
# 说明：
# 1、使用前先clean工程，确保工程bin下重新生成dex，以便lint进行分析。
# 2、如果清除资源后，工程缺少文件而报错（极少情况），尝试通过svn恢复该文件即可。
# 3、修改配置文件clean_lint_config.ini中的路径即可使用，其中：
# projectPath：项目路径
# lintPath：Android SDK目录中lint.bat的路径 一般为Android SDK目录下tools目录中
# 4、配置文件中filterkeys为过滤的关键字集合 默认过滤Android项目中values和layout目录下的资源
# 支持自定义添加 格式为：关键字1|关键字2 即以|分割
# 5、可利用cxFreeze、py2exe、pyInstaller等工具将py文件打包转成exe执行文件
#################################################

import sys
import os
import subprocess

import ConfigParser

# 定义python环境版本 用于兼容3.0以上语法变更
python_ver = 2.7

reload(sys)
sys.setdefaultencoding('utf-8')


# 打印兼容函数
def print_compat(s1, *sn):
    if len(sn) > 0:
        print_str = s1 % sn
    else:
        print_str = s1

    if python_ver < 3:
        print print_str
    else:
        print (print_str)


# 读取配置文件
configPath = os.path.abspath('.') + os.sep + "clean_lint_config.ini"
if not os.path.exists(configPath):
    print_compat("Warning:there is no file " + configPath)
    sys.exit()

config = ConfigParser.ConfigParser()
config.readfp(open(configPath))

pattern = "appears to be unused"
projectPath = config.get('path', 'projectPath').encode('gbk')
# print_compat("projectPath is " + projectPath)
lintPath = config.get('path', 'lintPath').encode('gbk')
# print_compat("lintPath is " + lintPath)
filterKeys = config.get('params', 'filterkeys').split('|')
# print_compat(filterKeys)

i = 0
j = 0

# 执行lint命令
cmd = lintPath + ' --check UnusedResources ' + projectPath
print_compat(cmd)
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
p.wait()


# 过滤关键字
def filter_file(sub_path):
    for key in filterKeys:
        if key in sub_path:
            # print_compat(key)
            return True
    return False


# 开始循环删除无用资源文件
for line in p.stdout:
    print_compat(line)
    if pattern in line:
        if line[0:3] != 'res':
            continue
        i = i + 1
        pos = line.find(':')
        subPath = line[0:pos]

        # print_compat(subPath)
        if filter_file(subPath):
            continue
        filename = projectPath + os.sep + subPath
        # print_compat(filename)
        if os.path.exists(filename):
            os.remove(filename)
            j = j + 1
            print_compat(filename + " was deleted!")
        else:
            print_compat(filename + " is not exists")

print_compat("Total Unused File Resources = " + str(i))
print_compat("Total deleted File Resources = " + str(j))

p.kill()
