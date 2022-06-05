import os


def get_files(dir):
    retval = []
    for root, _, files in os.walk(dir):
        for file in files:
            retval.append(os.path.join(root, file))
    
    return retval
