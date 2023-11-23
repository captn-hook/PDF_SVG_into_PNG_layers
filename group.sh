#this takes huge svg files (xml) and converts them to smaller svg files
#svgs are scoured already so structure is:
#  1|<?xml?>
#  2|<!-- inkscape comment -->
#  3|<svg>
#  4| <defs>
#  5|  <clipPath id="clipPath9999">
#  6|   <path>
#  7|  </clipPath>
#  ?|  ...
#100| </defs>
#101| <g>
#102| <path id="path9999" transform="matrix(1,0,0,1,0,0)" d="M 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 z" clip-path="url(#clipPath9999)" />
#  ?|  ...
#200| </g>
#201|</svg>

echo "working on directory $1, splitting to max size $2"
counter=0
for file in $1/*.svg
do
    echo $file
    echo $counter
    #wait for user input
    #read file
    data=$(cat $file)
    #split file into sections
    headersplit=$(grep -n '<def' $file | awk -F: '{print $1}')
    clipsplit=$(grep -n '</defs>' $file | awk -F: '{print $1}')
    transition=$(grep -n '<g' $file | awk -F: '{print $1}')
    pathsplit=$(grep -n '</g>' $file | awk -F: '{print $1}')
    footersplit=$(grep -n '</svg>' $file | awk -F: '{print $1}')

    clipsplit=$(($clipsplit - 1))
    pathsplit=$(($pathsplit - 1))

    #initialize variables
    header=""
    clippaths=""
    transition=""
    paths=""
    footer=""

    #put everything up to split into var
    for i in $(seq 1 $headersplit)
    do
        header=$header$(echo "$data" | sed -n "$i p")
    done
    for i in $(seq $headersplit $clipsplit)
    do
        clippaths=$clippaths$(echo "$data" | sed -n "$i p")
    done
    for i in $(seq $clipsplit $transition)
    do
        transition=$transition$(echo "$data" | sed -n "$i p")
    done
    for i in $(seq $transition $pathsplit)
    do
        paths=$paths$(echo "$data" | sed -n "$i p")
    done
    for i in $(seq $pathsplit $footersplit)
    do
        footer=$footer$(echo "$data" | sed -n "$i p")
    done

    echo "headersplit: $headersplit, clipsplit: $clipsplit, transitionsplit: $transition, pathsplit: $pathsplit, footersplit: $footersplit"
    #get lengths of all sections
    headerLength=$(echo "$header" | wc -l)
    clippathsLength=$(echo "$clippaths" | wc -l)
    transitionLength=$(echo "$transition" | wc -l)
    pathsLength=$(echo "$paths" | wc -l)
    footerLength=$(echo "$footer" | wc -l)

    echo "header length: $headerLength, clippaths length: $clippathsLength, transition length: $transitionLength, paths length: $pathsLength, footer length: $footerLength"

done