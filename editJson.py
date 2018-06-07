import json
dataList = ['all3C', 'allarts', 'allastrology', 'alldesign', 'allentertain',
'allfamily', 'allfashion', 'alllearn', 'alllife', 'allmoods', 'allpics',
'allpolitics', 'allsports', 'alltravel1', 'alltravel2', 'food1', 'food2']
dataList = ['all3C', 'allfashion', 'alllife','food1','food2']
# dataList = ['alldesign','beautymakeup','food','moviecritics']
dataList = ['food','threec','moviecritics']
user = 'user1'

for cat in dataList:
    # datapath = 'data/'+cat+'.json'
    datapath = 'userData/'+user+'/'+cat+'.json'
    with open(datapath, 'r') as json_data:
        data = json.load(json_data)

    # for i in data:
    #     i['id'] = i['id'].split('-')[0]
    #     print (i['id'].split('-')[0])
    
    # with open(datapath, 'w') as output:
    #     json.dump(data, output)