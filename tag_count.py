import json, argparse

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='', type=str, help='file of product list')
    return parser.parse_args()

tagged = 0
untagged = 0
args = arg_parse()
with open(args.file, 'r') as f: data = json.load(f)
for d in data:
    if d['status']=='untagged': untagged+=1
    else: tagged+=1

print('tagged: {}, untagged: {}'.format(tagged, untagged))
