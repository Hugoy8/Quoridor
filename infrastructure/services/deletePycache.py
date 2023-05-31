import os
import shutil

def deletePycache():
    root_dir = os.getcwd()
    for root, dirs, files in os.walk(root_dir):
        if "__pycache__" in dirs:
            pycache_dir = os.path.join(root, "__pycache__")
            shutil.rmtree(pycache_dir)
        