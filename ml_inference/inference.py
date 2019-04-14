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
        img = cv2.resize(img, (64, 64))  # resize the image to be the correct size

        img = (img.astype(np.float32) - 127.5) / 127.5

        img = np.expand_dims(img, axis=0)

        latent_vec = self.encoder.predict(img)  # the image is processed into a latent vector
        encoded_age = self.__encode_age(age)  # the age is on-hot encoded
        new_img = self.generator.predict([latent_vec, encoded_age])[0]  # the aged image from the age and latent vector

        new_img = ((0.5 * new_img + 0.5) * 255)  # format the image to be returned to the client

        return new_img

    def __encode_age(self, age):  # one-hot encodes the age
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

        return np.expand_dims(age_array, axis=0) # returns array in the required format
