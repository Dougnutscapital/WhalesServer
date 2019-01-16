from keras.models import load_model
import cv2 as cv
import numpy as np

model = load_model("../trained_models/cropping.model")


def crop_photo(im):
    resized = cv.resize(im, (128, 128))
    expanded_1 = np.expand_dims(resized, axis=3)
    expanded_2 = np.expand_dims(expanded_1, axis=0)
    res = np.squeeze(model.predict(expanded_2))

    for i in range(len(res)):
        if res[i] >= 128:
            res[i] = 127
        elif res[i] < 0:
            res[i] = 0
    res[0] *= im.shape[1] / 128 + 1
    res[1] *= im.shape[0] / 128 + 1
    res[2] *= im.shape[1] / 128 - 1
    res[3] *= im.shape[0] / 128 - 1

    res = res.astype(int)

    if res[2] - res[0] <= 1 or res[3] - res[1] <= 1:
        # failed to crop, return original image
        return im

    return im[res[1]:res[3], res[0]:res[2]]

