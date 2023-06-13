from fastapi import UploadFile

import tensorflow as tf
from keras.models import load_model
from keras.utils import img_to_array
import numpy as np
from PIL import Image

def preprocessing(fileImage: UploadFile):
    img = Image.open(fileImage.file)
    rgb_im = img.convert('RGB')
    img = rgb_im.resize((224, 224))
    img_array = img_to_array(img, dtype=np.float32)
    img_preprocessed = np.expand_dims(img_array, axis=0)
    return img_preprocessed

def post_preprocessing(img_postpreprocessing):
    model1 = load_model('models/beefy-1-model.h5')
    model2 = load_model('models/beefy-2-model.h5')

    predictions1 = model1.predict(img_postpreprocessing)
    predicted_label1 = np.argmax(predictions1, axis=1)[0]
    probabilities1 = tf.reduce_max(predictions1, axis=1)

    class_names_model1 = ['fresh', 'spoiled']
    predicted_class_model1 = class_names_model1[predicted_label1]

    predictions2 = model2.predict(img_postpreprocessing)
    predicted_label2 = np.argmax(predictions2, axis=1)[0]

    class_names_model2 = ['beef', 'others', 'pork']
    predicted_class_model2 = class_names_model2[predicted_label2]


    if (predicted_class_model1 == 'spoiled'):
        kesegaran = 100.0 - float(probabilities1)*100.0
    else:
        kesegaran = float(probabilities1)*100.0


    return predicted_class_model1, "{:.2f}%".format(kesegaran), predicted_class_model2

def inference(file: UploadFile):
    try:
        image = preprocessing(fileImage=file)
        label, level, type = post_preprocessing(img_postpreprocessing=image)
        if (type == 'others'):
            responseBody = {
                'label': 'others',
                'kesegaran': '-',
                'type': type
            }
        else:
            responseBody = {
                'label': label,
                'kesegaran': level,
                'type': type
            }
        return True, responseBody
    except:
        return False, None