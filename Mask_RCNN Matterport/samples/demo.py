#!/usr/bin/env python
# coding: utf-8

# # Mask R-CNN Demo
# 
# A quick intro to using the pre-trained model to detect and segment objects.

# In[1]:


import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
from itertools import groupby
import tweepy
import textblob
import pandas as pd
import image_utils

# Root directory of the project
ROOT_DIR = os.path.abspath("../")

# Import Mask RCNN
print("##########################################################\n",os.getcwd())
sys.path.append(ROOT_DIR)  # To find local version of the library
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n",os.getcwd())
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
import coco
from itertools import groupby as gb


# get_ipython().run_line_magic('matplotlib', 'inline')

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "images")


# ## Configurations
#
# We'll be using a model trained on the MS-COCO dataset. The configurations of this model are in the ```CocoConfig``` class in ```coco.py```.
#
# For inferencing, modify the configurations a bit to fit the task. To do so, sub-class the ```CocoConfig``` class and override the attributes you need to change.

# In[2]:


class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()


# ## Create Model and Load Trained Weights

# In[3]:


# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)


# ## Class Names
#
# The model classifies objects and returns class IDs, which are integer value that identify each class. Some datasets assign integer values to their classes and some don't. For example, in the MS-COCO dataset, the 'person' class is 1 and 'teddy bear' is 88. The IDs are often sequential, but not always. The COCO dataset, for example, has classes associated with class IDs 70 and 72, but not 71.
#
# To improve consistency, and to support training on data from multiple sources at the same time, our ```Dataset``` class assigns it's own sequential integer IDs to each class. For example, if you load the COCO dataset using our ```Dataset``` class, the 'person' class would get class ID = 1 (just like COCO) and the 'teddy bear' class is 78 (different from COCO). Keep that in mind when mapping class IDs to class names.
#
# To get the list of class names, you'd load the dataset and then use the ```class_names``` property like this.
# ```
# # Load COCO dataset
# dataset = coco.CocoDataset()
# dataset.load_coco(COCO_DIR, "train")
# dataset.prepare()
#
# # Print class names
# print(dataset.class_names)
# ```
#
# We don't want to require you to download the COCO dataset just to run this demo, so we're including the list of class names below. The index of the class name in the list represent its ID (first class is 0, second is 1, third is 2, ...etc.)

# In[4]:


# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',	
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']


# ## Run Object Detection

# In[11]:


# Load a random image from the images folder
#file_names = next(os.walk(IMAGE_DIR))[2]
image_path = "/home/shivansh/Desktop/DE_resnet_unet_hyb/images/skate_board.jpg"
image = skimage.io.imread(image_path)
image = image_utils.scale_image(image)
# image = image_utils.center_crop(image)


# Run detection
results = model.detect([image], verbose=1)

# Visualize results
r = results[0]

person_area = visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
                            class_names, r['scores'])

# detection_list = [[]]
# person_area_list = [[]]
# l_new = []
# p_new = np.argsort(person_area)

# # print("\t\tperson_area",person_area)
# l = r['class_ids']

# for i in p_new:
#     l_new.append(l[i])

# for i in l_new:
#     person_area_list[0].append(class_names[i])
# person_area_list.append(np.sort(person_area))
# person_area_list[1] = person_area_list[1].tolist()
# while("person" in person_area_list[0]):
#     print(person_area_list[0][i])
#     index = person_area_list[0].index("person")
#     person_area_list[0].remove("person")
#     person_area_list[1].remove(person_area_list[1][index])


# l = list(np.sort(l))
# l = list(filter(lambda a: a != 1, l))  # to remove person classes from detection array i.e. person class id = 1


# for i in l:
#     if class_names[i] not in detection_list[0]:
#         detection_list[0].append(class_names[i])

# sorted_freq = [len(list(group)) for key, group in groupby(l)]

# detection_list.append(sorted_freq)

# print("detection_area_list:",person_area_list)
# print("detection_class_count:",detection_list)

# consumer_key = "QHdoSPNYZdSrH2SITinjXH7B1"
# consumer_secret = "FbN8B5FtrwRjdJvm0lZpHwFITC6JLfkDNqlDkKpkpiVAJqX0jI"

# access_token = "428768497-5PaJi8GvUSqyHkOb6wA6NM4MVECQstWlLpzTWHIC"
# access_token_secret = "wOLACcTCYchHJOBs1P9UaxDaucSHUaJyapa9OJhMVuGuE"

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

# list_user_data = [[]]
# print("\t\t searched for ",detection_list[0][0])
# query = [detection_list[0][0]]

# public_tweets = api.search(query, count=15, lang='en', tweet_mode='extended', geocode="43.653226,-79.383184,50mi")

# for tweets in public_tweets:
#     print("yes")
# pol = []
# sub = []
# for tweets in public_tweets:
#     print("\n\nNew Tweet")

#     # print(tweets.retweeted)

#     if "RT" in tweets.full_text:
#         print(tweets.full_text)

#         print("Retweeted")

#         print(tweets.retweeted_status.full_text)
#     else:
#         print(tweets.full_text)
#     print(tweets.created_at)
#     print(tweets.user.location)
#     print(tweets.user.name)

#     analysis = textblob.TextBlob(tweets.full_text)
#     '''
#     lan = analysis.detect_language()
#     if(lan != 'en'):
#         tran = analysis.translate(to='en')
#         print("Changed")
#         print(tran)
#         analysis = tran
#     #print(analysis.detect_language())
#     '''

#     print(analysis.sentiment)
#     # pol.append(analysis.sentiment.polarity)
#     # sub.append(analysis.sentiment.subjectivity)
#     # df = pd.DataFrame(data=[tweet.text,tweet.user.name for tweet in public_tweets], columns=['Tweets','Name'])
# df_user_data = pd.DataFrame(
#     data=[[tweets.user.name, tweets.created_at, tweets.user.location, tweets.full_text] for tweets in public_tweets],
#     columns=['Name', 'Created On', 'location', 'Text'])
# # print(analysis.sentiment)
# file = open('/opt/lampp/htdocs/SE/Mask_RCNN Matterport/persons.txt', 'w')
# file.write("Just for fun")
# # for i in df_user_data.iloc[0]:
# #     file.write(str(i['Name'])+"\t"+str(i['Created On'])+"\t"+str(i['location'])+"\t"+str(i['Text'])+"\n")
# file.close()

# # In[ ]:




