#!/usr/local/bin/python
# -*-coding:utf-8-*-

import os
import subprocess

from clean_res_helper import ConfigReader, Utils

unused_file_count = 0
unused_file_total_size = 0

delete_file_count = 0
delete_file_total_size = 0

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

# 获取过滤的关键字
keepFilePathKeys = configReader.get_keep_file_path_keys()

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

        filename = projectPath + os.sep + subPath
        # print filename

        unused_file_count += 1
        unused_file_total_size += Utils.get_file_size(filename)

        if Utils.is_keep_file_path(keepFilePathKeys, subPath):
            continue

        if Utils.delete_file(filename):
            delete_file_count += 1
            delete_file_total_size += Utils.get_file_size(filename)

Utils.print_result(unused_file_count, unused_file_total_size, delete_file_count, delete_file_total_size)
