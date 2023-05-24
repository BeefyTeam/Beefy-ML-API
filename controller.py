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
    predictions = model.predict(img_postpreprocessing).flatten()
    predictions = tf.nn.sigmoid(predictions, name='sigmoid')
    predicted_label = tf.where(predictions < 0.5, 'fresh', 'spoiled').numpy()[0]
    label_final = bytes.decode(predicted_label, 'utf-8')
    return label_final

def inference(file: UploadFile):
    try:
        image = preprocessing(fileImage=file)
        label = post_preprocessing(img_postpreprocessing=image)
        responseBody = {
            'label': label,
        }
        return True, responseBody
    except:
        return False, None