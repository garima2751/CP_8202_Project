import numpy as np
from flask import Flask, request, jsonify, render_template
import simpletransformers
import pandas as pd
import requests
from simpletransformers.ner import NERModel
import json 
import io
from flask_csv import send_csv
from flask import make_response

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST',"GET"])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [x for x in request.form.values()]
    print(int_features)

    sentence = int_features[0]
    tags = ['I-Standard','I-GUI','O','I-Language','B-API','B-Language','I-API','B-Verb','I-Core','B-GUI','B-Standard','I-User','I-Hardware','I-Verb','B-Adjective','B-Hardware','B-Core','B-User']
    model = NERModel('bert', 'NERMODEL1', labels=tags,
                        args={
                        "save_eval_checkpoints": False,
                        "save_steps": -1,
                        "output_dir": "NERMODEL",
                        'overwrite_output_dir': False,
                        "save_model_every_epoch": False,
                        'reprocess_input_data': False, 
                        "train_batch_size": 10,'num_train_epochs': 3,"max_seq_length": 100, "gradient_accumulation_steps": 8}, use_cuda=False)

    predictions, raw_outputs = model.predict([sentence])


    if int_features[1] == 'display':
     
        result = json.dumps(predictions[0])
        
        return render_template('index.html', prediction_text=result)

    elif int_features[1] == 'getcsv':
        l=[]
        print(predictions[0])
        print(predictions[0][0])
        print(type(predictions[0][0]))
        for i in predictions[0]:
            dic={}
            for j in i.keys():
                dic['word']=j
                dic['tag']=i[j]
            l.append(dic)
        print(l)
        return send_csv(l,"tags.csv",["word","tag"])


if __name__ == "__main__":
    app.run(debug=True)


