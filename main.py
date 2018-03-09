#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
	username = 'Amy'

	plain_article = '我我,想,要,吃,番,茄茄;我我,不,想,要,睡,覺覺'

	article = [[(word, f'w-{l_id:05}-{w_id:05}',) \
		for w_id, word in enumerate(line.split(','))] \
			for l_id, line in enumerate(plain_article.split(';'))]

	return render_template('index.html', article=article)

@app.route('/result', methods=['POST'])
def signin():
	try:
		data = request.data
		json_data = json.loads(data)
		print(json_data['text'])
		return jsonify(message='')
	except Exception as e:
		print(f'"/result" failed: {e}')
		return jsonify(message=str(e)), 500

if __name__ == '__main__':
	app.run(debug=True)
