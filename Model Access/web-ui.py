try:
    from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
except ImportError:
    print("Flask Not Found  (Run the installer)")
try:
    from webForms import esrgan_form, sdxl_form, lcm_form, codeformer_form
except ImportError:
    print("Web Forms Import Error")
    exit(1)
try:
    from webCores import download, file_path_and_check, dir_path
except ImportError:
    print("Web Cores Import Error")
from os import environ, system, getcwd
from os.path import dirname, exists
try:
    from replicate import run
except ImportError:
    print("Replicate Not Found (Run the installer)")
from shutil import copy
from time import sleep
from sys import argv

web_ui = Flask(__name__, template_folder="templates", static_folder="Assets")
web_ui.config['SECRET_KEY'] = "Naveen William"
dir_name = dirname(__file__)


def program_init():
    try:
        check = argv[1]
        if check != "True":
            print("Run Image-SynthX")
            sleep(2)
            exit(0)
    except IndexError:
        print("Argv Error run Image-SynthX")
        sleep(2)
        exit(0)
    try:
        with open("token.txt", "r") as t:
            token = t.readline()
        if len(token) <= 10:
            print("INVALID TOKEN")
            exit(0)
        else:
            environ["REPLICATE_API_TOKEN"] = f"{token}"
    except FileNotFoundError:
        print("TOKEN FILE NOT FOUND!")
        exit(0)
    if not exists("Output"):
        system("mkdir Output")
        print("Output folder has been created!")


@web_ui.route("/")
def main():
    return render_template("synthx.html")


@web_ui.route("/codeformer", methods=['GET', 'POST'])
def codeformer():
    form = codeformer_form()
    if request.method == 'POST':
        image = str(form.image_file.data).split(" ")[1].strip("'")
        out_file_name = form.filename.data
        upscale_val = form.upscale.data
        background_enhance = bool(request.form.get("enhance"))

        codeformer_processor(image, out_file_name,
                             upscale_val, background_enhance)

    return render_template("codeformer.html", form=form)


def codeformer_processor(image, file_name, upscale, enhance):
    file_path, out_f, out_file_name = file_path_and_check(
        image, file_name)
    print(file_path)
    print(out_f)
    print(out_file_name)

    output = ""
    output_bool = False
    try:
        output = run(
            "sczhou/codeformer:7de2ea26c616d5bf2245ad0d5e24f0ff9a6204578a5c876db53142edd9d2cd56",
            input={"image": open(file_path, "rb"),
                   'background_enhance': enhance, 'upscale': upscale}
        )
        output_bool = bool(output)
    except Exception as e:
        if "NSFW" in str(e):
            print("\t\tNSFW Content Detected")
            flash("NSFW Content Detected")
        elif "getaddrinfo" in str(e):
            print("\t\tNetwork Error")
            flash("Network Error")
        elif "CUDA" or "memory" in str(e):
            print("\t\tMODEL ERROR: CUDA OUT OF MEMORY")
            flash("Model Error: CUDA OUT OF MEMORY")
        else:
            print(str(e))

    if output_bool:
        status = download(str(output), out_f, out_file_name)
        if status == True:
            print("DOWNLOADED")
            print(out_f)
            print(out_file_name)
            copy_status = bool(copy(f"{dir_name}\\Output\\{out_file_name}.png",
                                    f"{dir_name}\\Assets\\Output\\"))
            if not copy_status:
                print("Shutil copy Error!")
                exit(0)
            else:
                print("File Copied")
                check_processed_status(out_file_name)
        else:
            print("ERROR DOWNLOADING")
    else:
        return redirect(url_for("codeformer"))


@web_ui.route("/lcm", methods=['GET', 'POST'])
def lcm():
    form = lcm_form()
    if request.method == 'POST':
        prompt = form.prompt.data
        filename = form.filename.data

        height = int(form.height.data)
        lDiv8 = len(str(height/8).split(".")[1])
        if lDiv8 > 1:
            height = 720
        width = int(form.width.data)
        wDiv8 = len(str(width/8).split(".")[1])
        if wDiv8 > 1:
            width = 720

        print(prompt)
        print(filename)
        print(height)
        print(width)
        lcm_image_processor(prompt, filename, height, width)

    return render_template("lcm.html", form=form)


def lcm_image_processor(prompt, filename, height, width):
    print(prompt)
    print(filename)
    print(f"{height}x{width}")
    output = []
    output_bool = False
    try:
        output = run(
            "luosiallen/latent-consistency-model:553803fd018b3cf875a8bc774c99da9b33f36647badfd88a6eec90d61c5f62fc",
            input={
                "prompt": f"{prompt}", "width": width, "height": height}
        )
        output_bool = bool(output)
    except Exception as e:
        if "NSFW" in str(e):
            print("\t\tNSFW Content Detected")
            flash("NSFW Content Detected")
        elif "getaddrinfo" in str(e):
            print("\t\tNetwork Error")
            flash("Network Error")
        elif "CUDA" or "memory" in str(e):
            print("\t\tMODEL ERROR: CUDA OUT OF MEMORY")
            flash("Model Error: CUDA OUT OF MEMORY")
        else:
            print(str(e))

    if output_bool:
        out_f = dir_path + f"\{filename}.png"
        status = download(str(output[0]), out_f, filename)
        if status == True:
            print("DOWNLOADED")
            print(out_f)
            print(filename)
            copy_status = bool(copy(f"{dir_name}\\Output\\{filename}.png",
                                    f"{dir_name}\\Assets\\Output\\"))
            if not copy_status:
                print("Shutil copy Error!")
                exit(0)
            else:
                print("File Copied")
                check_processed_status(filename)
        else:
            print("ERROR DOWNLOADING")
    else:
        return redirect(url_for("lcm"))


@web_ui.route("/sdxl", methods=['GET', 'POST'])
def sdxl():
    form = sdxl_form()
    if request.method == 'POST':
        prompt = form.prompt.data
        nPrompt = form.nPrompt.data
        filename = form.filename.data

        height = int(form.height.data)
        lDiv8 = len(str(height/8).split(".")[1])
        if lDiv8 > 1:
            height = 720
        width = int(form.width.data)
        wDiv8 = len(str(width/8).split(".")[1])
        if wDiv8 > 1:
            width = 720

        sdxl_image_processor(prompt, nPrompt, filename, height, width)

    return render_template("sdxl.html", form=form)


def sdxl_image_processor(prompt, nprompt, filename, height, width):
    print(prompt)
    print(nprompt)
    print(filename)
    print(f"{height}x{width}")
    output = []
    output_bool = False
    try:
        output = run(
            "stability-ai/sdxl:8beff3369e81422112d93b89ca01426147de542cd4684c244b673b105188fe5f",
            input={"prompt": f"{prompt}", "negative_prompt": f"{nprompt}", "width": width,
                   "height": height, "apply_watermark": False}
        )
        output_bool = bool(output)
    except Exception as e:
        if "NSFW" in str(e):
            print("\t\tNSFW Content Detected")
            flash("NSFW Content Detected")
        elif "getaddrinfo" in str(e):
            print("\t\tNetwork Error")
            flash("Network Error")
        elif "CUDA" or "memory" in str(e):
            print("\t\tMODEL ERROR: CUDA OUT OF MEMORY")
            flash("Model Error: CUDA OUT OF MEMORY")
        else:
            print(str(e))

    if output_bool:
        out_f = dir_path + f"\{filename}.png"
        status = download(str(output[0]), out_f, filename)
        if status == True:
            print("DOWNLOADED")
            print(out_f)
            print(filename)
            copy_status = bool(copy(f"{dir_name}\\Output\\{filename}.png",
                                    f"{dir_name}\\Assets\\Output\\"))
            if not copy_status:
                print("Shutil copy Error!")
                exit(0)
            else:
                print("File Copied")
                check_processed_status(filename)
        else:
            print("ERROR DOWNLOADING")
    else:
        return redirect(url_for("sdxl"))


@web_ui.route("/real_esrgan", methods=['GET', 'POST'])
def esrgan():
    form = esrgan_form()
    if request.method == 'POST':
        image = str(form.image_file.data).split(" ")[1].strip("'")
        out_file_name = form.filename.data
        upscale_val = form.upscale.data
        enhance = bool(request.form.get("enhance"))

        print(f"{image}\n{out_file_name}\n{upscale_val}\n{enhance}")
        esrgan_image_processor(image, out_file_name, upscale_val, enhance)

    return render_template("esrgan.html", form=form)


def esrgan_image_processor(image, file_name, upscale, enhance):
    file_path, out_f, out_file_name = file_path_and_check(
        image, file_name)
    print(file_path)
    print(out_f)
    print(out_file_name)

    output = ""
    output_bool = False
    try:
        output = run(
            "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
            input={"image": open(file_path, "rb"),
                   "upscale": upscale, "face_enhance": enhance}
        )
        output_bool = bool(output)
    except Exception as e:
        if "NSFW" in str(e):
            print("\t\tNSFW Content Detected")
            flash("NSFW Content Detected")
        elif "getaddrinfo" in str(e):
            print("\t\tNetwork Error")
            flash("Network Error")
        elif "CUDA" or "memory" in str(e):
            print("\t\tMODEL ERROR: CUDA OUT OF MEMORY")
            flash("Model Error: CUDA OUT OF MEMORY")
        else:
            print(str(e))
    if output_bool:
        status = download(str(output), out_f, out_file_name)
        if status == True:
            print("DOWNLOADED")
            print(out_f)
            print(out_file_name)
            copy_status = bool(copy(f"{dir_name}\\Output\\{out_file_name}.png",
                                    f"{dir_name}\\Assets\\Output\\"))
            if not copy_status:
                print("Shutil copy Error!")
                exit(0)
            else:
                print("File Copied")
                check_processed_status(out_file_name)
        else:
            print("ERROR DOWNLOADING")
    else:
        return redirect(url_for("esrgan"))


@web_ui.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@web_ui.route("/check_processed_status/<file_name>", methods=['GET'])
def check_processed_status(file_name):
    processed_image_path = getcwd() + f"/Assets/Output/{file_name}.png"
    print("\t\t" + processed_image_path)
    if exists(processed_image_path):
        print("YES.................")
        proc = f"/Assets/Output/{file_name}"
        return jsonify({'status': 'success', 'result_url': proc})
    else:
        print("NO....................")
        return jsonify({'status': 'pending'})


if __name__ == "__main__":
    program_init()
    web_ui.run(debug=True)
