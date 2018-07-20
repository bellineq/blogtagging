from os import listdir
from os.path import isfile, join
import json, argparse

# print information of files.
def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', default='', type=str)
    args = parser.parse_args()
    return args

def GetInfo(nameoffiles, path):
    for file_id in range(len(nameoffiles)):
        bad_article      = 0
        finished_article = 0
        with open(path+nameoffiles[file_id], 'r') as file:
            data = json.load(file)
        for data_id in range(len(data)):
            if data[data_id]['status'] == 'abandoned':
                bad_article += 1
            elif data[data_id]['status'] == 'tagged':
                finished_article += 1
        print("filename: ", nameoffiles[file_id])
        print("total number of articles: ", len(data))
        print("portion of bad article: ", bad_article/len(data))
        print("portion of finished article: ", finished_article/len(data))
        print("============")



if __name__ == '__main__':
    args   = arg_parse()
    mypath = './userData/' + args.user + '/'
    Namesofiles = [f for f in listdir(mypath) if f.endswith('.json')]
    GetInfo(Namesofiles, mypath)

