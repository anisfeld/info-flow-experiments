import sys
import re
sys.path.append("../core")          # files from the core
import converter.reader             # read log and create feature vectors
import argparse

log_file = "16blocks.gender.search.log.txt"

urls = converter.reader.pull_url_from_log(log_file)

def filter_url(url):
    if not re.search("google", url):
        return re.sub("\?Nao=.*|\?sh=.*", "", url)

for key in urls.keys():

    treatment_urls = {filter_url(u) for u in urls[key] if filter_url(u)}

    out_file = "./site_files/womens_links.txt"
    if key == "0":
        out_file = "./site_files/mens_links.txt"

    fo = open(out_file, "w")
    for url in treatment_urls:
        fo.write(url + "\n")

