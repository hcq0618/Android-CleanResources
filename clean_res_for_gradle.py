#!/usr/local/bin/python
# -*-coding:utf-8-*-
import subprocess
import xml

import os
from xml.sax import make_parser, ContentHandler

from clean_res_helper import ConfigReader, Utils

# 获取配置文件参数
configReader = ConfigReader()
projectPath = configReader.get_project_path()
moduleName = configReader.get_module_name()

# 执行lint命令
goToProjectCmd = 'cd %s' % projectPath
lintCmd = './gradlew :%s:lintDebug' % moduleName
cmd = goToProjectCmd + ' && ' + lintCmd
print cmd
process = subprocess.Popen(cmd, shell=True)
process.wait()


class IssueHandler(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)
        self.isUnusedRes = False
        self.unusedResList = []

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        if tag == 'issue':
            # print '*****issue*****'
            # print tag
            if 'id' in attributes:
                _id = attributes['id']
                if _id == 'UnusedResources':
                    self.isUnusedRes = True
                    # print 'id:', _id
                    return
            self.isUnusedRes = False
        elif tag == 'location':
            if self.isUnusedRes:
                if 'file' in attributes:
                    file_path = attributes['file']
                    print file_path
                    self.unusedResList.append(file_path)

    def get_unused_res_list(self):
        return self.unusedResList


parser = make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
issueHandler = IssueHandler()
parser.setContentHandler(issueHandler)
parser.parse(
    projectPath + os.sep + moduleName + os.sep + 'build' + os.sep + 'reports' + os.sep + 'lint-results-debug.xml'
)

# 获取需要保留的文件目录
keepFilePathKeys = configReader.get_keep_file_path_keys()

unusedResList = issueHandler.get_unused_res_list()

unused_files = []
unused_file_total_size = 0

delete_files = []
delete_file_total_size = 0

for filePath in unusedResList:
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
