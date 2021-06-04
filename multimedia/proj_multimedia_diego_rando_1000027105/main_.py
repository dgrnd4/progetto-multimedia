import audioconverter
import audioreader
import audiowriter

import numpy as np

# Per provare la steganografia, avviando i codici,
# bisogna eliminare tutti i file di output in quanto 
# non c'è sovrascrizione:
# lasciare solo l'img e l'audio originale per non avere errori



from PIL import Image

from numpy import asarray


original_audio = 'EncodeAudio/matargasti.mp3'
output_audio = 'EncodeAudio/matargasti_output.wav'
decode_audio_wav= 'DecodeAudio/final.wav'
decode_audio_mp3= 'DecodeAudio/final.mp3'


# .mp3 --> .wav
audioconverter.mp3towav(original_audio,output_audio)


# L'audio diventa immagine (variabile output_audio ha il percorso)
audioreader.audiotoimage(output_audio) 
audio_image= 'audio.png'




def genData(data):

		newd = []

		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd


# Pixels modificati (8-bit binario)
def modPix(pix, data):

	datalist = genData(data) #conversione dei dati in 8-bit binari
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):

		# estrazione 3 pixel alla volta
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		# 1 pari, 0 dispari
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1
	

		# controllo se c'è ancora da continuare a leggere i pixel o no
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1
		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]


def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data): 

		# inseriamo i pixel nell'img
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1


# funzione ivnersa --> decodifica 
def decode():
	
	image = Image.open('final_img.png', 'r')
	data = ''
	imgdata = iter(image.getdata())

	while (True):
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]

		binstr = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return data

# Codifica i dati nell'img
def encode():
	
	image = Image.open("orig_img.png", 'r')

	img = Image.open('audio.png','r')
	data = str(asarray(img))


	if (len(data) == 0):
		raise ValueError('Data is empty')

	newimg = image.copy()
	encode_enc(newimg, data)

	# nome del file finale
	new_img_name = "final_img.png" 
	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper())) 



encode()

img_ = Image.open('audio.png','r')
# otteniamo l'array dall'immaigne audio
data_array = asarray(img_)

# dall'array ricaviamo l'immagine e la salviamo in array_to_img
data_img = Image.fromarray(data_array)
data_img.save('audio_extracted_by_final_img.png')




#t=decode()
#print(t)


output_audio_final = 'EncodeAudio/matargasti_output_final.wav'
audioconverter.mp3towav(original_audio,output_audio_final)

audiowriter.imagetoaudio(audio_image,decode_audio_wav)
#audioconverter.wavtomp3(decode_audio_wav,decode_audio_mp3)


