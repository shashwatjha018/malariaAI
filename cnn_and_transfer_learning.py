# import the libraries as shown below
from tensorflow.keras.applications.inception_v3 import InceptionV3 # trained pre built deeplearning model/weights                  #tensorflow keras->tensorflow
from tensorflow.keras.layers import Input, Lambda, Dense, Flatten,Conv2D #neural network layer
from tensorflow.keras.models import Model #class 
from tensorflow.keras.applications.vgg19 import VGG19#deeplearning model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential#type of model
import numpy as np#library
from glob import glob
import matplotlib.pyplot as plt

# re-size all the images to this
IMAGE_SIZE = [224, 224]

train_path = 'Dataset/Train'
valid_path = 'Dataset/Test'

# from google.colab import drive
# drive.mount('/content/drive')

# Import the Vgg19 library as shown below and add preprocessing layer to the front of VGG
# Here we will be using imagenet weights
mobilnet = InceptionV3(input_shape=IMAGE_SIZE + [3],weights='imagenet', include_top=False) #object """rgb""" weights are learned by model -> competition model, imagenet ->big database of photos classes
##include_top -> output layer is false
#mobilnet = VGG19(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# don't train existing weights
for layer in mobilnet.layers:
    layer.trainable = False

# useful for getting number of output classes
folders = glob('Dataset/Train/*')

folders

# our layers - you can add more if you want
x = Flatten()(mobilnet.output) #we added this own layer, base model o/p act as a input for flatten layer

prediction = Dense(len(folders), activation='softmax')(x)  #output layer -> o/p from flatten acts as a i/p

# create a model object
model = Model(inputs=mobilnet.input, outputs=prediction)

# view the structure of the model
model.summary()

from tensorflow.keras.layers import MaxPooling2D

### Create Model from scratch using CNN
model=Sequential()
model.add(Conv2D(filters=16,kernel_size=2,padding="same",activation="relu",input_shape=(224,224,3)))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=32,kernel_size=2,padding="same",activation ="relu"))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=64,kernel_size=2,padding="same",activation="relu"))
model.add(MaxPooling2D(pool_size=2))
model.add(Flatten())
model.add(Dense(500,activation="relu"))
model.add(Dense(2,activation="softmax"))
model.summary()

# tell the model what cost and optimization method to use
model.compile(
  loss='categorical_crossentropy', ##how much error is there from the actual result
  optimizer='adam',
  metrics=['accuracy']
)

# Use the Image Data Generator to import the images from the dataset
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,   #data augmentation techniques
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255) #we dont apply aug tech in test_datagen

# Make sure you provide the same target size as initialied for the image size
training_set = train_datagen.flow_from_directory('Dataset/Train',
                                                 target_size = (224, 224),
                                                 batch_size = 32, #import in batches
                                                 class_mode = 'categorical') #every folder is like a category

# training_set

test_set = test_datagen.flow_from_directory('Dataset/Test',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')

r = model.fit_generator(   #to train model
  training_set,
  validation_data=test_set, #we use a test_data as a validation data
  epochs=50,#cycles of test
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)

# plot the loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()
plt.savefig('LossVal_loss')

# plot the accuracy
plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()
plt.savefig('AccVal_acc')

from tensorflow.keras.models import load_model

model.save('cnn_model.h5') #we saved our weights

y_pred = model.predict(test_set) #predict on test set-probabilty of an image to belong to a class

# y_pred

import numpy as np
y_pred = np.argmax(y_pred, axis=1)  #arg_max = cap in Harry Potter, y_pred = probablities

y_pred



from keras.models import load_model
from keras.preprocessing import image

model_reloaded=load_model('cnn_model.h5')   #reload the model



img=image.load_img('Dataset/Test/infected/2.png',target_size=(224,224)) #random image 

x=image.img_to_array(img)
x

x.shape

x=x/255

x=np.expand_dims(x,axis=0)
img_data=preprocess_input(x)
img_data.shape

model_reloaded.predict(img_data)

a=np.argmax(model_reloaded.predict(img_data), axis=1)

if(a==1):
    print("Uninfected")
else:
    print("Infected")



