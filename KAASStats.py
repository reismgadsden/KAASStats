"""
This program will break down BRITE hierarchies created by KAAS (KEGG Automatic Annotation Server)

author: Reis Gadsden 17-08-2022
version: 17-08-2022
last modified: Reis Gadsden 17-08-2022
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
    build_graph(ko_counts)


def read_brite(infile) -> dict:
    brite = ""

    try:
        with open(infile) as json_file:
            brite = json.load(json_file)
    except FileNotFoundError:
        print("File, \"" + infile + "\" does not exist.")
        sys.exit(2)

    ko_counts = dict()

    for head in brite["children"]:
        for sub in head["children"]:
            if "children" in sub:
                ko_counts[sub["name"]] = len(sub["children"])
    return ko_counts




def build_graph(ko_counts):
    pass



if __name__ == "__main__":
    main(sys.argv[1:])