#!/usr/local/bin/python
# -*-coding:utf-8-*-

# 读取配置文件
import ConfigParser
import os

import sys


class ConfigReader:
    pathSectionKey = 'path'
    paramsSectionKey = 'params'

    def __init__(self):
        config_path = os.path.abspath('.') + os.sep + "clean_res_config.ini"
        if not os.path.exists(config_path):
            print "Warning:there is no file - " + config_path
            sys.exit()

        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(config_path))

    @staticmethod
    def encode_path(path):
        return path.encode('gbk')

    def get_project_path(self):
        project_path = self.config.get(self.pathSectionKey, 'projectPath')
        return self.encode_path(project_path)

    def get_lint_path(self):
        lint_path = self.config.get(self.pathSectionKey, 'lintPath')
        return self.encode_path(lint_path)

    def get_keep_file_path_keys(self):
        return self.config.get(self.paramsSectionKey, 'keepFilePathKeys').split('|')

    def get_module_name(self):
        return self.config.get(self.paramsSectionKey, 'moduleName')


class Utils:
    def __init__(self):
        return

    # 获取文件的大小,结果保留两位小数，单位为KB
    @staticmethod
    def get_file_size(file_path):
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            file_size = file_size / float(1024)
            return round(file_size, 2)

    # 是否为需要忽略的目录
    @staticmethod
    def is_keep_file_path(keep_file_path_keys, file_path):
        for key in keep_file_path_keys:
            if os.sep + key in file_path:
                # print key
                return True
        return False

    @staticmethod
    def print_result(unused_file_count, unused_file_total_size, delete_file_count, delete_file_total_size):
        print "Total unused resources count is %s and total size is %s kb" % \
              (str(unused_file_count), str(unused_file_total_size))
        print "Total deleted file resources count is %s and total size is %s kb" % \
              (str(delete_file_count), str(delete_file_total_size))

    @staticmethod
    def delete_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            print file_path + " was deleted!"
            return True
        else:
            print file_path + " is not exists"
            return False
