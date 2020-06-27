import argparse
import shutil
import os
# import sys


class Directory:
    def __init__(self, path):
        self.directory_path = os.path.abspath('.') if path is None else path
        self.files_before = self.get_files()
        self.undo_list = [self.files_before]
        self.redo_list = []

    def get_files(self):
        return {os.stat(filename).st_ino: filename
                for filename in os.listdir(self.directory_path)
                if os.path.isfile(filename)}

    def rename(self, old_names, new_names):
        for inode, file_before in old_names.items():
            shutil.move(file_before, new_names[inode])
            self.undo_list.append(new_names)

    def undo(self):
        if len(self.undo_list) > 1:
            last_names = self.undo_list.pop()
            before_names = self.undo_list.pop()
            self.rename(last_names, before_names)
            self.redo_list.append(before_names)

    def redo(self):
        if self.redo_list != []:
            before_names = self.undo_list[-1]
            new_names = self.redo_list.pop()
            self.rename(before_names, new_names)

    def check_inode(self, inode_1, inode_2):
        '''TODO USEFULL ???'''
        return inode_1 == inode_2


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', action="store", default=None)
    parser.add_argument('-f', '--format', action="store")
    args = parser.parse_args()
    return args


def main():
    args = read_args()
    directory = Directory(args.path)
    return directory


if __name__ == "__main__":
    directory = main()
