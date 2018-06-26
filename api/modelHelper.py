from PIL import Image
from io import BytesIO
from azure.storage.blob import *

import pickle
import os.path
import json
import requests
import numpy as np
import gzip

# model libraries - these can change, based on the model you are using!
import cntk as C
from cntk.ops.functions import load_model

def load_model():
    try:
        with open("./config.json", "r") as config_file:
            config = json.load(config_file)
        block_blob_service = BlockBlobService(account_name=config['blob']['account_name'], 
                                        account_key=config['blob']['account_key'])
        container = config['model']['container']
        generator = block_blob_service.list_blobs(container)
        model = None
        for blob in generator:
            if(blob.name != config['model']['name']):
                continue
            
            path = "data/{}".format(blob.name)
            if(not os.path.exists(path)):
                print('Loading model...')
                block_blob_service.get_blob_to_path(container, blob.name, path)

            model = open_cntk_model(path)
            print('Model loaded!')
        return model
    except Exception as e:
        raise Exception("Model could not be loaded. Error: {}".format(str(e)))

def open_cntk_model(path):
    if(path[-3:] == ".gz"):
        model_file = gzip.open(path,'rb').read()
    else:
        model_file = open(path, 'rb').read()
    model = C.load_model(model_file)
    return model

def label_and_prob_cntk(arr, model):
    predictions = model.eval(arr)[0]
    top_class = np.argmax(predictions)
    lables = ['croissant', 'sloth']

    return (lables[top_class], predictions[top_class])

def process_image(img_url):
    o_img = get_image(img_url)
    p_img = pad_image(o_img)
    r_img = reshape_image(p_img)
    r_arr = np.array(r_img)
    n_arr = normalize(r_arr) 
    t_arr = n_arr.astype(int).reshape(3,128,128)
    return t_arr
    
def get_image(img_url):
    response = requests.get(img_url)
    new_image = Image.open(BytesIO(response.content)).convert('RGB')
    return new_image

def pad_image(img, color = (255,255,255)):
    max_size = max(img.size)
    background = Image.new('RGB', (max_size, max_size), color)
    img_w, img_h = img.size
    bg_w, bg_h = background.size
    offset = ((int)((bg_w - img_w) / 2), (int)((bg_h - img_h) / 2))
    background.paste(img, offset)
    return background

def reshape_image(img, size = (128,128)):
    try:
        img.thumbnail(size, Image.ANTIALIAS)
        return img
    except IOError:
        print('Error')

def normalize(arr):
    """
    Linear normalization
    http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
    """
    arr = arr.astype('float')
    # Do not touch the alpha channel
    for i in range(3):
        minval = arr[...,i].min()
        maxval = arr[...,i].max()
        if minval != maxval:
            arr[...,i] -= minval
            arr[...,i] *= ( 255.0 / ( maxval - minval ) )
    return arr