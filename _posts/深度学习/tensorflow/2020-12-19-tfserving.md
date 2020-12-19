---
layout:     post
title:      "tf-serving"
subtitle:   " \"tf\""
date:       2020-12-19 18:00:00
mathjax: true
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - 工具
---
* TOC
{:toc}

# 环境准备

```
安装docker
docker pull tensorflow/serving
新建文件夹tmp/tfserving
git clone https://github.com/tensorflow/serving
```
模型训练保存
```
model_output_dir = "D:\zwt\work_test\qa_robot_test\logs\\1"
tf.saved_model.simple_save(session, model_output_dir, inputs={"char_inputs": self.model.char_inputs},
                outputs={"outputs": self.model.prediction})

在tmp文件夹下新建文件，命名为模型名称，将模型文件copy到新建文件夹下
```
-启动服务：
```
    - docker run -t --rm -p 8500:8500 -p 8501:8501 --mount type=bind,source=D:\\zwt\\docker\\tmp\\transformer\\,target=/models/transformer  -e MODEL_NAME=transformer  tensorflow/serving &
```
测试是否启动
curl http://localhost:8501/v1/models/transformer
```
    显示{"model_version_status": [
  {
   "version": "1",
   "state": "AVAILABLE",
   "status": {
    "error_code": "OK",
    "error_message": ""} }}
```
curl http://localhost:8501/v1/models/transformer/metadata
```
    {"model_spec":{"name": "transformer","signature_name": "","version": "1"},"metadata": {"signature_def":{"signature_def": {
  "serving_default": {
   "inputs": {
    "myInput": {
     "dtype": "DT_FLOAT",
     "tensor_shape": {
      "dim": [
       { "size": "-1",
        "name": ""
       }, {
        "size": "100",
        "name": ""
       }],
      "unknown_rank": false
     },
     "name": "myInput:0" }
   },
   "outputs": {
    "myOutput": {
     "dtype": "DT_FLOAT",
     "tensor_shape": {
      "dim": [
       {
        "size": "-1",
        "name": ""
       },
       {
        "size": "1",
        "name": ""
       }
      ],
      "unknown_rank": false
     },
     "name": "Sigmoid:0"
    }  }, "method_name": "tensorflow/serving/predict"
  }}}}}
```
命令框模型调用：
```
curl -d "{\"instances\": [[45, 181, 121, 22, 246, 88, 146, 25, 16, 117, 145, 231, 187, 157, 206, 191, 77, 236, 124, 68, 198, 19, 84, 193, 251, 7, 105, 229, 119, 243, 103, 90, 250, 82, 138, 9, 1, 240, 242, 133, 214, 216, 111, 189, 54, 212, 209, 169, 167, 179, 13, 249, 99, 95, 137, 55, 199, 237, 159, 183, 15, 150, 76, 104, 2, 27, 220, 149, 38, 3, 86, 8, 23, 235, 83, 12, 190, 239, 5, 140, 155, 114, 53, 135, 148, 141, 89, 232, 219, 226, 62, 33, 116, 46, 225, 49, 154, 4, 234, 222, 59, 217, 184, 163, 196, 213, 48, 42, 122, 101, 170, 233, 158, 35, 30, 52, 197, 178, 210, 56, 165, 120, 106, 129, 172, 32, 176, 18, 28, 26, 174, 221, 173, 20, 60, 40, 123, 161, 66, 72, 134, 29, 69, 100, 180, 152, 200, 11, 51, 151, 238, 252, 41, 160, 215, 218, 131, 21, 58, 203, 34, 102, 75, 207, 255, 175, 201, 164, 81, 47, 139, 162, 244, 126, 211, 192, 6, 57, 182, 195, 73, 254, 143, 70, 125, 185, 227, 130, 228, 153, 94, 248, 144, 127, 91, 202, 96, 92, 17, 98, 65, 67, 241, 87, 80, 224, 24, 147, 166, 230, 78, 112, 97, 118, 204, 186, 107, 108, 253, 43, 74, 10, 37, 245, 208, 14, 194, 110, 64, 113, 128, 79, 115, 223, 171, 247, 61, 142, 109, 132, 63, 36, 205, 31, 93, 0, 136, 177, 71, 156, 44, 188, 50, 168, 85, 39]]}" -X POST http://localhost:8501/v1/models/transformer:predict
```
restful接口访问
```
import requests
import json
import numpy

char_index = {' ': 0}


def load_dict():
    i = 0
    with open('D:\zwt\work_test\qa_robot_test\\resource\\vocab\dictionary.json', "r+", encoding="utf-8") as reader:
        items = json.load(reader)
        for charvalue in items:
            char_index[charvalue.strip()] = i + 1
            i += 1


def convert_vector(input_text, limit):
    char_vector = numpy.zeros((70), dtype=numpy.int32)
    count = len(input_text.strip().lower())
    if count > limit:
        count = limit
    for i in range(count):
        if input_text[i] in char_index.keys():
            char_vector[i] = char_index[input_text[i]]
    return numpy.array([char_vector])


load_dict()
t = convert_vector('哪里有汉堡', 70)
pdata = {"instances": t.tolist()}
param = json.dumps(pdata)
res = requests.post('http://localhost:8501/v1/models/transformer:predict', data=param)
print(res.text)
```
grpc访问：
```
import numpy as np
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from grpc.beta import implementations


# 利用grpc 进行连接
channel = implementations.insecure_channel("127.0.0.1", 8500)
stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
request = predict_pb2.PredictRequest()
# 模型的名称
request.model_spec.name = "transformer"
# 签名的名称
# request.model_spec.signature_name = "predict"

# 每次只支持传入一条数据进行预测，传入数据时要注意数据格式和模型定义时的格式一致
request.inputs['char_inputs'].CopyFrom(tf.contrib.util.make_tensor_proto(t[0], dtype=tf.int32, shape=[1, 256]))

# response返回的是protobuff的格式
response = stub.Predict.future(request)
# 去除预测的数值，对于many to many 的LSTM，输出的结果是多个，读取成列表的形式
res_list = response.result().outputs["outputs"].float_val
print(res_list)
```


多模型配置：
```
在tmp文件夹下新建multiModel文件，在其中分别存放保存好的模型
在multiModel文件夹下新建model.config文件
```
文件中写入
```
model_config_list:{
    config:{
      name:"test1",
      base_path:"/models/models/test1",
      model_platform:"tensorflow",
      model_version_policy{
        specific {
            versions: 1
            versions: 2
        }
    }
    },
  config: {
    name: "model2",
    base_path: "/models//models/model2",
    model_platform: "tensorflow",
      model_version_policy{
        specific {
            versions: 1
            versions: 2
        }
    }
  }
}

也可以通过：
model_platform:"tensorflow",
      model_version_policy:{
        all:{}
      }
      来进行版本控制
      
      
版本切换：
model_version_policy {
  specific {
    versions: 42
    versions: 43
  }
}
version_labels {
  key: 'stable'
  value: 43
}
version_labels {
  key: 'canary'
  value: 43
}
```
如果需要版本控制，加入上述文件后访问的时候需要
```
启动命令后加上  --model_config_file=/models/models/models.config
访问时：http://localhost:8501/v1/models/model1/versions/1:predict
```