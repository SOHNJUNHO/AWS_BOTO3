import requests
import sys
import base64
import scipy.io as sio
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt

WAVE_FILENAME = 'c:\\output.wav'
KEYWORD = '' # 예) 안녕|하세

def post(url, field_data) :
    headers = {'API-KEY-ID':'ACADEMY_SPEECH', 'API-KEY':'e8j8GPwcLqeijX1D'}
    return requests.post(url, headers=headers, data=field_data)

try:
    inputData = open(WAVE_FILENAME, 'rb').read()
except:
    print('error: file does not exists')
    sys.exit(1)

bytesdata = base64.b64encode(inputData)

url = 'https://t-stt.chunjaeai.com/stt/upload'
field_data = {'modelId':'0', 'contentbytes':bytesdata}

r = post(url, field_data)
print('==============================result==============================')
print(r.json())
print('==============================result==============================')


# graph
rate, data = sio.wavfile.read(WAVE_FILENAME)
size = len(data)
times = np.arange(size)/float( rate)

print ('sample_size: ', size)
print ('shape of data: ', data.shape )
print ('sample_rate: ', rate)
print ('play time : : ', times[-1] )

plt.plot(times, data)
plt.xlim(times[0], times[-1])

plt.xlabel('time (s)')
plt.ylabel('amplitude')
plt.show()