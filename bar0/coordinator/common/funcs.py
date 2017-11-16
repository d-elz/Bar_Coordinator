import os , sys

def dirc(ex_file,back,file):
    dir_of_executable = os.path.dirname(ex_file)
    path = os.path.abspath(os.path.join(dir_of_executable, back)) + file
    return path

def read_file(path):
    f = open(path)   # Make a new file in output mode >>>
    text = f.read()  # Read entire file into a string >>> text 'Hello\nworld\n'
    return text
