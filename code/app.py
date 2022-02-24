from typing import BinaryIO
import base64
from flask import Flask, jsonify,request,send_file
from logging import FileHandler,WARNING
import cv2
import numpy as np
import matplotlib.pyplot as plt
import requests
import time
from PIL import Image

project_hash_code = '9321f92aa387'
job_hash_code = 'f33089d46803'
dataset_hash_code = "60840f857f65"
model_idx = 1
req = requests.post(
    url='http://125.227.129.220:21720/api/access-token', 
    json={
        'user_email':'learning_kit_demo@leadtek.com.tw',
        'password':'123456'
    }
)
tokens = req.json()

ip = '125.227.129.220'

port = 21720

cookie = ''
for key, value in tokens.items():
    if key in ('refresh_token', 'access_token'):
        key += '_cookie'
    cookie += f'{key}={value};'
    
my_headers = {
    'Cookie': cookie,
    'Content-Type':'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'X-CSRF-TOKEN': tokens['csrf_refresh_token'],
    'Accept': 'application/json'
}

def post_api(name_space, send_json: dict = {}):
    url = f'http://{ip}:{port}/{name_space}'
        
    r = requests.post(
        url, 
        headers=my_headers, 
        json=send_json
    )
    print(type(r))
    print(r.status_code)
    
    return r

def get_api(name_space, query_string: dict = {}):
    url = f'http://{ip}:{port}/{name_space}'
    r = requests.get(
        url, 
        headers=my_headers, 
        params=query_string
    )
    print(r.status_code)
    
    return r

def put_api(name_space, send_json: dict = {}):
    url = f'http://{ip}:{port}/{name_space}'
        
    r = requests.put(
        url, 
        headers=my_headers, 
        json=send_json
    )
    print(r.status_code)
    
    return r

def delete_api(name_space, send_json: dict = {}):
    url = f'http://{ip}:{port}/{name_space}'
        
    r = requests.delete(
        url, 
        headers=my_headers, 
        json=send_json
    )
    print(r.status_code)
    
    return r

def get_hash_code(dataset_name,job_name):
    #job_hash
    hash=[]
    
    dataset = get_api(
        f'api/projects/{project_hash_code}/datasets_list'
    )
    for i in dataset.json():
        if i['dataset_name']==dataset_name:
            hash.append(i['dataset_hash_code'])
    r = get_api(
        f'api/projects/{project_hash_code}/jobs'
    )
    for i in r.json()['columns_value']:
        if i[0]==job_name:
            hash.append(i[1])

    return hash

app = Flask(__name__)

@app.route("/upload",methods=['GET'])
def upload():
    name=request.args.get('type')
    job_hash_code = " "
    dataset_hash_code = ""
    if name=="classification":
        job_hash_code = "7354412e0f64"
        dataset_hash_code = "f2f6a3cbd574"
    else:
        job_hash_code = "f33089d46803"
        dataset_hash_code = "60840f857f65"
    r = get_api(
        f'/api/projects/9321f92aa387/datasets/{dataset_hash_code}/jobs/{job_hash_code}/models/upload_images'
    )
    return jsonify(r.json())


@app.route("/model")
def inference():
    r = get_api(
    f'api/job_data/{job_hash_code}/{model_idx}/Move-1 30.jpg'
)


@app.route("/get_token")
def get_token():
    return tokens


@app.route("/dataset_list")
def show_dataset():
    r = get_api(
        f'api/projects/{project_hash_code}/datasets_list'
    )
    return jsonify(r.json())

@app.route("/job_list")
def job_list():
    r = get_api(
        f'api/projects/{project_hash_code}/jobs'
    )
    r.json()['columns_value']
    return  jsonify(r.json()['columns_value'])

@app.route("/detection",methods=['POST','GET'])
def detect():
    if request.method=="GET":
        dataset_hash_code = "60840f857f65"
        job_hash_code = 'f1a0292e7535'
        project_hash_code = '9321f92aa387'
        name=request.args.get('name')
        r = get_api(
            f'api/projects/{project_hash_code}/datasets/{dataset_hash_code}/jobs/{job_hash_code}/models/upload_images'
        )
        
        post_api(
            f'api/inference_images_in_model',
            {
                'job_hash_code': job_hash_code,
                'model_idx': model_idx
            }
        )
        upload_images_list = get_api(
            f'api/projects/{project_hash_code}/datasets/{dataset_hash_code}/jobs/{job_hash_code}/models/upload_images'
        )
        print(upload_images_list.json()['upload_images_list'])
        filename=upload_images_list.json()['upload_images_list']
        r = get_api(
            f'api/job_data/{job_hash_code}/{model_idx}/{name}'
        )
        b_str = r.content
        nparr = np.frombuffer(b_str, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite("./result/test1.jpg",img)
        return img 
    
    
@app.route("/classify",methods=['POST','GET'])
def classify():
    if request.method == 'GET':
        name=request.args.get('name')       
        #print(request.files['file'])
        send_data = {'image': open(name, 'rb')}
        # return image or not:
        output_image = 0
        data = {'output_image': output_image}
        url = 'http://163.25.101.181:77/inference'
        print('Send image ...')
        t1 = time.time()
        response = requests.post(url, data=data, files=send_data)
        # r = json.loads(response.text)

        # result = r.content.decode("utf-8")
        if not output_image:
            print(str(response.json()['classes'][0][0]))
            return str(response.json()['classes'][0][0])
        else:
            b_str = response.content
            nparr = np.fromstring(b_str, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            print(img.shape)
            cv2.imwrite('test.jpg', img)
            print('1')
            print(response.json()['classes'])
            return response.json()
       

  

@app.route("/training", methods=['GET','POST'])
def train():
    dataset_hash_code=" "
    job_hash_code=" "
    model_name=""
    model_tag=""
    project_hash_code = '9321f92aa387'
    if request.form["model_type"]=='object detection':
        dataset_hash_code = "60840f857f65"
        job_hash_code = 'f33089d46803'
        model_name="library/object_detection__yolov4"
        model_tag="1.0.7"
    elif request.form["model_type"]=='classification':
        job_hash_code = '7354412e0f64'
        dataset_hash_code = "f2f6a3cbd574"
        model_name="library/classification__pytorch"
        model_tag="v1.0.7"
    #create job
    res=post_api(
        f'api/projects/${project_hash_code}/jobs/create', 
        {
            'job_name': request.form["job_name"],
            'model_name': model_name,
            'model_tag': model_tag,
            'project_hash_code': project_hash_code,
            'project_name': 'learningkits',
            'dataset_hash_code': dataset_hash_code,
            'dataset_name': request.form["dataset_name"],
            'job_gpu': '1',
            'job_memory': '2',
            'job_cpu': '0.5'
        }
    )
    r = get_api(
        f'api/projects/{project_hash_code}/jobs'
    )
    post_api(
        f'api/projects/{project_hash_code}/datasets/{dataset_hash_code}/jobs/{job_hash_code}/models/1/train_model'
    )
    #get job_hash
   
    return jsonify( r.json()['columns_value'])





@app.route("/log",methods=['GET','POST'])
def log():
    if request.method=='POST':
        project_hash_code = '9321f92aa387'
        hash=get_hash_code(request.form['dataset_name'],request.form['job_name'])
        print(hash)
        status = get_api(
                f'api/projects/{project_hash_code}/datasets/{dataset_hash_code}/jobs/{job_hash_code}/train_status'
            )
        log = get_api(
                f'api/projects/{project_hash_code}/datasets/{dataset_hash_code}/jobs/{job_hash_code}/models/1/train_log'
        )
        return '1'

@app.route("/progress",methods=['GET','POST'])
def progress():
    if request.method=="POST":
        print(request.form['job_name'],request.form['dataset_name'])
        hash=get_hash_code(request.form['dataset_name'],request.form['job_name'])
        print(hash)
        progress = get_api(
            f'api/projects/{project_hash_code}/datasets/{hash[0]}/jobs/{hash[1]}/models/1/train_progress'
    )
        return progress.json()


@app.route("/dataset", methods=['GET'])
def dataset():
    project_hash_code = '9321f92aa387'
    name=request.args.get('name')
    model_type=request.args.get('type')
    print(name)
    r = post_api(
    f'api/projects/{project_hash_code}/datasets/create', 
    {
        'project_hash_code': project_hash_code,
        'dataset_name': name,
    })
    print(1)
    hash = get_api(
        f'/api/projects/{project_hash_code}/datasets', 
        {
            'model_type': model_type
        }
    )

    print(2)
    print(hash.json()['datasets_hash_code'][0])
    return hash.json()['datasets_hash_code'][0]



app.run(debug=True)
