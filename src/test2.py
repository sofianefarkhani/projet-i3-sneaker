# from keras.backend import softmax
# from keras.engine.base_layer import TensorFlowOpLayer
# import tensorflow
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras import Sequential, layers
# from tensorflow.keras.utils import get_file, img_to_array
# from keras.preprocessing.image import load_img
from keras.models import load_model
# from tensorflow import expand_dims, nn
# import numpy as np
# from keras.preprocessing import image
# import cv2
# import matplotlib.pyplot as plt
# from tensorflow.python.ops.gen_math_ops import imag_eager_fallback


model = load_model('model.h5')
model.load_weights('weights.h5')
imgPath = "../img/train/trainingTestImages/421092-1--96c78ec3-7cc0-4ad3-ad10-eb2db8916eaf.jpg"

# img = image.load_img(imgPath, target_size=(120, 120), color_mode="grayscale")
# img_array = image.img_to_array(img)
# img_batch = np.expand_dims(img_array, axis=0)
# img_batch /=255.
# model.compile(optimizer='adam', loss='categorical_crossentropy',             metrics=['accuracy'])
# # prediction = model.predict(img_batch, verbose=1)


# # img2 = (np.expand_dims(img,0))


# # probability_model = Sequential([model, layers.Softmax()])
# # prediction = probability_model.predict(img2)


# # print(prediction)


# # test_image = image.load_img(imgPath, target_size=(120,120), color_mode="grayscale")
# # images = image.img_to_array(test_image)
# # images = np.expand_dims(images, axis=0)
# # images/=255.

# img_width, img_height = 120, 120
# img = image.load_img(imgPath, target_size = (img_width, img_height), color_mode="grayscale")
# img = image.img_to_array(img)
# img = np.expand_dims(img, axis = 0)/255
# img = tensorflow.cast(img, tensorflow.float32)

# print(type(img[0]))



# print(model.predict(img))

from keras.preprocessing.image import ImageDataGenerator

test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
        "/home/vedoc/Images/Sneaker-data/test temp",
        target_size=(120, 120),
        batch_size=32,
        color_mode="grayscale",
        class_mode='binary',
        shuffle=False)

#make the prediction
prediction=model.predict(test_generator, verbose=1)

print(prediction)