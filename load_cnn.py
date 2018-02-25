#loading conv net
from keras.models import model_from_json
import numpy as np

x_train = np.load('pixel_data.npy')[0]
y_train = np.load('pixel_data.npy')[2]
x_test = np.load('pixel_data.npy')[1]
y_test = np.load('pixel_data.npy')[3]


def load_model():
   json_file = open('model.json', 'r')
   loaded_model_json = json_file.read()
   json_file.close()
   
   loaded_model = model_from_json(loaded_model_json)
   # load weights into new model
   loaded_model.load_weights("weights.h5")
       
   # evaluate loaded model on test data
   loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
   score = loaded_model.evaluate(x_test, y_test, verbose=0)
   print(score[1])
   return loaded_model


if __name__ == '__main__':
   model = load_model()
   print(model.predict( np.expand_dims(x_train[0], axis=0)    ))
   print(y_test[0])
   
      