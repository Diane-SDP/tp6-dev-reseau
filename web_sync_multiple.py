import sys
import requests
import time

start_time = time.time()

f = open(sys.argv[1], "r")
content = f.read()
urls = content.split("\n")

def get_content(url) :
    x = requests.get(url)
    return x.content.decode()

def write_content(content, file) :
        f = open(file, "w+", encoding="utf-8")
        f.write(content)
        f.close()

for elt in urls :
    name = str(elt).split("/")[2]
    write_content(get_content(elt), f"./tmp/web_{name}")

print("--- %s seconds ---" % (time.time() - start_time))