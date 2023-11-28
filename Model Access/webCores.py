try:
    from flask import flash, redirect, url_for
except ImportError:
    print("Flask Not Found  (Run the installer)")
from os.path import exists, dirname
try:
    from wget import download as dwn
except ImportError:
    print("Wget Not Found  (Run the installer)")
try:
    from replicate import run
except ImportError:
    print("replicate Not Found  (Run the installer)")
from shutil import copy
from os import getcwd

dir_path = getcwd() + "\Output"
dir_name = dirname(__file__)


def download(url, out_f, out_file_name):
    dwn(str(url), out=out_f)
    file_ext = f"\{out_file_name}.png"
    exist = dir_path+file_ext
    if exists(exist):
        return True
    else:
        return False


def file_path_and_check(file, fileName):
    file_path = f"{dir_path}\{file}"
    out_file_name = fileName
    if not exists(file_path):
        exit(0)
    out_f = dir_path + f"\{out_file_name}.png"
    return file_path, out_f, out_file_name


def exceptionizer(exception):
    if "NSFW" in str(exception):
        print("\t\tNSFW Content Detected")
        flash("NSFW Content Detected")
    elif "getaddrinfo" in str(exception):
        print("\t\tNetwork Error")
        flash("Network Error")
    elif "CUDA" or "memory" in str(exception):
        print("\t\tMODEL ERROR: CUDA OUT OF MEMORY")
        print(f"\n\n{str(exception)}")
        flash("Model Error: CUDA OUT OF MEMORY")
    else:
        print(str(exception))


def cloud_process(model_name, model_id, input_params, list_check, file_name):
    output = ""
    output_bool = False
    out_f = dir_path + f"\{file_name}.png"
    out_file_name = file_name

    try:
        print("\n")
        print(model_id)
        print(input_params)
        output = run(model_id, input=input_params)
        output_bool = bool(output)
    except Exception as e:
        exceptionizer(str(e))
        return redirect(url_for(model_name))

    if output_bool:
        if list_check == True:
            status = download(str(output[0]), out_f, out_file_name)
        else:
            status = download(str(output), out_f, out_file_name)

        if status == True:
            print("DOWNLOADED")
            print(out_f)
            print(input_params)
            copy_status = bool(copy(f"{dir_name}\\Output\\{out_file_name}.png",
                                    f"{dir_name}\\Assets\\Output\\"))
            if not copy_status:
                print("Shutil copy Error!")
                exit(0)
            else:
                print("File Copied")
        else:
            print("ERROR DOWNLOADING")
    else:
        return redirect(url_for(model_name))
