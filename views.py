from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
import pickle
import os
from django.core.files.storage import FileSystemStorage
import io
import base64
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import cv2
from keras.utils.np_utils import to_categorical
from keras.layers import  MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten, LSTM
from keras.layers import Convolution2D
from keras.models import Sequential, load_model, Model
import pickle
from keras.callbacks import ModelCheckpoint
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import pymysql

global uname, graph, cnn_model, scaler, label_encoder, lstm_model

accuracy = []
precision = []
recall = [] 
fscore = []

#function to calculate all metrics
def calculateMetrics(algorithm, y_test, predict):
    global graph
    a = accuracy_score(y_test,predict)*100
    p = precision_score(y_test, predict,average='macro') * 100
    r = recall_score(y_test, predict,average='macro') * 100
    f = f1_score(y_test, predict,average='macro') * 100
    accuracy.append(a)
    precision.append(p)
    recall.append(r)
    fscore.append(f)      

dataset = pd.read_csv("Clinical_data.csv")
label_encoder = []
columns = dataset.columns
types = dataset.dtypes.values
for j in range(len(types)):
    name = types[j]
    if name == 'object': #finding column with object type
        le = LabelEncoder()
        dataset[columns[j]] = pd.Series(le.fit_transform(dataset[columns[j]].astype(str)))#encode all str columns to numeric
        label_encoder.append([columns[j], le])
dataset.fillna(0, inplace = True)
clinical_Y = dataset['stroke'].ravel()
dataset.drop(['stroke'], axis = 1,inplace=True)
clinical_X = dataset.values

indices = np.arange(clinical_X.shape[0])
np.random.shuffle(indices)
clinical_X = clinical_X[indices]
clinical_Y = clinical_Y[indices]

image_X = np.load('model/X.npy')
image_Y = np.load('model/Y.npy')


image_X = image_X.astype('float32')
image_X = image_X/255

indices = np.arange(image_X.shape[0])
np.random.shuffle(indices)
image_X = image_X[indices]
image_Y = image_Y[indices]
image_Y = to_categorical(image_Y)
image_X_train, image_X_test, image_y_train, image_y_test = train_test_split(image_X, image_Y, test_size=0.2) #split dataset into train and test

cnn_model = Sequential()
cnn_model.add(Convolution2D(32, (3 , 3), input_shape = (image_X_train.shape[1], image_X_train.shape[2], image_X_train.shape[3]), activation = 'relu'))
cnn_model.add(MaxPooling2D(pool_size = (2, 2)))
cnn_model.add(Convolution2D(32, (3, 3), activation = 'relu'))
cnn_model.add(MaxPooling2D(pool_size = (2, 2)))
cnn_model.add(Flatten())
cnn_model.add(Dense(units = 256, activation = 'relu'))
cnn_model.add(Dense(units = image_y_train.shape[1], activation = 'softmax'))
cnn_model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
if os.path.exists("model/cnn_weights.hdf5") == False:
    model_check_point = ModelCheckpoint(filepath='model/cnn_weights.hdf5', verbose = 1, save_best_only = True)
    hist = cnn_model.fit(image_X_train, image_y_train, batch_size = 32, epochs = 30, validation_data=(image_X_test, image_y_test), callbacks=[model_check_point], verbose=1)
    f = open('model/cnn_history.pckl', 'wb')
    pickle.dump(hist.history, f)
    f.close()    
else:
    cnn_model.load_weights("model/cnn_weights.hdf5")

predict = cnn_model.predict(image_X_test)
predict = np.argmax(predict, axis=1)
y_test1 = np.argmax(image_y_test, axis=1)
conf_matrix = confusion_matrix(y_test1, predict)
calculateMetrics("CNN", y_test1, predict)

clinical_Y = to_categorical(clinical_Y)
scaler = StandardScaler()
clinical_X = scaler.fit_transform(clinical_X)
clinical_X = np.reshape(clinical_X, (clinical_X.shape[0], clinical_X.shape[1], 1))
                                  
clinical_X_train, clinical_X_test, clinical_y_train, clinical_y_test = train_test_split(clinical_X, clinical_Y, test_size=0.2) #split dataset into train and test

lstm_model = Sequential()#defining deep learning sequential object
#adding LSTM layer with 100 filters to filter given input X train data to select relevant features
lstm_model.add(LSTM(32,input_shape=(clinical_X_train.shape[1], clinical_X_train.shape[2])))
#adding dropout layer to remove irrelevant features
lstm_model.add(Dropout(0.5))
#adding another layer
lstm_model.add(Dense(32, activation='relu'))
#defining output layer for prediction
lstm_model.add(Dense(clinical_y_train.shape[1], activation='softmax'))
#compile LSTM model
lstm_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#start training model on train data and perform validation on test data
#train and load the model
if os.path.exists("model/lstm_weights.hdf5") == False:
    model_check_point = ModelCheckpoint(filepath='model/lstm_weights.hdf5', verbose = 1, save_best_only = True)
    hist = lstm_model.fit(clinical_X_train, clinical_y_train, batch_size = 8, epochs = 50, validation_data=(clinical_X_test, clinical_y_test), callbacks=[model_check_point], verbose=1)
    f = open('model/lstm_history.pckl', 'wb')
    pickle.dump(hist.history, f)
    f.close()    
else:
    lstm_model.load_weights("model/lstm_weights.hdf5")
#perform prediction on test data    
predict = lstm_model.predict(clinical_X_test)
predict = np.argmax(predict, axis=1)
y_test1 = np.argmax(clinical_y_test, axis=1)
calculateMetrics("LSTM", y_test1, predict) 

def TrainModels(request):
    if request.method == 'GET':
        global accuracy, precision, recall, fscore, conf_matrix
        labels = ['Normal', 'Stroke']
        output='<div class="table-responsive"><table class="table table-bordered table-striped table-hover align-middle text-center"><thead class="table-dark"><tr>'
        output += '<th>Algorithm</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F-Score</th>'
        output += '</tr></thead><tbody>'
        algorithms = ['CNN', 'LSTM']
        for i in range(len(algorithms)):
            output += '<tr><td><strong>'+algorithms[i]+'</strong></td><td>'+str(round(accuracy[i],2))+'%</td><td>'+str(round(precision[i],2))+'%</td>'
            output += '<td>'+str(round(recall[i],2))+'%</td><td>'+str(round(fscore[i],2))+'%</td></tr>'
        output += '</tbody></table></div><br/>'
        df = pd.DataFrame([['CNN','Accuracy',accuracy[0]],['CNN','Precision',precision[0]],['CNN','Recall',recall[0]],['CNN','FSCORE',fscore[0]],
                           ['LSTM','Accuracy',accuracy[1]],['LSTM','Precision',precision[1]],['LSTM','Recall',recall[1]],['LSTM','FSCORE',fscore[1]],
                          ],columns=['Parameters','Algorithms','Value'])

        figure, axis = plt.subplots(nrows=1, ncols=2,figsize=(10, 3))#display original and predicted segmented image
        axis[0].set_title("Confusion Matrix Prediction Graph")
        axis[1].set_title("All Algorithms Performance Graph")
        ax = sns.heatmap(conf_matrix, xticklabels = labels, yticklabels = labels, annot = True, cmap="viridis" ,fmt ="g", ax=axis[0]);
        ax.set_ylim([0,len(labels)])    
        df.pivot("Parameters", "Algorithms", "Value").plot(ax=axis[1], kind='bar')
        plt.title("All Algorithms Performance Graph")
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        #plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        plt.clf()
        plt.cla()
        context= {'data':output, 'img': img_b64}
        return render(request, 'UserScreen.html', context)

def PredictAction(request):
    if request.method == 'POST':
        global scaler, label_encoder
        labels = ['<font size=3 color=green>Normal</font>', '<font size=3 color=red>Stroke</font>']
        cnn_model = load_model("model/cnn_weights.hdf5")
        lstm_model = load_model("model/lstm_weights.hdf5")
        gender = request.POST.get('t1', False)
        age = request.POST.get('t2', False)
        hypertension = request.POST.get('t3', False)
        glucose = request.POST.get('t4', False)
        bmi = request.POST.get('t5', False)
        smoking = request.POST.get('t6', False)
        myfile = request.FILES['t7'].read()
        fname = request.FILES['t7'].name
        if os.path.exists('StrokeApp/static/'+fname):
            os.remove('StrokeApp/static/'+fname)
        with open('StrokeApp/static/'+fname, "wb") as file:
            file.write(myfile)
        file.close()

        testData = []
        testData.append([gender, int(age), int(hypertension), float(glucose), float(bmi), smoking])
        testData = pd.DataFrame(testData, columns=['gender','age','hypertension','avg_glucose_level','bmi','smoking_status'])
        for j in range(len(label_encoder)):
            le = label_encoder[j]
            testData[le[0]] = pd.Series(le[1].transform(testData[le[0]].astype(str)))#encode all str columns to numeric
        testData.fillna(0, inplace = True)
        testData = testData.values
        testData = scaler.transform(testData)
        testData = np.reshape(testData, (testData.shape[0], testData.shape[1], 1))
        clinical_probs = lstm_model.predict(testData)
        lstm_predict = np.argmax(clinical_probs)
        sm = ['Smokes', 'Formerly Smoked', 'Never Smoked']
        hypertension_label = "No" if hypertension == "0" else "Yes"
        output = '<div class="table-responsive"><table class="table table-bordered table-striped table-hover align-middle text-center">'
        output += '<thead class="table-dark"><tr>'
        output += '<th>Gender</th><th>Age</th><th>Hypertension</th><th>Glucose</th><th>BMI</th><th>Smoking</th>'
        output += '</tr></thead><tbody><tr>'
        output += '<td>'+gender+'</td>'
        output += '<td>'+age+'</td>'
        output += '<td>'+hypertension_label+'</td>'
        output += '<td>'+glucose+'</td>'
        output += '<td>'+bmi+'</td>'
        output += '<td>'+smoking+'</td>'
        output += '</tr></tbody></table></div><br/>'
        image = cv2.imread('StrokeApp/static/'+fname)
        img = cv2.resize(image, (32,32))
        im2arr = np.array(img)
        im2arr = im2arr.reshape(1,32,32,3)
        img = np.asarray(im2arr)
        img = img.astype('float32')
        img = img/255
        cnn_probs = cnn_model.predict(img)
        cnn_predict = np.argmax(cnn_probs)
        output1 = "LSTM Clinical Prediction = "+labels[lstm_predict]+"<br/>"
        output1 += "CNN Image Prediction = "+labels[cnn_predict]+"<br/><br/>"
        cnn_probs = cnn_probs.ravel()
        print(cnn_probs)
        output1 += "Normal Score = "+str(round(cnn_probs[0], 3))+"<br/>"
        output1 += "Stroke Score = "+str(round(cnn_probs[1], 3))+"<br/>"
        height = cnn_probs
        bars = ['Normal', 'Stroke']
        y_pos = np.arange(len(bars))
        plt.figure(figsize = (4, 3)) 
        plt.bar(y_pos, height)
        plt.xticks(y_pos, bars)
        plt.xlabel("Stroke Type")
        plt.ylabel("Probability")
        plt.title("Stroke & Normal Probability")
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        plt.clf()
        plt.cla()
        context= {'data':output+output1, 'img': img_b64}
        return render(request, 'UserScreen.html', context)

def Predict(request):
    if request.method == 'GET':
       return render(request, 'Predict.html', {})    

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})    

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})   

def UserLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'stroke',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username, password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    uname = username
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'UserLogin.html', context)        
    
def RegisterAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'stroke',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    status = "Username already exists"
                    break
        if status == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'stroke',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = "Signup process completed"
        context= {'data': status}
        return render(request, 'Register.html', context)

def LoadDataset(request):
    if request.method == 'GET':
        global image_X
        output = "Total Stroke images found in Dataset = "+str(image_X.shape[0])
        output += "<br/>Labels found in Dataset = Normal &amp; Stroke<br/><br/>"
        dataset = pd.read_csv("Clinical_data.csv")
        columns = dataset.columns
        dataset = dataset.values
        output += '<div class="table-responsive"><table class="table table-bordered table-striped table-hover align-middle text-center"><thead class="table-dark"><tr>'
        for i in range(len(columns)):
            output += '<th>'+columns[i]+'</th>'
        output += '</tr></thead><tbody>'
        for i in range(len(dataset)):
            output += '<tr>'
            for j in range(len(dataset[i])):
                output += '<td>'+str(dataset[i,j])+'</td>'
            output += '</tr>'
        output += '</tbody></table></div>'
        #print(output)
        context= {'data':output}
        return render(request, 'UserScreen.html', context)      

