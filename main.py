__copyright__ 	= 'Copyright (C) 2020 AI, Inc.'
__url__ 		= 'https://www.ai-j.jp/'


import streamlit as st
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import re
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

class AITalkWebAPI:
	
	URL = 'https://cloud.ai-j.jp/demo/aitalk2webapi_nop.php'	# WebAPI URL
	ID = 'altrobo'	# ユーザ名(接続ID)
	PW = 'O6Dv.hm|mPNF[Xzg'	# パスワード(接続パスワード)


	def __init__(self):
		self.username = self.ID
		self.password = self.PW
		self.api_version = "v5"
		self.speaker_id     = 511
		self.style 			= '{"j":"1.0"}'	# 感情パラメータ
		self.input_type 	= 'text'		# 合成文字種別
		self.text 			= ''			# 合成文字
		self.volume 		= 1.0			# 音量（0.01-2.00）
		self.speed 			= 1.0			# 話速（0.50-4.00）
		self.pitch 			= 1.0			# ピッチ（0.50-2.00）
		self.range 			= 1.0			# 抑揚（0.00-2.00）
		self.anger          = 0
		self.sadness        = 0
		self.joy            = 0
		self.output_type 	= 'sound'		# 出力形式
		self.ext 			= 'mp3'			# 出力音声形式
		self.use_udic 		= '1'; 			# ユーザー辞書利用フラグ
		self._headers = None
		self._sound = None
		self._err_msg = None


	def synth(self):
		dic_param = {
			'username'		: self.username,
			'password'		: self.password,
			'api-version'	: self.api_version,
			'speaker_id'    : self.speaker_id,
			'style'			: self.style,
			'input_type'	: self.input_type,
			'text'			: self.text,
			'volume'		: self.volume,
			'speed'			: self.speed,
			'pitch'			: self.pitch,
			'range'			: self.range,
			'output_type'	: self.output_type,
			'ext'			: self.ext,
			'use_udic'		: self.use_udic,
			'anger'         : self.anger,
			'sadness'       : self.sadness,
			'joy'           : self.joy,
		}

		# URLエンコードされた合成パラメータの生成
		encoded_param = urllib.parse.urlencode(dic_param).encode('ascii')
		# HTTPヘッダーの生成
		header = {'Content-Type': 'application/x-www-form-urlencoded',}
		# URLリクエストの生成
		req = urllib.request.Request(self.URL, encoded_param, header)

		ret = False
		try:
			with urllib.request.urlopen(req) as response:
				
				self.code = response.getcode()
				self.headers = response.info()
				self.sound = response.read()
				
				# Decode the bytes to a string
				response_str = self.sound.decode('utf-8')
				print("response:", response_str)

				# Use regex to find the JSON object within the callback function
				match = re.search(r'callback\((.*)\)', response_str)

				# If there's a match, parse the JSON and extract the file name
				if match:
					json_str = match.group(1)
					data = json.loads(json_str)
					self.sound = data['url']
				else:
					print("No URL found in the response.")
						
				ret = self.code == 200
		except urllib.error.HTTPError as e:
			self._err_msg = 'HTTPError, Code: ' + str(e.code) + ', ' + e.reason
		except urllib.error.URLError as e:
			self._err_msg = e.reason
		return ret

	
	def get_error(self):
		return self._err_msg if self._err_msg is not None else ''


	def get_cloud_file_url(self):
		print(self.sound)
		return "https:" + self.sound
	

def text_to_speech(text, speaker_id, volume, speed, pitch, range, anger, sadness, joy):
	target_text = text
	target_file = 'output.mp3'

	# ext = os.path.splitext(target_file)[1][1:]
	# if ext == 'm4a':
	# 	ext = 'aac'

	aitalk = AITalkWebAPI()
	aitalk.text = target_text
	aitalk.speaker_id = speaker_id
	aitalk.style = '{"j":"1.0"}'
	aitalk.ext = "mp3"
	aitalk.volume = volume
	aitalk.speed = speed
	aitalk.pitch = pitch
	aitalk.range = range
	aitalk.anger = anger
	aitalk.sadness = sadness
	aitalk.joy = joy

	if not aitalk.synth():
		print(aitalk.get_error(), file=sys.stderr)
		return 1

	response = aitalk.get_cloud_file_url()
	
	return response


def main():
	speech_file_path = ""
	st.title("Text to Speech Converter")
	# Text input
	user_input = st.text_area("Enter the text you want to convert to speech:", height=150)
	
	col1, col2, col3, col4, col5 = st.columns(5)
	
	with col1:
		st.image('./image/seiji.png', caption='seiji')

		col11, col12, col13 = st.columns([1, 6, 1])
		with col12:
			# kenta button
			if st.button(label="Convert", type="secondary", key="seiji"):
				speech_file_path = text_to_speech(user_input, 511, 1.0, 1, 1, 1, 0, 0, 0)
				

	with col2:
		st.image('./image/taichi.png', caption='taichi')

		col21, col22, col23 = st.columns([1, 6, 1])
		with col22:
			# osamu button
			if st.button(label="Convert", type="secondary", key="taichi"):
				speech_file_path = text_to_speech(user_input, 514, 1.0, 1, 1, 1, 0, 0, 0)

	with col3:
		st.image('./image/kenta.png', caption='kenta')

		col31, col32, col33 = st.columns([1, 6, 1])
		with col32:
			# seiji button
			if st.button(label="Convert", type="secondary", key="kenta"):
				speech_file_path = text_to_speech(user_input, 525, 1.0, 1, 1, 1, 0, 0, 0)

	with col4:
		st.image('./image/osamu.png', caption='osamu')

		col41, col42, col43 = st.columns([1, 6, 1])
		with col42:
			# taichi button
			if st.button(label="Convert", type="secondary", key="osamu"):
				speech_file_path = text_to_speech(user_input, 13, 1.0, 1, 1, 1, 0, 0, 0)

	with col5:
		st.image('./image/yamato.png', caption='yamato')

		col51, col52, col53 = st.columns([1, 6, 1])
		with col52:
			# taichi button
			if st.button(label="Convert", type="secondary", key="yamato"):
				speech_file_path = text_to_speech(user_input, 202, 1.0, 1, 1, 1, 0, 0, 0)


	if speech_file_path:
		try:
			with urllib.request.urlopen(speech_file_path) as response:
				audio_bytes = response.read()

			st.audio(audio_bytes, format='audio/mp3')
			st.download_button(label="Download",
							data=audio_bytes,
							file_name="speech.mp3",
							mime="audio/mp3")
		except Exception as e:
			print(e)


if __name__ == "__main__":
  main()