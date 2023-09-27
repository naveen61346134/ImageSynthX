import os
import wget
import time
import replicate

token = ""
with open("token.txt", "r") as t:
    token = t.readlines()
os.environ["REPLICATE_API_TOKEN"] = f"{token[0]}"

dir_path = os.getcwd()
file_path = input("Enter complete file path: ")
if os.path.exists(file_path):
    pass
else:
    print("File doesnt exist!")
    exit(1)

print("Processing...")
output = replicate.run(
    "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
    input={"image": open(file_path, "rb")}
)
out_f = dir_path + "\output.jpeg"
wget.download(str(output), out=out_f)
if os.path.exists("output.jpeg"):
    print("\nFile Created!")
else:
    print("\nERROR")

time.sleep(2)
