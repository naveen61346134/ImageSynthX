import os
import wget
import time
import replicate

try:
    with open("token.txt", "r") as t:
        token = t.readlines()
    os.environ["REPLICATE_API_TOKEN"] = f"{token[0]}"
except FileNotFoundError:
    print("TOKEN FILE NOT FOUND!")
    time.sleep(1)
    exit(1)
dir_path = os.getcwd()


def download(url, out_f, out_file_name, png_check):
    wget.download(str(url), out=out_f)
    if png_check ==  True:
        file_ext = f"{out_file_name}.png"
    else:
        file_ext = f"{out_file_name}.jpeg"

    if os.path.exists(file_ext):
        print("\nFile Created!")
    else:
        print("\nERROR")
    time.sleep(2)

def file_path_and_check(png):
    file_path = input("Enter complete file path: ")
    out_file_name = input("Enter output file name: ")
    if os.path.exists(file_path):
        pass
    else:
        print("File doesnt exist!")
        exit(1)
    if png == True:
        out_f = dir_path + f"\\{out_file_name}.png"
    else:
        out_f = dir_path + f"\\{out_file_name}.jpeg"
    return file_path, out_f, out_file_name


def esrgan():
    file_path, out_f, out_file_name = file_path_and_check(True)
    try:
        upscale = int(input("Enter upscale value: "))
    except ValueError:
        upscale = 4

    print("Processing...")
    try:
        output = replicate.run(
            "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
            input={"image": open(file_path, "rb"), "upscale": upscale}
        )
    except Exception as e:
        if "NSFW" in str(e):
            print("NSFW Content Detected")
            time.sleep(1)
            exit(1)
        else:
            print(str(e))
    print("Downloading...")
    download(str(output), out_f, out_file_name, True)


def sdxl():
    prompt = input("Enter prompt for image: ")
    out_file_name = input("Enter output file name: ")
    try:
        width = int(input("Enter width: "))
        height = int(input("Enter hieight: "))
    except ValueError:
        width = 1024
        height = 1024
    print("Processing...")
    try:
        output = replicate.run(
            "stability-ai/sdxl:8beff3369e81422112d93b89ca01426147de542cd4684c244b673b105188fe5f",
            input={"prompt": f"{prompt}", "width": width, "height": height, "apply_watermark": False}
        )
    except Exception as e:
        if "NSFW" in str(e):
            print("NSFW Content Detected")
            time.sleep(1)
            exit(1)
        else:
            print(str(e))
    out_f = dir_path + f"\\{out_file_name}.jpeg"
    print("Downloading...")
    download(str(output[0]), out_f, out_file_name, False)


def cartoonify():
    file_path, out_f, out_file_name = file_path_and_check(True)
    print("Processing...")
    try:
        output = replicate.run(
            "catacolabs/cartoonify:043a7a0bb103cd8ce5c63e64161eae63a99f01028b83aa1e28e53a42d86191d3",
            input={"image": open(file_path, "rb")}
        )
    except Exception as e:
        if "NSFW" in str(e):
            print("NSFW Content Detected")
            time.sleep(1)
            exit(1)
        else:
            print(str(e))
    print("Downloading...")
    download(str(output), out_f, out_file_name, True)


def anime_anything():
    prompt = input("Enter prompt for image: ")
    out_file_name = input("Enter output file name: ")
    try:
        width = int(input("Enter width: "))
        height = int(input("Enter hieight: "))
    except ValueError:
        width = 512
        height = 512
    print("Processing...")
    try:
        output = replicate.run(
            "cjwbw/anything-v4.0:42a996d39a96aedc57b2e0aa8105dea39c9c89d9d266caf6bb4327a1c191b061",
            input={"prompt": prompt, "width": width, "height": height}
        )
    except Exception as e:
        if "NSFW" in str(e):
            print("NSFW Content Detected")
            time.sleep(1)
            exit(1)
        else:
            print(str(e))
    print("Downloading...")
    out_f = dir_path + f"\\{out_file_name}.png"
    download(str(output[0]), out_f, out_file_name, True)


if __name__ == "__main__":
    try:
        while True:
            print("""\n
                [1] Image upscaler (REAL ESRGAN)
                [2] Text to image (SDXL)
                [3] Cartoonify (CARTOONIFY)
                [4] Anime (ANYTHING V4.0) -> MAX RES: [1024x768 or 768x1024]
                [0] EXIT
            """)
            choice = input("\nEnter choice: ")
            if choice == "1":
                esrgan()
            elif choice == "2":
                sdxl()
            elif choice == "3":
                cartoonify()
            elif choice == "4":
                anime_anything()
            elif choice == "0":
                exit(0)
            else:
                print("Invalid Choice\n")
    except KeyboardInterrupt:
        print("\nInterrupt Detected..")
        time.sleep(1)
        exit(0)
