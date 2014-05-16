#!/usr/local/bin/python
#-*-coding:utf-8-*-
#################################################
#环境: win + python2.7
#Author: changqiang
#Email: hcq0618@163.com
#说明：
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

#定义python环境版本 用于兼容3.0以上语法变更
python_ver = 2.7

reload(sys)
sys.setdefaultencoding('utf-8')


#打印兼容函数
def printCompat(s1, *sn):
    printStr = None
    if len(sn) > 0:
        printStr = s1 % sn
    else:
        printStr = s1

    if python_ver < 3:
        print printStr
    else:
        print (printStr)


#读取配置文件
configPath = os.path.abspath('.') + "\/clean_lint_config.ini"
if not os.path.exists(configPath):
    printCompat("Warning:there is no file " + configPath)
    sys.exit()

config = ConfigParser.ConfigParser()
config.readfp(open(configPath))

pattern = "appears to be unused"
projectPath = config.get('path', 'projectPath').encode('gbk')
printCompat("projectPath is " + projectPath)
lintPath = config.get('path', 'lintPath').encode('gbk')
printCompat("lintPath is " + lintPath)
filterKeys = config.get('params', 'filterkeys').split('|')
printCompat(filterKeys)

i = 0
j = 0


#执行lint命令
cmd = lintPath + ' --check UnusedResources ' + projectPath
printCompat(cmd)
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
p.wait()


#过滤关键字
def filterFile(subPath):
    for key in filterKeys:
        if key in subPath:
            # printCompat(key)
            return True
    return False


#开始循环删除无用资源文件
for line in p.stdout:
    printCompat(line)
    if pattern in line:
        if (line[0:3] != 'res'):
            continue
        i = i + 1
        pos = line.find(':')
        subPath = line[0:pos]

        # printCompat(subPath)
        if filterFile(subPath):
            continue
        filename = projectPath + "\/" + subPath
        # printCompat(filename)
        if os.path.exists(filename):
            os.remove(filename)
            j = j + 1
            printCompat(filename + " was deleted!")
        else:
            printCompat(filename + " is not exists")

printCompat("Total Unused File Resources = " + str(i))
printCompat("Total deleted File Resources = " + str(j))

p.kill()