from os import listdir
from os.path import isfile, join
import json, argparse, csv

# get the link and title of the annotation file.
def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', default='', type=str)
    args = parser.parse_args()
    return args

def GetInfo(path, json_name, csv_name):
    with open(path + json_name, 'r') as json_file:
        data = json.load(json_file)
    with open(path + csv_name, 'w') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow(['link', 'title'])
        for data_id in range(len(data)):
            csvwriter.writerow([data[data_id]['link'], data[data_id]['title']])


if __name__ == '__main__':
    args        = arg_parse()
    originpath  = './data/nonsep/'
    jsonname    = args.type + '.json'
    csvname     = args.type + '.csv'
    GetInfo(originpath, jsonname, csvname)