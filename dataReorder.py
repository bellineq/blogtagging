import csv, os, json, argparse
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def arg_parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('--user', default='user0', type=str, help='select user')
	parser.add_argument('--organize', action='store_true',help='')
	parser.add_argument('--count', action='store_true',help='')
	parser.add_argument('--alluser', action='store_true',help='')
	return parser.parse_args()
def category(filename):
	if 'movie' in filename: return 'movie'
	elif 'beauty' in filename: return 'beauty'
	elif 'tech' in filename: return 'tech'
	elif 'food' in filename: return 'food'

def csv_count(d, tag):
	count = [0,0,0,0,0,0]
	#root = ET.fromstring(d[tag])	
	soup = BeautifulSoup(d[tag], "html.parser")
	for mention in soup.find_all('mention'):
		#print(mention['score'])
		count[int(mention['score'])]+=1
	return [d['title'], count[5], count[4], count[3], count[2], count[1]]	
def word_count(article):
	soup = BeautifulSoup(article, "html.parser")
	return len(soup.find_all('word'))
def csv_write(data, filename):
	with open(filename, 'w', encoding='utf8') as f:
		w = csv.writer(f)
		w.writerows(data)
	return
		
args = arg_parse()
if args.alluser:
	workcsv = [['user','goal','tagging','tagged','left']]
	users = os.listdir(os.path.join(os.getcwd(), 'userData/'))
	for user in users:
		if not user.startswith('user'): continue
		total = 0
		progress = 0
		done = 0
		#abandoned = 0
		files = os.listdir(os.path.join(os.getcwd(), 'userData/'+user))
		for filename in files:
			if not filename.endswith('.json'): continue
			with open('userData/'+user+'/'+filename, 'r',encoding='utf8') as f: data = json.load(f)
			total+=len(data)
			for d in data:
				if d['status']=='tagged': done+=1
				elif d['status']=='tagging': progress+=1 
				#elif d['status']=='abandoned': abandoned+=1
		workcsv.append([user,total,progress,done,total-done])
		with open('alluser_status.csv', 'w', encoding='utf8') as f:
			w = csv.writer(f)
			w.writerows(workcsv)
elif args.count:
	files = os.listdir(os.path.join(os.getcwd(), 'userData/done/first_stage'))
	abd_csv = [['category','average_chars_per_abandoned_article','average_chars_per_tagged_article','abandoned_ratio']]
	for filename in files:
		print(filename)
		csv_w = [['title','five','four','three','two','one']]
		csv_s = [['title','five','four','three','two','one']]
		with open('userData/done/first_stage/'+filename, 'r') as f: data = json.load(f)
		tagged_words = 0
		tagged_n = 0
		abandoned_words = 0
		abandoned_n = 0
		for d in data:
			if d['status']=='tagged':
				tagged_words+=word_count(d['content_w'])
				tagged_n+=1
				csv_w.append(csv_count(d, 'content_w'))
				csv_s.append(csv_count(d, 'content_s'))
			elif d['status']=='abandoned':
				abandoned_words+=word_count(d['content_w'])
				abandoned_n+=1
		abd_csv.append([category(filename), abandoned_words/abandoned_n, tagged_words/tagged_n, abandoned_n/len(data)])
		csv_write(csv_s, category(filename)+'_done_sentence_gereralInfo.csv')
		csv_write(csv_w, category(filename)+'_done_word_gereralInfo.csv')
	csv_write(abd_csv, 'abandoned_analysis.csv')
else:
	files = os.listdir(os.path.join(os.getcwd(), 'userData/'+args.user))
	done_path = 'userData/done/first_stage/'

	for filename in files:
		if not filename.endswith('.json'): continue
		print(filename)
		with open('userData'+'/'+args.user+'/'+filename, 'r') as f: userData = json.load(f)
		if args.organize:
			print(done_path+category(filename)+'.json')
			with open(done_path+category(filename)+'.json', 'r') as f: data = json.load(f)
			for d in userData: 
				d['annotator'] = args.user
				data.append(d)
			with open(done_path+category(filename)+'.json', 'w') as f: json.dump(data,f)
