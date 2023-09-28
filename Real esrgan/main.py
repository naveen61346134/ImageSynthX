import os
import wget
import time
import replicate

with open("token.txt", "r") as t:
    token = t.readlines()
os.environ["REPLICATE_API_TOKEN"] = f"{token[0]}"
dir_path = os.getcwd()


def esrgan():
    file_path = input("Enter complete file path: ")
    out_file_name = input("Enter output file name: ")
    if os.path.exists(file_path):
        pass
    else:
        print("File doesnt exist!")
        exit(1)

    print("Processing...")
    output = replicate.run(
        "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
        input={"image": open(file_path, "rb"), "face_enhance": True}
    )
    out_f = dir_path + f"\\{out_file_name}.jpeg"
    wget.download(str(output), out=out_f)
    if os.path.exists(f"{out_file_name}.jpeg"):
        print("\nFile Created!")
    else:
        print("\nERROR")
    time.sleep(2)


def sdxl():
    prompt = input("Enter prompt for image: ")
    out_file_name = input("Enter output file name: ")
    width = int(input("Enter width: "))
    height = int(input("Enter hieight: "))
    output = replicate.run(
        "stability-ai/sdxl:8beff3369e81422112d93b89ca01426147de542cd4684c244b673b105188fe5f",
        input={"prompt": f"{prompt}", "width": width, "height": height, "apply_watermark": False}
    )
    out_f = dir_path + f"\\{out_file_name}.jpeg"
    wget.download(str(output[0]), out=out_f)
    if os.path.exists(f"{out_file_name}.jpeg"):
        print("\nFile created!")
    else:
        print("\nERROR")
    time.sleep(2)

if __name__ == "__main__":
    while True:
        print("""\n
            [1] Image upscaler (REAL ESRGAN)
            [2] Text to image (SDXL)
            [0] EXIT
        """)
        choice = input("\nEnter choice: ")
        if choice == "1":
            esrgan()
        elif choice == "2":
            sdxl()
        elif choice == "0":
            exit(0)
        else:
            print("Invalid Choice\n")
