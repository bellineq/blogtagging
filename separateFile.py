#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, argparse, csv

def arg_parse():
    parser = argparse.ArgumentParser()
    # separate target: 'type'.json
    parser.add_argument('--type', type=str)
    # separate to 'number' of files.
    parser.add_argument('--num', type=int)
    args = parser.parse_args()
    return args

def GetData(type_name, sep_num):
    with open ('data/'+type_name+'.json', 'r') as json_data:
        origin = json.load(json_data)
    total_length = len(origin)
    single_length = int(total_length/sep_num)
    return origin, single_length

def SepData(ta_data, single_len, num_file):
    origin_length = len(ta_data)
    for idx in range(num_file):
        with open('data/'+ type_name+ '_'+ idx+ '.json', 'w') as file:
            if (idx+1)*single_len < origin_length:
                json.dump(ta_data[idx*single_len: (idx+1)*single_len], file)
            else:
                json.dump(ta_data[idx*single_len::], file)


if __name__ == '__main__':
    args = arg_parse()
    target, length = GetData(args.type, args.num)
    SepData(target, length, args.num)