#!/usr/local/bin/python
# -*-coding:utf-8-*-

import os
import subprocess

from clean_res_helper import ConfigReader, Utils

# 获取配置文件参数
configReader = ConfigReader()
projectPath = configReader.get_project_path()
lintPath = configReader.get_lint_path()
# print "projectPath is " + projectPath
# print "lintPath is " + lintPath

# 执行lint命令
cmd = lintPath + ' --check UnusedResources ' + projectPath
print cmd
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
process.wait()

# 获取需要保留的文件目录
keepFilePathKeys = configReader.get_keep_file_path_keys()

unused_files = []
unused_file_total_size = 0

delete_files = []
delete_file_total_size = 0

# 开始循环删除无用资源文件
pattern = "appears to be unused"
for line in process.stdout:
    print line
    if pattern in line:
        if line[0:3] != 'res':
            continue
        pos = line.find(':')
        subPath = line[0:pos]
        # print subPath

        filePath = projectPath + os.sep + subPath
        # print filePath

        fileSize = Utils.get_file_size(filePath)
        if fileSize > 0 and filePath not in unused_files:
            unused_files.append(filePath)
            unused_file_total_size += fileSize

        if Utils.is_keep_file_path(keepFilePathKeys, filePath):
            continue

        if Utils.delete_file(filePath) and filePath not in delete_files:
            delete_files.append(filePath)
            delete_file_total_size += fileSize

Utils.print_result(len(unused_files), unused_file_total_size, len(delete_files), delete_file_total_size)
