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
import warnings


def main(argv) -> None:
    input_file = ""
    input_regex = r"^(.)*\.json$"

    top_trans = 5
    top_regex = r"^[0-9]+$"

    output_file = ""
    output_file_regex = r"^[\w\-. ]+$"

    step = 1

    title = ""

    no_title = False

    bin_regex = r"^[0-9]*\.[0-9]+$"
    bin = 0.8

    indv_names = False

    try:
        opts, args = getopt.getopt(argv, "hzxi:t:n:s:g:b:", ["input=", "top=", "name=", "help=", "step=", "title=", "no-title=", "bin=", "indv-names="])
    except getopt.GetoptError:
        print("KAASStats.py -i <inputfile.json> -t # -n outfile_name")
        sys.exit(2)
    if ("-i" not in argv and "--input" not in argv)  and ("-h" not in argv and "--help" not in argv):
        print("KAASStats.py -i/--input <inputfile.json>\nOptional Arguments:\n\t"
              "-h/--help - Displays this help menu"
              "-n/--name - <String> Name of the output file (Default: input file name appended with '_bar')\n\t"
              "-t/--top - <Int> Maximum number of bars to display (Default: 5)\n\t"
              "-s/--step - <Int> The scale of the y-axis (Default: 1)\n\t"
              "-b/--bin - <Float> The width of the bars (Default : 0.8)\n\t"
              "-g/--title - <String> The title of the graph (Default: '')\n\t"
              "-z/--no-title <None> This will remove the title from the graph. This flag requires no arguments\n\t"
              "-x/--indv-names <None> This will group hits by individual hits instead of by family. This flag requires no arguments\n"
              "For more info on these flags please refer to the documentation: https://github.com/reismgadsden/KAASStats")
        exit(-1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("KAASStats.py -i/--input <inputfile.json>\nOptional Arguments:\n\t"
                  "-h/--help - Displays this help menu"
                  "-n/--name - <String> Name of the output file (Default: input file name appended with '_bar')\n\t"
                  "-t/--top - <Int> Maximum number of bars to display (Default: 5)\n\t"
                  "-s/--step - <Int> The scale of the y-axis (Default: 1)\n\t"
                  "-b/--bin - <Float> The width of the bars (Default : 0.8)\n\t"
                  "-g/--title - <String> The title of the graph (Default: '')\n\t"
                  "-z/--no-title <None> This will remove the title from the graph. This flag requires no arguments\n\t"
                  "-x/--indv-names <None> This will group hits by individual hits instead of by family. This flag requires no arguments\n"
                  "For more info on these flags please refer to the documentation: https://github.com/reismgadsden/KAASStats")
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
        elif opt in ("-s", "--step"):
            if re.fullmatch(top_regex, arg) and int(arg.strip().replace(" ", "").replace("\n", "").replace("\r", "")) > 0:
                step = int(arg.strip().replace(" ", "").replace("\n", "").replace("\r", ""))
            else:
                print("-s/--step argument must be a positive integer")
                sys.exit(2)
        elif opt in ("-b", "--bin"):
            if re.fullmatch(bin_regex, arg) and float(arg.strip().replace(" ", "").replace("\n", "").replace("\r", "")) > 0:
                bin = float(arg.strip().replace(" ", "").replace("\n", "").replace("\r", ""))
            else:
                #print(re.fullmatch(bin_regex, arg))
                print("-b/--bin argument must be a positive floating point number")
                sys.exit(2)
        elif opt in ("-g", "title"):
            title = arg.strip().replace("\n", "").replace("\r", "")
        elif opt in ("-z", "--no-title"):
            no_title = True
        elif opt in ("-x", "indv-names"):
            indv_names = True

    ko_counts = read_brite(input_file, indv_names)
    build_graph(ko_counts, top_trans, input_file.replace(".json", ""), output_file, step=step, title=title, no_title=no_title, bin=bin)


def read_brite(infile, indv_names) -> dict:
    brite = ""

    try:
        with open(infile) as json_file:
            brite = json.load(json_file)
    except FileNotFoundError:
        print("File, \"" + infile + "\" does not exist.")
        sys.exit(2)

    ko_counts = dict()
    if not indv_names:
        deconstruct_json(ko_counts, brite["children"])
    else:
        deconstruct_json_indv(ko_counts, brite["children"])
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


def deconstruct_json_indv(ko_dict, brite):
    pattern = r"[EC:[0-9\.\s\-]*]"
    for head in brite:
        if "children" in head:
            deconstruct_json_indv(ko_dict, head["children"])
            if "children" not in head["children"] and re.fullmatch(r"^TRINITY_.*$", head["children"][0]["name"]):
                for name in head["children"]:
                    split_name = re.sub(pattern, ""," ".join(name["name"].split(" ")[3:])).strip()
                    if split_name in ko_dict:
                        ko_dict[split_name] += 1
                    else:
                        ko_dict[split_name] = 1


def build_graph(ko_counts, top, in_file, out_name="", step=1, title="", no_title=False, bin=0.8):
    ko_counts_sorted = dict(sorted(ko_counts.items(), key=lambda item: item[1], reverse=True))

    ko_name = list(ko_counts_sorted.keys())[:top]
    ko_count = list(ko_counts_sorted.values())[:top]

    #fig, ax = plt.subplots()
    if not no_title:
        if title != "":
            title = ": " + title
        plt.suptitle("Hits per BRITE KO" + title)
    #plt.xlabel("BRITE Name")
    plt.ylabel("# of hits")

    plt.bar(ko_name, ko_count, width=bin, color="black")
    plt.xticks(rotation=45, ha="right", size="small")

    plt.autoscale()
    plt.ylim(0, max(ko_count) + 1)
    plt.yticks(numpy.arange(0, max(ko_count) + 2, step))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        plt.tight_layout()

    if out_name == "":
        plt.savefig(in_file + "_bar.png", bbox_inches="tight")
        return
    plt.savefig(out_name + ".png")

if __name__ == "__main__":
    main(sys.argv[1:])