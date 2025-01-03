import os
import shutil

def static_refresh(source_dir="static", destination_dir="public"):
    if os.path.exists(destination_dir):
        shutil.rmtree(path=destination_dir)    
    file_list = os.listdir(path=source_dir)
    os.mkdir(destination_dir)

    for item in file_list:
        source_path = os.path.join(source_dir, item)
        destination_path = os.path.join(destination_dir, item)
        if os.path.isdir(source_path):
            os.mkdir(destination_path)
            static_refresh(source_path, destination_path)
        else:
            shutil.copy(source_path, destination_path)
