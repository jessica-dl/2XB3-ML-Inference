from keras.models import load_model
import cv2
import numpy as np


class Inference:

    def __init__(self, encoder_fp, generator_fp):
        self.encoder_fp = encoder_fp
        self.generator_fp = generator_fp
        self.encoder = load_model(encoder_fp)
        self.generator = load_model(generator_fp)

        self.encoder.summary()
        self.generator.summary()

        self.encoder._make_predict_function()
        self.generator._make_predict_function()

    def infer(self, img, age):
        img = cv2.resize(img, (64, 64))

        img = (img.astype(np.float32) - 127.5) / 127.5

        img = np.expand_dims(img, axis=0)

        latent_vec = self.encoder.predict(img)
        encoded_age = self.__encode_age(age)
        new_img = self.generator.predict([latent_vec, encoded_age])[0]

        new_img = ((0.5 * new_img + 0.5) * 255)

        return new_img

    def __encode_age(self, age):
        age_array = np.zeros((6,))
        if 0 < age < 18:
            age_array[0] = 1
        elif 19 < age < 29:
            age_array[1] = 1
        elif 30 < age < 39:
            age_array[2] = 1
        elif 40 < age < 49:
            age_array[3] = 1
        elif 50 < age < 59:
            age_array[4] = 1
        else:
            age_array[5] = 1

        return np.expand_dims(age_array, axis=0)
