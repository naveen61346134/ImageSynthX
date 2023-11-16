import wget
import os

dir_path = os.getcwd() + "\Output"


def download(url, out_f, out_file_name):
    wget.download(str(url), out=out_f)
    file_ext = f"\{out_file_name}.png"
    exist = dir_path+file_ext
    if os.path.exists(exist):
        return True
    else:
        return False


def file_path_and_check(file, fileName):
    file_path = f"{dir_path}\{file}"
    out_file_name = fileName
    if not os.path.exists(file_path):
        exit(0)
    out_f = dir_path + f"\{out_file_name}.png"
    return file_path, out_f, out_file_name
