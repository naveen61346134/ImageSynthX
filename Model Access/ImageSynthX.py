import os
from time import sleep
from webbrowser import open as webopen
from subprocess import Popen
try:
    from colorama import Fore, Style
except ImportError:
    print("colorama package not installed\nRun the installer")
    sleep(2)
    exit(0)
try:
    from wget import download
    from replicate import run
except ImportError:
    print(Fore.RED + "\t\t Error Loading Packages\n\t\tRun the installer")
    sleep(1)
    exit(0)
try:
    from banners import main_banner, credits_banner, anything_banner, lcm_banner, sdxl_banner, esrgan_banner, images_banner
except ImportError:
    print(Style.BRIGHT + Fore.RED + "\t\tError in banners file")
    sleep(2)
    exit(0)

dir_path = os.getcwd()


def program_init():
    try:
        with open("token.txt", "r") as t:
            token = t.readline()
        if len(token) <= 10:
            print(Fore.RED + "\t\tINVALID TOKEN")
            sleep(2)
            exit(0)
        else:
            os.environ["REPLICATE_API_TOKEN"] = f"{token}"
    except FileNotFoundError:
        print(Fore.RED + "\t\tTOKEN FILE NOT FOUND!")
        sleep(1)
        exit(0)
    if not os.path.exists("Output"):
        os.system("mkdir Output")
        print(Fore.CYAN + "Output folder has been created!")


def download(url, out_f, out_file_name, png_check):
    download(str(url), out=out_f)
    if png_check == True:
        file_ext = f"\\Output\\{out_file_name}.png"
    else:
        file_ext = f"\\Output\\{out_file_name}.jpeg"
    exist = dir_path+file_ext
    if os.path.exists(exist):
        print("\nFile Created!")
        sleep(1)
        os.system("cls")
    else:
        print(Fore.RED + "\n\t\tERROR")
        sleep(1)
        os.system("cls")
    sleep(1.5)


def file_path_and_check(png):
    file_path = img_searcher()
    out_file_name = input(
        Fore.BLUE + "\t\tEnter output file name: " + Fore.CYAN)
    if not os.path.exists(file_path):
        print(Fore.RED + "\t\tFile doesnt exist!")
        sleep(1)
        exit(0)

    if png == True:
        out_f = dir_path + f"\\Output\\{out_file_name}.png"
    else:
        out_f = dir_path + f"\\Output\\{out_file_name}.jpeg"
    return file_path, out_f, out_file_name


def img_searcher():
    print("\n\n")
    print(images_banner)
    img_path = dir_path + "\\Output"
    extensions = [".png", ".jpg", ".jpeg"]
    images = os.listdir(img_path)

    for img in range(len(images)):
        for ext in extensions:
            if images[img].endswith(ext):
                if img < 9:
                    print(
                        Fore.CYAN + f"\t\t[0{img+1}]" + Fore.GREEN + f" {images[img]}")
                else:
                    print(
                        Fore.CYAN + f"\t\t[{img+1}]" + Fore.GREEN + f" {images[img]}")

    print(Style.BRIGHT + Fore.YELLOW + "\n\t\tEnter 'X' to go back to menu")
    choice = input(Fore.BLUE + "\t\tEnter choice: " + Fore.CYAN)
    try:
        if choice == "X" or choice == "x":
            loader()
        elif int(choice) <= len(images) and int(choice) != 0:
            file = f"{img_path}\\{images[int(choice)-1]}"
        elif int(choice) == 0:
            os.system("cls")
            print(Fore.RED + "\t\tInvalid Choice!")
            sleep(1)
            os.system("cls")
            esrgan()
        else:
            os.system("cls")
            print(Fore.RED + "\t\tInvalid Choice!")
            sleep(1)
            os.system("cls")
            esrgan()
    except ValueError:
        os.system("cls")
        print(Fore.RED + "\t\tInvalid Choice!")
        sleep(1)
        os.system("cls")
        esrgan()

    return file


def esrgan():
    print(esrgan_banner)
    file_path, out_f, out_file_name = file_path_and_check(True)
    try:
        upscale = int(
            input(Fore.BLUE + "\t\tEnter upscale value: " + Fore.CYAN))
    except ValueError:
        upscale = 2

    print(Fore.BLUE + "\t\tProcessing...")
    try:
        output = run(
            "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
            input={"image": open(file_path, "rb"), "upscale": upscale}
        )
    except Exception as e:
        if "NSFW" in str(e):
            print(Fore.RED + "\t\tNSFW Content Detected!")
            sleep(1)
            loader()
        elif "getaddrinfo" in str(e):
            print(Fore.RED + "\t\tNetwork Error!")
            sleep(1)
            exit(0)
        elif "CUDA" or "memory" in str(e):
            print(Fore.RED + "\t\tMODEL ERROR: CUDA OUT OF MEMORY!")
            sleep(1)
            loader()
        else:
            print(str(e))
            sleep(2)
            loader()
    print(Fore.MAGENTA + "\t\tDownloading...")
    download(str(output), out_f, out_file_name, True)


def sdxl():
    print(sdxl_banner)
    print(Style.BRIGHT + Fore.YELLOW + "\t\tEnter 'X' to go back to menu")
    prompt = input(Fore.BLUE + "\t\tEnter prompt for image: " + Fore.CYAN)
    if prompt == "X" or prompt == "x":
        loader()
    nPrompt = input(
        Fore.BLUE + "\t\tEnter the things to be avoided in the image: " + Fore.CYAN)
    if len(nPrompt) <= 0:
        nPrompt = ""
    out_file_name = input(
        Fore.BLUE + "\t\tEnter output file name: " + Fore.CYAN)
    try:
        width = int(input(Fore.BLUE + "\t\tEnter width: " + Fore.CYAN))
        wDiv8 = len(str(width/8).split(".")[1])
        if wDiv8 > 1:
            print(Fore.RED + "\t\tWidth should be divisible by 8")
            sleep(2)
            loader()
        height = int(input(Fore.BLUE + "\t\tEnter height: " + Fore.CYAN))
        lDiv8 = len(str(height/8).split(".")[1])
        if lDiv8 > 1:
            print(Fore.RED + "\t\tHeight should be divisible by 8")
            sleep(2)
            loader()
    except ValueError:
        width = 720
        height = 720
    print(Fore.BLUE + "\t\tProcessing...")
    try:
        output = run(
            "stability-ai/sdxl:8beff3369e81422112d93b89ca01426147de542cd4684c244b673b105188fe5f",
            input={"prompt": f"{prompt}", "negative_prompt": f"{nPrompt}", "width": width,
                   "height": height, "apply_watermark": False}
        )
    except Exception as e:
        if "NSFW" in str(e):
            print(Fore.RED + "NSFW Content Detected")
            sleep(1)
            loader()
        elif "getaddrinfo" in str(e):
            print(Fore.RED + "\t\tNetwork Error")
            sleep(1)
            exit(0)
        elif "CUDA" or "memory" in str(e):
            print(Fore.RED + "\t\tMODEL ERROR: CUDA OUT OF MEMORY")
            sleep(1)
            loader()
        else:
            print(str(e))

    out_f = dir_path + f"\\Output\\{out_file_name}.jpeg"
    print(Fore.MAGENTA + "\t\tDownloading...")
    download(str(output[0]), out_f, out_file_name, False)


def latent_consistency_model():
    print(lcm_banner)
    print(Style.BRIGHT + Fore.YELLOW + "\t\tEnter 'X' to go back to menu")
    prompt = input(Fore.BLUE + "\t\tEnter prompt for image: " + Fore.CYAN)
    if prompt == "X" or prompt == "x":
        loader()
    out_file_name = input(
        Fore.BLUE + "\t\tEnter output file name: " + Fore.CYAN)
    try:
        width = int(input(Fore.BLUE + "\t\tEnter width: " + Fore.CYAN))
        wDiv8 = len(str(width/8).split(".")[1])
        if wDiv8 > 1:
            print(Fore.RED + "\t\tWidth should be divisible by 8")
            sleep(2)
            loader()
        height = int(input(Fore.BLUE + "\t\tEnter height: " + Fore.CYAN))
        lDiv8 = len(str(height/8).split(".")[1])
        if lDiv8 > 1:
            print(Fore.RED + "\t\tHeight should be divisible by 8")
            sleep(2)
            loader()
    except ValueError:
        width = 720
        height = 720
    print(Fore.BLUE + "\t\tProcessing...")
    try:
        output = run(
            "luosiallen/latent-consistency-model:553803fd018b3cf875a8bc774c99da9b33f36647badfd88a6eec90d61c5f62fc",
            input={
                "prompt": f"{prompt}", "width": width, "height": height}
        )
    except Exception as e:
        if "NSFW" in str(e):
            print("\t\tNSFW Content Detected")
            sleep(1)
            loader()
        elif "getaddrinfo" in str(e):
            print(Fore.RED + "\t\tNetwork Error")
            sleep(1)
            exit(0)
        elif "CUDA" or "memory" in str(e):
            print(Fore.RED + "\t\tMODEL ERROR: CUDA OUT OF MEMORY")
            sleep(1)
            loader()
        else:
            print(str(e))
    out_f = dir_path + f"\\Output\\{out_file_name}.png"
    print(Fore.MAGENTA + "\t\tDownloading...")
    download(str(output[0]), out_f, out_file_name, True)


def anime_anything():
    print(anything_banner)
    print(Style.BRIGHT + Fore.YELLOW + "\t\tEnter 'X' to go back to menu")
    prompt = input(Fore.BLUE + "\t\tEnter prompt for image: " + Fore.CYAN)
    if prompt == "X" or prompt == "x":
        loader()
    out_file_name = input(
        Fore.BLUE + "\t\tEnter output file name: " + Fore.CYAN)
    try:
        width = int(input(Fore.BLUE + "\t\tEnter width: " + Fore.CYAN))
        wDiv8 = len(str(width/8).split(".")[1])
        if wDiv8 > 1:
            print(Fore.RED + "\t\tWidth should be divisible by 8")
            sleep(2)
            loader()
        height = int(input(Fore.BLUE + "\t\tEnter hieight: " + Fore.CYAN))
        lDiv8 = len(str(height/8).split(".")[1])
        if lDiv8 > 1:
            print(Fore.RED + "\t\tHeight should be divisible by 8")
            sleep(2)
            loader()
    except ValueError:
        width = 512
        height = 512
    print(Fore.BLUE + "\t\tProcessing...")
    try:
        output = run(
            "cjwbw/anything-v4.0:42a996d39a96aedc57b2e0aa8105dea39c9c89d9d266caf6bb4327a1c191b061",
            input={"prompt": prompt, "width": width, "height": height}
        )
    except Exception as e:
        if "NSFW" in str(e):
            print(Fore.RED + "\t\tNSFW Content Detected")
            sleep(1)
            loader()
        elif "getaddrinfo" in str(e):
            print(Fore.RED + "\t\tNetwork Error")
            sleep(1)
            exit(0)
        elif "CUDA" or "memory" in str(e):
            print(Fore.RED + "\t\tMODEL ERROR: CUDA OUT OF MEMORY")
            sleep(1)
            loader()
        else:
            print(str(e))
    print(Fore.MAGENTA + "\t\tDownloading...")
    out_f = dir_path + f"\\{out_file_name}.png"
    download(str(output[0]), out_f, out_file_name, True)


def PCredits():
    os.system("cls")
    print(credits_banner)
    sleep(2)
    loader()


def web_ui():
    file = "web-ui.py"
    if not os.path.exists(file):
        print(Style.BRIGHT + Fore.RED + "WEB UI File Not Found")
        sleep(2)
        exit(0)
    else:
        Popen(
            ["start", "cmd", "/c", "python", "web-ui.py", "True"], shell=True)
        sleep(2)
        webopen("http://127.0.0.1:5000")


def loader():
    try:
        os.system("cls")
        while True:
            print(main_banner)
            choice = input(Fore.BLUE + Style.BRIGHT +
                           "\n\t\tEnter choice: " + Fore.CYAN)
            if choice == "1":
                os.system("cls")
                web_ui()
            elif choice == "2":
                os.system("cls")
                esrgan()
            elif choice == "3":
                os.system("cls")
                sdxl()
            elif choice == "4":
                os.system("cls")
                latent_consistency_model()
            elif choice == "5":
                os.system("cls")
                anime_anything()
            elif choice == "C":
                PCredits()
            elif choice == "0":
                print(Fore.RED + "\t\tExiting..")
                sleep(1)
                os.system("cls")
                exit(0)
            else:
                print(Fore.RED + "\t\tInvalid Choice\n")
                sleep(1)
                os.system("cls")
    except KeyboardInterrupt:
        print(Fore.RED + "\n\t\tKeyboard Interrupt Detected..")
        sleep(1)
        os.system("cls")
        exit(0)


program_init()
loader()
