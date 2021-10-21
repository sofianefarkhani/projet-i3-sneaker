import numpy
from tensorflow.keras import layers
from Data.Color import Color
from Data.Tag import Tag
from Data.Type import Type
import json
from json import JSONEncoder
import jsonpickle
from interface.Writer import Writer
from interface.JsonReader import JsonReader
from interface.Loader import Loader
from PIL import Image
import cv2
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPool2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout

# 
# 
# OLD FILE ONLY TO KEEP SOME INFO TO TEST WITH IA
# 
# 
# 


IMG_SIZE = 100  # Todo: set and load this in config and not here


def showImage(img):
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


img = []
for i in range(1, 10):
    image = cv2.imread('../img/test/' + str(i) + '.png')
    # If needed we can directely use Image.open(path) #Read image syntax with PIL Library
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image) # Convert opencv image into PIL image
    image.convert('L') #Grayscale conversion with PIL library
    image.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS) #Resizing image syntax with PIL Library
    # image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    # image = image[...,::-1] # opencv is in BGR, but keras need RGB
    # image = image.astype(numpy.float32) / 255.0

    img.insert(i-1, image)
    # showImage(img[i-1])

def load_data():
    x_train = []
    y_train = []
    for image in img[:5]:
        x_train.append(numpy.array(image))
        y_train.append(numpy.array([1, 0]))

    x_test = []
    y_test = []
    for image in img[5:]:
        x_test.append(numpy.array(image))
        y_test.append(numpy.array([0,1]))
    
    return (x_train, y_train), (x_test, y_test)



# load dataset
(x_train, y_train), (x_test, y_test) = load_data()


# # normalize pixel values
# x_train = x_train.astype('float32') / 255.0
# x_test = x_test.astype('float32') / 255.0

input_shape = (IMG_SIZE, IMG_SIZE, 1)


# define model

model = Sequential()
model.add(Conv2D(32, (5,5), activation='relu', kernel_initializer='he_uniform', input_shape=input_shape))
model.add(MaxPool2D((5, 5)))
# model.add(Conv2D(64, (5,5), activation='relu'))
# model.add(MaxPool2D((5, 5)))

# model.add(Conv2D(32, (5,5), activation='relu'))
# model.add(MaxPool2D((5, 5)))
# model.add(Conv2D(64, (5,5), activation='relu'))
# model.add(MaxPool2D((5, 5)))
# model.add(Conv2D(32, (5,5), activation='relu'))
# model.add(MaxPool2D((5, 5)))
# model.add(Conv2D(64, (5,5), activation='relu'))
# model.add(MaxPool2D((5, 5)))


model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.8))
model.add(Dense(2, activation='softmax'))

# define loss and optimizer
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# fit the model
model.fit(x_train, y_train, epochs=10, batch_size=128, verbose=0)


# # evaluate the model
# loss, acc = model.evaluate(x_test, y_test, verbose=0)
# print('Accuracy: %.3f' % acc)