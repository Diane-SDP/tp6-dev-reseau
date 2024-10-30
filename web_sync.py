import sys
import requests

host = sys.argv[1]

def get_content(url) :
    x = requests.get(url)
    return x.content.decode()

def write_content(content, file) :
        f = open(file, "w+", encoding="utf-8")
        f.write(content)
        f.close()

write_content(get_content(host), "/tmp/web_page")