import json, csv


InfoData = []
with open('data/food.json') as json_data:
    data = json.load(json_data)
    for idx in range(len(data)):
        InfoData.append([data[idx]['title'], data[idx]['view_count'], data[idx]['word_count']])

with open('data/food.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['title', 'view_count', 'word_count'])
    for idx in range(len(InfoData)):
        csvwriter.writerow([InfoData[idx][0], InfoData[idx][1], InfoData[idx][2] ])

