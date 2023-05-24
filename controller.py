from fastapi import UploadFile

import tensorflow as tf
from keras.models import load_model
from keras.utils import img_to_array
import numpy as np
from PIL import Image

def preprocessing(fileImage: UploadFile):
    img = Image.open(fileImage.file)
    img = img.resize((224, 224))
    img_array = img_to_array(img, dtype=np.float32)
    img_preprocessed = np.expand_dims(img_array, axis=0)
    return img_preprocessed

def post_preprocessing(img_postpreprocessing):
    model = load_model('./models/beefy-mobilenetv2.h5')
    predictions = model.predict(img_postpreprocessing)
    predicted_label = np.argmax(predictions, axis=1)[0]
    probabilities = tf.reduce_max(predictions, axis=1)

    class_names = ['fresh', 'spoiled']
    predicted_class = class_names[predicted_label]

    if (predicted_class == 'spoiled'):
        kesegaran = 100.0 - float(probabilities)*100
    else:
        kesegaran = float(probabilities)*100


    return predicted_class, "{:.2f}%".format(kesegaran)

def inference(file: UploadFile):
    try:
        image = preprocessing(fileImage=file)
        label, level = post_preprocessing(img_postpreprocessing=image)
        responseBody = {
            'label': label,
            'kesegaran': level
        }
        return True, responseBody
    except:
        return False, None