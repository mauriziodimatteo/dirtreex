#!/usr/bin/env python
import os
import argparse

parser = argparse.ArgumentParser(description='Print the directory tree for the LaTeX dirtree package.')
parser.add_argument(dest='path', type=str, help="Root directory of the tree")
parser.add_argument('-H', '--includeHidden', dest='includeHidden', action='store_true', help='Include hidden files')
parser.add_argument('-S', '--includeSystem', dest='includeSystem', action='store_true', help='Include system files')

rootDir = parser.parse_args().path
includeHidden = parser.parse_args().includeHidden
includeSystem = parser.parse_args().includeSystem

print(includeSystem)
print(includeHidden)

indentChar = " "

# Count how many levels deep is the directory with respect to dirRoot
def get_relative_depth(dir_path, level_offset):
    return dir_path.count(os.path.sep) - level_offset


# Escape illegal symbols for LaTeX
def escape_illegal(name):
    illegal_char_array = ['\\', '&', '%', '$', '#', '_', '{', '}', '~', '^']
    for char in illegal_char_array:
        name = name.replace(char, "\\" + char)
    return name


# Return true if a file is system file
def is_system_file(file_name):
    system_file_names = [".DS_Store"]
    for sfn in system_file_names:
        if file_name == sfn:
            return True
    return False


# Return true if a file is hidden
def is_hidden(file_name):
    return file_name[0] == "."


levelOffset = rootDir.count(os.path.sep) - 1

print "\dirtree{%"

for dirName, subdirList, fileList in os.walk(rootDir):

    level = get_relative_depth(dirName, levelOffset)

    if level == 1:  # for the first level print the whole path
        print(indentChar + "." + str(level) + " " + escape_illegal(rootDir) + " .")
    else:
        baseName = os.path.basename(dirName)
        if not includeHidden or is_hidden(baseName):
            print(indentChar * level + "." + str(level) + " " + escape_illegal(baseName) + " .")

    level += 1
    for fileName in fileList:
        if (not includeHidden or is_hidden(fileName)) and (not includeSystem or is_system_file(fileName)):
            print(indentChar * level + "." + str(level) + " " + escape_illegal(fileName) + " .")

print "}"