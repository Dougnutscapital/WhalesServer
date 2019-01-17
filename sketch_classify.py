import numpy as np
import pandas as pd
from keras.applications.imagenet_utils import preprocess_input
from keras.metrics import top_k_categorical_accuracy
from keras.models import load_model
from keras.preprocessing import image
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

img_size = 224


def top_5_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=5)


model = load_model('trained_models/white_model.h5', custom_objects={'top_5_accuracy': top_5_accuracy})
df_train = pd.read_csv('metadata/train.csv')


def prepareImages(data, m, dataset):
    print("Preparing images")
    X_train = np.zeros((m, img_size, img_size, 3))
    count = 0

    for fig in data['Image']:
        img = image.load_img(dataset + "/" + fig, target_size=(img_size, img_size, 3))
        x = image.img_to_array(img)
        x = preprocess_input(x)

        X_train[count] = x
        if count % 500 == 0:
            print("Processing image: ", count + 1, ", ", fig)
        count += 1

    return X_train


def load_img(img_name):
    X = np.zeros((img_size, img_size, 3))
    img = image.load_img(img_name, target_size=(img_size, img_size, 3))
    X = image.img_to_array(img)
    X = preprocess_input(X)
    return X


def prepare_labels(y):
    y = df_train['Id']
    values = np.array(y)
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    # print(integer_encoded)

    one_encoder = OneHotEncoder()
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    one_encoded = one_encoder.fit_transform(integer_encoded)
    # print(onehot_encoded)

    y = one_encoded
    # print(y.shape)
    return y, label_encoder, one_encoder


y, label_encoder, one_encoder = prepare_labels(df_train['Id'])


def predict_from_sketch(img_path):
    """
    Predict image id from user sketch
    :param img_path: relative path to the image (stored on the local fil system)
    :return: array containing ids: ["__id1__", "__id2__"] (return one id is okay)
    """
    img_1 = img_path
    result = model.predict(load_img(img_1).reshape(1, 224, 224, 3))
    print(result)
    result_1 = one_encoder.inverse_transform(result).astype(int)
    result_2 = label_encoder.inverse_transform(result_1)
    return result_2


model._make_predict_function()
