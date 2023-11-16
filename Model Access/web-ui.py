from flask import Flask, render_template, request, jsonify
from webForms import esrgan_form, sdxl_form, lcm_form, codeformer_form
from webCores import download, file_path_and_check, dir_path
import replicate
import os

web_ui = Flask(__name__, template_folder="templates", static_folder="Assets")
web_ui.config['SECRET_KEY'] = "OptimusPrime"


def program_init():
    try:
        with open("token.txt", "r") as t:
            token = t.readline()
        if len(token) <= 10:
            print("INVALID TOKEN")
            exit(0)
        else:
            os.environ["REPLICATE_API_TOKEN"] = f"{token}"
    except FileNotFoundError:
        print("TOKEN FILE NOT FOUND!")
        exit(0)
    if not os.path.exists("Output"):
        os.system("mkdir Output")
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

    output = replicate.run(
        "sczhou/codeformer:7de2ea26c616d5bf2245ad0d5e24f0ff9a6204578a5c876db53142edd9d2cd56",
        input={"image": open(file_path, "rb"),
               'background_enhance': enhance, 'upscale': upscale}
    )
    status = download(str(output), out_f, out_file_name)
    if status == True:
        print("DOWNLOADED")
        print(out_f)
        print(out_file_name)
        print(
            f"copy Output\{out_file_name}.png Z:\ImageSynthX\Assets\Output\\")
        os.system(
            f"copy Output\{out_file_name}.png Z:\ImageSynthX\Assets\Output\\")
        check_processed_status(out_file_name)
    else:
        print("ERROR DOWNLOADING")


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
    output = replicate.run(
        "luosiallen/latent-consistency-model:553803fd018b3cf875a8bc774c99da9b33f36647badfd88a6eec90d61c5f62fc",
        input={
            "prompt": f"{prompt}", "width": width, "height": height}
    )
    out_f = dir_path + f"\{filename}.png"
    status = download(str(output[0]), out_f, filename)
    if status == True:
        print("DOWNLOADED")
        print(out_f)
        print(filename)
        print(
            f"copy Output\{filename}.png Z:\ImageSynthX\Assets\Output\\")
        os.system(
            f"copy Output\{filename}.png Z:\ImageSynthX\Assets\Output\\")
        check_processed_status(filename)
    else:
        print("ERROR DOWNLOADING")


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
    output = replicate.run(
        "stability-ai/sdxl:8beff3369e81422112d93b89ca01426147de542cd4684c244b673b105188fe5f",
        input={"prompt": f"{prompt}", "negative_prompt": f"{nprompt}", "width": width,
               "height": height, "apply_watermark": False}
    )
    out_f = dir_path + f"\{filename}.png"
    status = download(str(output[0]), out_f, filename)
    if status == True:
        print("DOWNLOADED")
        print(out_f)
        print(filename)
        print(
            f"copy Output\{filename}.png Z:\ImageSynthX\Assets\Output\\")
        os.system(
            f"copy Output\{filename}.png Z:\ImageSynthX\Assets\Output\\")
        check_processed_status(filename)
    else:
        print("ERROR DOWNLOADING")


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

    output = replicate.run(
        "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
        input={"image": open(file_path, "rb"),
               "upscale": upscale, "face_enhance": enhance}
    )
    status = download(str(output), out_f, out_file_name)
    if status == True:
        print("DOWNLOADED")
        print(out_f)
        print(out_file_name)
        print(
            f"copy Output\{out_file_name}.png Z:\ImageSynthX\Assets\Output\\")
        os.system(
            f"copy Output\{out_file_name}.png Z:\ImageSynthX\Assets\Output\\")
        check_processed_status(out_file_name)
    else:
        print("ERROR DOWNLOADING")


@web_ui.route("/check_processed_status/<file_name>", methods=['GET'])
def check_processed_status(file_name):
    processed_image_path = os.getcwd() + f"/Assets/Output/{file_name}.png"
    print("\t\t" + processed_image_path)
    if os.path.exists(processed_image_path):
        print("YES.................")
        proc = f"/Assets/Output/{file_name}"
        return jsonify({'status': 'success', 'result_url': proc})
    else:
        print("NO....................")
        return jsonify({'status': 'pending'})


if __name__ == "__main__":
    program_init()
    web_ui.run(debug=True)
