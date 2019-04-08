import csv
import os
import sys
csv.field_size_limit(sys.maxsize)
def text_to_csv(file):
    txt_file = file
    csv_file = file[:-4]+".csv"
    filename = csv_file
    if os.path.exists(filename):
        os.remove(filename)
    in_txt = csv.reader(open(txt_file, "rb"), delimiter='\t')
    out_csv = csv.writer(open(csv_file, 'wb'))
    out_csv.writerows(in_txt)
    print ("text to csv writing done!")
def frange(start, stop, step):
    i = start
    ls=[]
    while i < stop:
        ls.append(i)
        i += step
    return ls