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
    file_path, out_f, out_file_name = file_path_and_check()
    try:
        upscale = int(input("Enter upscale value: "))
    except ValueError:
        upscale = 4

    print("Processing...")
    output = replicate.run(
        "cjwbw/real-esrgan:d0ee3d708c9b911f122a4ad90046c5d26a0293b99476d697f6bb7f2e251ce2d4",
        input={"image": open(file_path, "rb"), "upscale": upscale}
    )
    print("Downloading...")
    download(str(output), out_f, out_file_name)


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
    output = replicate.run(
        "stability-ai/sdxl:8beff3369e81422112d93b89ca01426147de542cd4684c244b673b105188fe5f",
        input={"prompt": f"{prompt}", "width": width, "height": height, "apply_watermark": False}
    )
    out_f = dir_path + f"\\{out_file_name}.jpeg"
    print("Downloading...")
    download(str(output[0]), out_f, out_file_name)


def cartoonify():
    file_path, out_f, out_file_name = file_path_and_check(True)
    print("Processing...")
    output = replicate.run(
        "catacolabs/cartoonify:043a7a0bb103cd8ce5c63e64161eae63a99f01028b83aa1e28e53a42d86191d3",
        input={"image": open(file_path, "rb")}
    )
    print("Downloading...")
    download(str(output), out_f, out_file_name, True)


if __name__ == "__main__":
    try:
        while True:
            print("""\n
                [1] Image upscaler (REAL ESRGAN)
                [2] Text to image (SDXL)
                [3] Cartoonify (CARTOONIFY)
                [0] EXIT
            """)
            choice = input("\nEnter choice: ")
            if choice == "1":
                esrgan()
            elif choice == "2":
                sdxl()
            elif choice == "3":
                cartoonify()
            elif choice == "0":
                exit(0)
            else:
                print("Invalid Choice\n")
    except KeyboardInterrupt:
        print("\nInterrupt Detected..")
        time.sleep(1)
        exit(0)
