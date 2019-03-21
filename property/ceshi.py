from django.core.cache import cache
from pydub import AudioSegment
import time, os
from django.conf import settings


# dict1 = {
#     'name': '郭昌荣',
#     'sex': '男',
#     'age': 24
# }
# cache.set('a', dict1, 60*6)
# print(cache.has_key('a'))
# a = cache.get('a')
# print(a, type(a))

# filepath1 = 'C:/Users/gcr/PycharmProjects/xytproperty/media/tmp_578325a21d2282cae134ff1066c7cf28b63cd57d0697edf3.m4a'
# filepath = 'wav/' + str(time.time())
# sound = AudioSegment.from_m4a(filepath1)
# sound.export(filepath, format='wav')

# import wave
# m4a_path = r'C:/Users/gcr/Desktop/临时保存/607d3b3e538b90f8b4daa1b79fb2fb36a1c3c509.m4a'
#
# with open(m4a_path, 'rb') as m4afile:
#     m4adata = m4afile.read()
# with wave.open(m4a_path + '.wav', 'wb') as wavfile:
#     wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
#     wavfile.writeframes(m4adata)
#     print('succese')

# from . import translate_test
import hashlib

# filepath = f"{settings.MEDIA_ROOT}3333.m4a"
# filepath = filepath.replace('\\', '/')
# # filepath = filepath.replace('//', '/')
# filepath1 = filepath.replace('.m4a', '.wav')
# print(filepath, filepath1)
# os.system(f'ffmpeg -i {filepath} {filepath1}')

