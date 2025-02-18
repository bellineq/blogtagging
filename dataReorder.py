import csv, os, json, argparse
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def arg_parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('--user', default='user0', type=str, help='select user')
	parser.add_argument('--n_user', default=1, type=int, help='select user')
	parser.add_argument('--organize', action='store_true',help='')
	parser.add_argument('--count', action='store_true',help='')
	parser.add_argument('--alluser', action='store_true',help='')
	return parser.parse_args()
def category(filename):
	if 'movie' in filename: return 'movie'
	elif 'beauty' in filename: return 'beauty'
	elif 'tech' in filename: return 'tech'
	elif 'food' in filename: return 'food'

def csv_count(d):
	result = [d['title']]
	for tag in ['content_w','content_s']:
		count = [0,0,0,0,0,0]
		#root = ET.fromstring(d[tag])	
		soup = BeautifulSoup(d[tag], "html.parser")
		for mention in soup.find_all('mention'):
			#print(mention['score'])
			count[int(mention['score'])]+=1
		for i in range(5,0,-1): result.append(count[i])
	return result
def tag_count(article):
	soup = BeautifulSoup(article, "html.parser")
	return len(soup.find_all('mention'))
def csv_write(data, filename):
	with open(filename, 'w', encoding='utf8') as f:
		w = csv.writer(f)
		w.writerows(data)
	return
		
args = arg_parse()
if args.alluser:
	workcsv = [['user','goal','tagging','tagged','left']]
	for i in range(args.n_user+1):
		user = 'user'+str(i)
		goal = 50
		progress = 0
		done = 0
		#abandoned = 0
		files = os.listdir(os.path.join(os.getcwd(), 'userData/'+user))
		for filename in files:
			if not filename.endswith('.json'): continue
			with open('userData/'+user+'/'+filename, 'r',encoding='utf8') as f: data = json.load(f)
			for d in data:
				if d['status']=='tagged': done+=1
				elif d['status']=='tagging': progress+=1 
				#elif d['status']=='abandoned': abandoned+=1
		workcsv.append([user,goal,progress,done,goal-done])
		with open('alluser_status.csv', 'w', encoding='utf8') as f:
			w = csv.writer(f)
			w.writerows(workcsv)
elif args.count:
	done_path = '../blogtagging_done/first_stage/'
	files = os.listdir(os.path.join(os.getcwd(), done_path))
	abd_csv = [['category','average_chars_per_abandoned_article','average_chars_per_tagged_article','abandoned_ratio']]
	total_csv = [['category','done_articles','tagged_sentences','sentence_five','sentence_four','sentence_three','sentence_two','sentence_one','tagged_words','word_five','word_four','word_three','word_two','word_one']]
	for filename in files:
		print(filename)
		csv = [['title','sentence_five','sentence_four','sentence_three','sentence_two','sentence_one','word_five','word_four','word_three','word_two','word_one']]
		with open(done_path+filename, 'r') as f: data = json.load(f)
		tagged_w = 0
		tagged_s = 0
		tagged_n = 0
		abandoned_words = 0
		abandoned_n = 0
		
		for d in data:
			print(d['id'], d['status'])
			if d['status']=='tagged':
				tagged_w+=tag_count(d['content_w'])
				tagged_s+=tag_count(d['content_s'])
				tagged_n+=1
				c = csv_count(d)
				csv.append(c)
			elif d['status']=='abandoned':
				abandoned_words+=count(d['content_w'])
				abandoned_n+=1
		total_csv.append([category(filename), tagged_n, tagged_s, ])
		abd_csv.append([category(filename), abandoned_words/abandoned_n, tagged_words/tagged_n, abandoned_n/len(data)])
		csv_write(csv, category(filename)+'_done_gereralInfo.csv')
	csv_write(abd_csv, 'abandoned_analysis.csv')
	csv_write(total_csv, 'total_analysis.csv')
elif args.organize:
	done_path = '../blogtagging_done/first_stage/'

	for i in range(args.n_user+1):
		user_path = 'userData/user'+str(i)+'/'
		user_files = os.listdir(os.path.join(os.getcwd(), user_path))
		for userf in user_files:
			if not userf.endswith('.json'): continue
			print('user{}/{}'.format(i,userf))
			with open(user_path+userf,'r',encoding='utf8') as f: userData = json.load(f)
			with open(done_path+category(userf)+'.json','r',encoding='utf8') as f: doneData = json.load(f)
			for d in userData:
				if d['status']!='tagged': continue 
				d['annotator'] = args.user
				doneData.append(d)
			with open(done_path+category(userf)+'.json', 'w') as f: json.dump(doneData,f)
