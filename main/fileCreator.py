# Helper functions for creating files at specific path.

from glob import glob

def writeTextFile(path, name, content):
        print('Writing Start')
        full_path = path + '\\' + name + '.txt'
        text_file= open(full_path, "w")
        lines = content
        text_file.writelines(lines)
        text_file.close()

# If file has been created, return 1. Else, return 0.
def numFilesIn(path):
    directory = glob(path + '\\*.txt')
    return len(directory)