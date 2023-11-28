try:
    from flask import Flask, render_template, request, jsonify
except ImportError:
    print("Flask Not Found  (Run the installer)")
try:
    from webForms import esrgan_form, sdxl_form, lcm_form, codeformer_form
except ImportError:
    print("Web Forms Import Error")
    exit(1)
try:
    from webCores import file_path_and_check, cloud_process
except ImportError:
    print("Web Cores Import Error")
from os import environ, system, getcwd
from os.path import exists
from time import sleep
from sys import argv

web_ui = Flask(__name__, template_folder="templates", static_folder="Assets")
web_ui.config['SECRET_KEY'] = "Naveen William"


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

    model_id = "sczhou/codeformer:7de2ea26c616d5bf2245ad0d5e24f0ff9a6204578a5c876db53142edd9d2cd56"
    model_params = {
        "image": open(file_path, "rb"),
        'background_enhance': enhance,
        'upscale': upscale
    }
    cloud_process("codeformer", model_id, model_params, False, out_file_name)


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
    model_id = "luosiallen/latent-consistency-model:553803fd018b3cf875a8bc774c99da9b33f36647badfd88a6eec90d61c5f62fc"
    model_params = {
        "prompt": f"{prompt}",
        "width": width,
        "height": height
    }
    cloud_process("lcm", model_id, model_params, True, filename)


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

    model_id = "stability-ai/sdxl:8beff3369e81422112d93b89ca01426147de542cd4684c244b673b105188fe5f"
    model_params = {
        "prompt": f"{prompt}",
        "negative_prompt": f"{nprompt}",
        "width": width,
        "height": height,
        "apply_watermark": False
    }
    cloud_process("sdxl", model_id, model_params, True, filename)


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

    model_id = "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b"
    model_params = {
        "image": open(file_path, "rb"),
        "upscale": upscale,
        "face_enhance": enhance
    }
    cloud_process("esrgan", model_id, model_params, False, out_file_name)


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
