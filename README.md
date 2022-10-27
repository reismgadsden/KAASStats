# KAAS Stats
By: Reis Gadsden
<a href="https://github.com/reismgadsden/KAASStats">Github</a>

---

## Introduction
KAAS Stats is a program to visualize BRITE hierarchies JSON files returned by KAAS job.

---

## Requirements
* Python
    * sys
    * getopt
    * re
    * json
    * numpy
    * warnings
    * matplotlib

## Initial Run
Running the KAASStats is done via a terminal. Below is a minimal run of the program. 
```
$> python KAASStats.py -i <input.json>
```
There are also several additional command line options available to help customize your graph below.

## Command Line Flags
#### -h/--help
Prints out the following string to the console.
```
$> python KAASStats.py -h

KAASStats.py -i/--input <inputfile.json>
Optional Arguments:
        -n/--name - <String> Name of the output file (Default: input file name appended with '_bar')
        -t/--top - <Int> Maximum number of bars to display (Default: 5)
        -s/--step - <Int> The scale of the y-axis (Default: 1)
        -b/--bin - <Float> The width of the bars (Default : 0.8)
        -g/--title - <String> The title of the graph (Default: '')
        -z/--no-title <None> This will remove the title from the graph. This flag requires no arguments
        -x/--indv-names <None> This will group hits by individual hits instead of by family. This flag requires no arguments
For more info on these flags please refer to the documentation: https://github.com/reismgadsden/KAASStats

```

#### -i/--input
*String* - Name of the input file.

#### -n/--name *(Default: input file name appended with '_bar')*
*String* - Name of the output file.

#### -t/--top *(Default: 5)*
*Int* - Maximum number of bars to display.
*Note: Total number of bars can be less then specified value if there is not enough hits.*

#### -s/--step *(Default: 1)*
*Int* - Y-axis scale.

#### -b/--bin *(Default: 0.8)*
*Float* - Width of the bars.

#### -g/--title *(Default: "")*
*String* - Choose a custom title for the plot. If the default is left, then the title is simply, *Hits per BRITE KO*.
*Note: Please encapsulate your title in quotes as if it contains any spaces the title will not be correct.*

#### -z/--no-title *(No Argument)*
If this flag is passed then the final plot will not have a title.

#### -x/--indv-names *(No Argument)*
If this flag is set it will choose the individual transcript KO names instead of its families name. For example with the following excerpt from a KAAS job:
```
.
.
.
{
    "name":"MAPK family [OT]",
        "children":[
			{
			    "name":"TRINITY_DN12702_c0_g1_i1; K04371  ERK, MAPK1_3; mitogen-activated protein kinase 1\/3 [EC:2.7.11.24]"
                        },
.
.
.
```
If the flag is not passed the title of the bar will be, *MAPK family [OT]*. However if the flag is passed the name will be *ERK, MAPK1_3; mitogen-activated protein kinase 1/3*.
*Note: Setting this flag will change both how your graph looks and the total number of counts for each bar.*