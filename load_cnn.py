#loading conv net
from keras.models import model_from_json
import numpy as np

x_train = np.load('pixel_data.npy')[0]
y_train = np.load('pixel_data.npy')[2]
x_test = np.load('pixel_data.npy')[1]
y_test = np.load('pixel_data.npy')[3]


def load_model():
   json_file = open('model.json', 'r')
   model_json = json_file.read()
   json_file.close()
   
   model = model_from_json(model_json)
   # load weights into new model
   model.load_weights("weights.h5")
       
   # evaluate loaded model on test data
   model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
   score = model.evaluate(x_test, y_test, verbose=0)
   model_predictions = model.predict(x_test) 
   fc_scores = []
   predictions = []
   for c in range(0, model_predictions.shape[1]):
      fc_scores.append([])
      for r in range(0, model_predictions.shape[0]):
         fc_scores[c].append(model_predictions[r][c])
         
   for c in range(0, len(fc_scores[0])):
      if(fc_scores[0][c] > fc_scores[1][c]):
         predictions.append("0")
      elif(fc_scores[0][c] < fc_scores[1][c]):
         predictions.append("1")

   ground_truth_test = []   
   for i in range(0, len(y_test)):
      if(y_test[i][0] > y_test[i][1]):
         ground_truth_test.append("0")
      else:
         ground_truth_test.append("1")
   
   
   print(score[1])
   pos_acc = get_positive_accuracy(predictions, ground_truth_test)
   neg_acc = get_negative_accuracy(predictions, ground_truth_test)
   print("Predictions:")
   print(predictions[0:20])
   print("Truth: ")
   print(ground_truth_test[0:20])
   print("Positive accuracy: " + str(pos_acc))
   print("Negative accuracy: " + str(neg_acc))
   
   return model 
  
   
   
   
   
def get_positive_accuracy(pred, truth):
   right_positive = 0
   total_positive = 0
   for i in range(0, len(truth)):
      pathology = int(truth[i])
      if(pathology == 1):
         total_positive += 1
         if(int(pred[i]) == 1):
            right_positive += 1
      
     
   return float(right_positive)/float(total_positive)

def get_negative_accuracy(pred, truth):
   right_negative = 0
   total_negative = 0
   for i in range(0, len(truth)):
      pathology = int(truth[i])
      if(pathology == 0):
         total_negative += 1
         if(int(pred[i]) == 0):
            right_negative += 1
   return float(right_negative)/float(total_negative)
   
   
   



if __name__ == '__main__':
   model = load_model()
   #print(model.predict( np.expand_dims(x_train[0], axis=0)    ))
   #print(y_test[0])
   
      