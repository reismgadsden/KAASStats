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

    output_file = ""
    output_file_regex = r"^[\w\-. ]+$"

    try:
        opts, args = getopt.getopt(argv, "hi:t:n:", ["input=", "top=", "name=", "help="])
    except getopt.GetoptError:
        print("KAASStats.py -i <inputfile.json> -t # -n outfile_name")
        sys.exit(2)
    if (("-i" not in argv and "--input" not in argv) ^ ("-t" not in argv and "--top" not in argv)) \
            and ("-h" not in argv and "--help" not in argv):
        print("KAASStats.py -i <inputfile.json> -t # -n outfile_name\n\t" +
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
        elif opt in ("-n", "--name"):
            if re.fullmatch(output_file_regex, arg):
                output_file = arg
            else:
                print("-n/--name must be a valid file name conforming to pattern: ^[\w\-. ]+$")
                exit(2)

    ko_counts = read_brite(input_file)
    build_graph(ko_counts, top_trans, input_file.replace(".json", ""), output_file)


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
                if head["name"] in ko_dict:
                    ko_dict[head["name"] + "_a"] = len(head["children"])
                else:
                    ko_dict[head["name"]] = len(head["children"])


def build_graph(ko_counts, top, in_file, out_name=""):
    ko_counts_sorted = dict(sorted(ko_counts.items(), key=lambda item: item[1], reverse=True))

    ko_name = list(ko_counts_sorted.keys())[:top]
    ko_count = list(ko_counts_sorted.values())[:top]

    #fig, ax = plt.subplots()

    plt.suptitle("Hits per BRITE KO: Transporters")
    plt.xlabel("BRITE Name")
    plt.ylabel("# of hits")
    plt.ylim(0, max(ko_count) + 1)
    plt.yticks(numpy.arange(0, max(ko_count) + 2))

    plt.bar(ko_name, ko_count, width=0.4, color="black")
    plt.xticks(rotation=45, ha="right", size="small")

    plt.tight_layout()

    if out_name == "":
        plt.savefig(in_file + "_bar.png")
        return
    plt.savefig(out_name + ".png")

if __name__ == "__main__":
    main(sys.argv[1:])