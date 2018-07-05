import json, argparse

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str)
    parser.add_argument('--newfile', type=str)
    parser.add_argument('--num', type=int)
    args   = parser.parse_args()
    return args

def GetArticles(filename):
    articles = []
    with open(filename, 'r') as json_data:
        file = json.load(json_data)

    # goal: get all names of untagged articles.
    for idx in range(len(file)):
        if file[idx]['status'] == 'untagged':
            articles.append(file[idx])
    return articles 


def SaveArticles(filename, articles, num):
    with open(filename, 'w') as json_data:
        json.dump(articles[0:num], json_data)

    return articles[0:num]

def DeleteArticles(filename, articles):
    updated_articles = []
    with open(filename, 'r') as origin_json_data:
        origin_file  = json.load(origin_json_data)

    for idx in range(len(origin_file)):
        if origin_file[idx] not in articles:
            updated_articles.append(origin_file[idx])

    with open(filename, 'w') as updated_json_data:
        json.dump(updated_articles, updated_json_data)


if __name__ == '__main__':
    args          = arg_parse()
    filename      = args.file
    save_filename = args.newfile
    num_to_update = args.num
    all_articles = GetArticles(filename)
    should_be_delete_articles = SaveArticles(save_filename, all_articles, num_to_update)
    DeleteArticles(filename, should_be_delete_articles)



