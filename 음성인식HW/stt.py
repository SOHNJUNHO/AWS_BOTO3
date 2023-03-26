import pyaudio
import wave
import base64
import json
import threading
import time
import scipy.io as sio
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
from sttapi import SttApi
import levenshtein
import random_word

# 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 30
KEYWORD = ''

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


## 읽을 단어 = read_it

read_it = random_word.word

instructions = (
        "다음의 단어를 소리내서 읽으시오:\n"
        "{words}\n"
    ).format(words = read_it)

print(instructions)

# init
stt = SttApi.create(RATE, CHUNK, RECORD_SECONDS)

# prepare
sttId = stt.prepare(KEYWORD)

thdSend = threading.Thread(target=stt.sendBody, args=(sttId, stream))
thdSend.start()

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    stt.setData(data)
    if not(stt.STT_STATUS == 'P01' or stt.STT_STATUS == 'P02'):
        break

print("녹음이 끝났습니다.")

stream.stop_stream()
stream.close()
p.terminate()

while(stt.STT_STATUS == 'P01' or stt.STT_STATUS == 'P02'):
    print('')
# finish

res = stt.finish(sttId)

#print('==============================result==============================')
#print(res.json())
#print('==============================result==============================')

jsonObject = res.json() ## 인식된 음성의 정보 json 형식


## 레벤슈타인 값 출력
ref_text = jsonObject['analysisResult']['result'] ## 인식된 음성 텍스트로 출력
stt_text = read_it ## 정답 텍스트

sentence_info = {'ref': ref_text, 'hyp': stt_text}
cer_info = levenshtein.cer(sentence_info)

 #인식률 (Character Error Rate) 출력
 
print('refer : %s' % ref_text)

print('hyper : %s' % stt_text)

cer_rate = 100 - cer_info.get('cer')
print('cer : %f' % cer_rate if cer_rate > 0 else 0.0)  

print('match list : ', cer_info.get('list'))

#print('tot : %d' % cer_info.get('tot'))  # 전체 음절 수
#print('mat : %d' % cer_info.get('mat'))  # 매치 음절 수
#print('sub : %d' % cer_info.get('sub'))  # 교체 에러 수
#print('ins : %d' % cer_info.get('ins'))  # 삽입 에러 수
#print('del : %d' % cer_info.get('del'))  # 삭제 에러 수