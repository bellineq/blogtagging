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
	plain_article = '火關就手依態行以的;小住到下走。電有展到福系，痛名談喜河功野候，中上白；好野科點著來怕美合公了式上。來心要黨構施先……我立後待義在品是則頭團見聲我小熱分八美關不樂視身經教，交有連在電，小門開這題意，久門器。;遊國叫。感日本任影的，子動制；很愛乎種，樓樂呢，字生指效象、一一系燈教河正、比質金大但有理者說指不議兒化作持媽年人後市交經，消操腦關戰比望者他。;自說八國金要求海面完一最更光業交。機質學喜改觀處應樣我響地何過是；它不濟心一道日報春。車建來統很總說太最或了戲直司我我成立起；人緊來相城告後自山校次題。場著起愛要學加，教間次下相形單背加樂交這大一座，麼感上林說歌前且照受大有片過對清人明中小務其；飯半間要們人世院先友一到、知西由來但然國來的候事，候養一親萬好備孩心一法音隨難理容大，有還人遊親去通一包神人長起東如有想中家無？異華親類。中學即法信一的你象品是保處不的拿消、人查己但被藝富選歡，太制河之學，北一多關大受計力人民論，而法像管……老產者王及心或別前告立活每年。'

	article = [[(word, f'{l_id:01}-{w_id:01}',) \
		for w_id, word in enumerate(line)] \
			for l_id, line in enumerate(plain_article.split(';'))]

	return render_template('index.html', article=article)

@app.route('/save', methods=['POST'])
def save():
	try:
		data = request.data
		json_data = json.loads(data)
		print(json_data['text'])
		return jsonify(message='')
	except Exception as e:
		print(f'"/result" failed: {e}')
		return jsonify(message=str(e)), 500

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
