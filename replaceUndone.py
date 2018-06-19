from os import listdir
from os.path import isfile, join
import json, argparse, pdb

# show files in 'done' folder
# mypath = '/Users/kenkao70508/github_files/mymy/userData/user0'
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# files = [f for f in listdir(mypath) if f.endswith('.json')]

DoneData = []

def arg_parse():
    parser = argparse.ArgumentParser()
    # check file
    parser.add_argument('--user', type=str)
    args = parser.parse_args()
    return args

def GetListofFiles(username):
    done_path = '/Users/kenkao70508/github_files/mymy/userData/done'
    check_path = '/Users/kenkao70508/github_files/mymy/userData/'+ username
    done_list = [f for f in listdir(done_path) if f.endswith('.json')]
    check_list = [f for f in listdir(check_path) if f.endswith('.json')]
    return done_list, check_list

def GetDoneData(list_of_files, name):
    global DoneData
    for idx in range(len(list_of_files)):
        filename = list_of_files[idx]
        with open('./userData/done/'+filename, 'r') as file:
            data = json.load(file)
        DoneData += data

def ReplaceUndoneData(list_of_files, name):
    global DoneData
    
    for name_idx in range(len(list_of_files)):
        with open('./userData/'+ name+ '/' + list_of_files[name_idx] , 'r') as check:
            check_data = json.load(check)
            replaced_check_data = list(check_data)
        # pdb.set_trace()
        for idx in range(len(check_data)):
            for idx_j in range(len(DoneData)):
                if check_data[idx]['link'] == DoneData[idx_j]['link']:
                    replaced_check_data.remove(check_data[idx])


        with open('./userData/'+ name+ '/' + list_of_files[name_idx], 'w') as done_check:
            json.dump(replaced_check_data, done_check)

if __name__ == '__main__':
    args = arg_parse()
    done_list_filenames, check_list_filenames = GetListofFiles(args.user)
    GetDoneData(done_list_filenames, args.user)
    ReplaceUndoneData(check_list_filenames, args.user)