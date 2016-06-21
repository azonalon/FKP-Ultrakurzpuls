#!/bin/sh
for file in *.ods
do
    # ssconvert -T "Gnumeric_stf:stf_assistant"  \
    #     -O 'format=raw quoting-mode=always quoting-on-whitespace=FALSE separator=","' \
    #     $file
    # ssconvert -T "Gnumeric_OpenCalc:openoffice:stf_csv" $file
    soffice --convert-to csv $file
done
