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

    def get_filter_keys(self):
        return self.config.get(self.paramsSectionKey, 'filterKeys').split('|')

    def get_main_module_name(self):
        return self.config.get(self.paramsSectionKey, 'mainModuleName')


class Utils:
    def __init__(self):
        return

    # 获取文件的大小,结果保留两位小数，单位为KB
    @staticmethod
    def get_file_size(file_path):
        file_size = os.path.getsize(file_path)
        file_size = file_size / float(1024)
        return round(file_size, 2)

    # 是否为过滤的文件
    @staticmethod
    def is_filter_file(filter_keys, sub_path):
        for key in filter_keys:
            if key in sub_path:
                # print key
                return True
        return False

    @staticmethod
    def print_result(unused_file_count, unused_file_total_size, delete_file_count, delete_file_total_size):
        print "Total unused file resources count is %s and total size is %s kb" % \
              (str(unused_file_count), str(unused_file_total_size))
        print "Total deleted file resources count is %s and total size is %s kb" % \
              (str(delete_file_count), str(delete_file_total_size))

    @staticmethod
    def delete_file(filename):
        if os.path.exists(filename):
            os.remove(filename)
            print filename + " was deleted!"
            return True
        else:
            print filename + " is not exists"
            return False
