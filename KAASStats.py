"""
This program will break down BRITE hierarchies created by KAAS (KEGG Automatic Annotation Server)

author: Reis Gadsden 17-08-2022
version: 21-09-2022
last modified: Reis Gadsden 21-09-2022
github: https://github.com/reismgadsden/KAASStats
"""
import sys
import getopt
import re
import json
import numpy
import matplotlib.pyplot as plt


def main(argv) -> None:
    input_file = ""
    input_regex = r"^(.)*\.json$"

    top_trans = 0
    top_regex = r"^[0-9]+$"

    try:
        opts, args = getopt.getopt(argv, "hi:t:", ["input=", "top=", "help="])
    except getopt.GetoptError:
        print("KAASStats.py -i <inputfile.json> -t #")
        sys.exit(2)
    if (("-i" not in argv and "--input" not in argv) ^ ("-t" not in argv and "--top" not in argv)) \
            and ("-h" not in argv and "--help" not in argv):
        print("KAASStats.py -i <inputfile.json> -t #\n\t" +
              "KAASStats.py --input <inputfile.json> --top #\n\t" +
              "KAASStats.py -h\n\tKAASStat.py --help")

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("KAASStats.py -i <inputfile.json> -t #")
            sys.exit()
        elif opt in ("-i", "--input"):
            if re.fullmatch(input_regex, arg):
                input_file = arg
            else:
                print("Input file must be a .json")
                sys.exit(2)
        elif opt in ("-t", "--top"):
            if re.fullmatch(top_regex, arg) and int(arg.strip().replace(" ", "").replace("\n", "").replace("\r", "")) > 0:
                top_trans = int(arg.strip().replace(" ", "").replace("\n", "").replace("\r", ""))
            else:
                print("-t/--top argument must be a positive integer")
                sys.exit(2)

    ko_counts = read_brite(input_file)
    build_graph(ko_counts, top_trans)


def read_brite(infile) -> dict:
    brite = ""

    try:
        with open(infile) as json_file:
            brite = json.load(json_file)
    except FileNotFoundError:
        print("File, \"" + infile + "\" does not exist.")
        sys.exit(2)

    ko_counts = dict()

    deconstruct_json(ko_counts, brite["children"])

    return ko_counts


def deconstruct_json(ko_dict, brite):
    for head in brite:
        if "children" in head:
            deconstruct_json(ko_dict, head["children"])
            if "children" not in head["children"] and re.fullmatch(r"^TRINITY_.*$", head["children"][0]["name"]):
                ko_dict[head["name"]] = len(head["children"])


def build_graph(ko_counts, top):
    ko_counts_sorted = dict(sorted(ko_counts.items(), key=lambda item: item[1], reverse=True))

    ko_name = list(ko_counts_sorted.keys())[:top]
    ko_count = list(ko_counts_sorted.values())[:top]

    fig = plt.figure(figsize=(10,5))

    plt.bar(ko_name, ko_count, width=0.4)

    plt.show()
    pass

if __name__ == "__main__":
    main(sys.argv[1:])