#!/usr/local/bin/python
# -*-coding:utf-8-*-
import json

import os

from clean_res_helper import ConfigReader, Utils


class ResultParser:
    def __init__(self):
        config_reader = ConfigReader()
        project_path = config_reader.get_project_path()
        lib_paths = config_reader.get_lib_paths()
        matrix_json_result_path = config_reader.get_matrix_json_result_path()
        # print matrix_json_result_path

        self.search_paths = []
        self.search_paths.append(project_path)
        for lib_path in lib_paths:
            self.search_paths.append(lib_path)
        # print self.search_paths

        f = None
        try:
            if os.path.exists(matrix_json_result_path):
                f = open(matrix_json_result_path, 'r')
                self.result = json.load(f)
        finally:
            if f:
                f.close()

    def execute(self):
        unused_resources = None
        for task in self.result:
            task_type = task['taskType']
            if task_type == 12:
                unused_resources = task['unused-resources']
                # print len(unused_resources)

        res_sub_dirs = []
        for root_dir in self.search_paths:
            self.get_res_sub_dirs(root_dir, res_sub_dirs)

        unused_res_paths = []
        unused_files_total_size = 0
        for unused_res in unused_resources:
            unused_res_split = unused_res.split('.')
            unused_res_dir = unused_res_split[1]
            unused_res_name = unused_res_split[2]
            for res_sub_dir in res_sub_dirs:
                if unused_res_dir in res_sub_dir:
                    # print unused_res_name
                    unused_files_total_size += self.delete_unused_res(unused_res_name, res_sub_dir, unused_res_paths)

        Utils.print_result(len(unused_res_paths), unused_files_total_size, len(unused_res_paths),
                           unused_files_total_size)

    def get_res_sub_dirs(self, root_dir, res_sub_dirs):
        list_dir = os.listdir(root_dir)
        for _dir in list_dir:
            path = os.path.join(root_dir, _dir)
            if os.path.isdir(path):
                if '/main/res' in path and 'main/resources' not in path:
                    self.get_sub_dirs(path, res_sub_dirs)
                else:
                    self.get_res_sub_dirs(path, res_sub_dirs)

    def get_sub_dirs(self, res_dir, res_sub_dirs):
        list_dir = os.listdir(res_dir)
        for _dir in list_dir:
            path = os.path.join(res_dir, _dir)
            if os.path.isdir(path):
                res_sub_dirs.append(path)
                print path

    @staticmethod
    def delete_unused_res(unused_res_name, res_sub_dir, unused_res_paths):
        unused_files_size = 0
        list_files = os.listdir(res_sub_dir)
        for list_file in list_files:
            path = os.path.join(res_sub_dir, list_file)
            if os.path.isfile(path) and unused_res_name in path:
                print path
                unused_res_paths.append(path)
                unused_files_size += Utils.get_file_size(path)
                Utils.delete_file(path)
        return unused_files_size


resultParser = ResultParser()
resultParser.execute()
