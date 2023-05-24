from fastapi import UploadFile

import tensorflow as tf
from keras.utils import img_to_array
import numpy as np
from PIL import Image

def preprocessing(fileImage: UploadFile):
    img = Image.open(fileImage.file).resize((224, 224))
    img_array = img_to_array(img)
    img_preprocessed = np.expand_dims(img_array, axis=0)
    return img_preprocessed

def post_preprocessing(img_postpreprocessing):
    model = tf.keras.models.load_model('./models/beefy-mobilenetv2.h5')
    predictions = model.predict(img_postpreprocessing).flatten()
    predictions = tf.nn.sigmoid(img_postpreprocessing)
    predicted_label = tf.where(predictions < 0.5, 'fresh', 'spoiled').numpy()[0]
    return predicted_label, predictions


def inference(file: UploadFile):
    try:
        image = preprocessing(fileImage=file)
        label, probability = post_preprocessing(img_postpreprocessing=image)
        responseBody = {
            'label': label,
            'pobability': probability
        }
        return True, responseBody
    except:
        return False, None