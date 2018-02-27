import os
import shutil


def recursive_copy(src, dest):
    for file in os.listdir(src):
        path = os.path.join(src, file)

        if os.path.isfile(path):
            shutil.copy(path, dest)
