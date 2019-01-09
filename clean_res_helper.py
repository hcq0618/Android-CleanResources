#!/usr/local/bin/python
# -*-coding:utf-8-*-

import json
import os

import sys


class ConfigReader:
    def __init__(self):
        config_path = os.path.abspath('.') + os.sep + "clean_res_config.json"
        if not os.path.exists(config_path):
            print "Warning:there is no file - " + config_path
            sys.exit()

        f = None
        try:
            if os.path.exists(config_path):
                f = open(config_path, 'r')
                self.config = json.load(f)
        finally:
            if f:
                f.close()

    @staticmethod
    def encode_path(path):
        if path:
            return path.encode('gbk')
        else:
            return path

    def get_path(self, path_key):
        paths = None
        if self.config and 'paths' in self.config:
            paths = self.config['paths']

        if paths and path_key in paths:
            path = paths[path_key]
            if isinstance(path, list):
                path_list = path
                for index in range(len(path_list)):
                    path_list[index] = self.encode_path(path_list[index])
                return path_list
            else:
                return self.encode_path(path)

        return None

    def get_params(self, params_key):
        params = None
        if self.config and 'params' in self.config:
            return self.config['params']

        if params and params_key in params:
            return params[params_key]

        return None

    def get_project_path(self):
        return self.get_path('projectPath')

    def get_lib_paths(self):
        return self.get_path('libPaths')

    def get_lint_path(self):
        return self.get_path('lintPath')

    def get_matrix_json_result_path(self):
        return self.get_path('matrixJsonResultPath')

    def get_keep_file_path_keys(self):
        return self.get_params('keepFilePathKeys')

    def get_module_name(self):
        return self.get_params('moduleName')


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
        if keep_file_path_keys:
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
