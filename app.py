import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pickle 
import cv2
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash

# os.chdir("C:/Users/Kevin Thelly/Documents/College/ifp_2/Mask_RCNN")
ROOT_DIR = os.path.abspath("../")
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
cwd = os.getcwd()
print("------------------------------")
print(cwd)

os.chdir("./coco")

print("------------------------------")
print(os.getcwd())



# import coco
from coco import coco

MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = "mask_rcnn_coco.h5"


# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)


class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    NUM_CLASSES=81
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
#loading weights
# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir='mask_rcnn_coco.hy', config=config)

# Load weights trained on MS-COCO
model.load_weights('mask_rcnn_coco.h5', by_name=True)

# COCO Class names
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
# class_names=['BG','person']

print("-----------------")
os.chdir("../")
print(os.getcwd())

#people alone
def people():
  os.chdir("./images")
  print("----------------")
  print(os.getcwd())
  image = cv2.imread('mohan.jpg')
  
  os.chdir("../")
  print("----------------")
  print(os.getcwd())
  # dimensions=image.shape
  # print(dimensions)
  # Run detection
  print("-----------------------------------")
  print("Image read classbench")
  results = model.detect([image], verbose=1)

  # Visualize results
  r = results[0]

  rois=[]
  scores=[]
  masks=[]
  class_ids=[]
  count=0
  for i in range(r['class_ids'].size):
    if r['class_ids'][i]==1:
      count=count+1
      rois.append(r['rois'][i])
      scores.append(r['scores'][i])
      masks.append(r['masks'][i])
      class_ids.append(r['class_ids'][i])
  # rois=np.asarray(rois)
  # scores=np.asarray(scores)
  # masks=np.asarray(masks)
  # class_ids=np.asarray(class_ids)
  r1={}
  r1['rois']=rois
  r1['scores']=scores
  r1['masks']=masks
  r1['class_ids']=class_ids
  print("--------------------------------------------------")
  print("Number of People :",count)
  # ax = get_ax(1)
  # visualize.display_instances(image, r1['rois'], r1['masks'], r1['class_ids'], ['person'], r1['scores'],ax=ax)

  im = np.array(image)

  # Create figure and axes
  fig,ax = plt.subplots(1)

  # Display the image
  ax.imshow(im)
  for i in r1['rois']:
    y1, x1, y2, x2 = i
    x=(x1+x2)//2
    # y=(y1+y2)//2
    print(x1, y1, x2, y2)
    # rect = patches.Rectangle((x1+(x2 - x1)/2, y1), 50, 50,linewidth=1,edgecolor='r',facecolor='none')
    image = cv2.rectangle(image,(x, y1), (x+50, y1+50),(0,255,0),2)
    # ax.add_patch(rect)
  (50,100),40,30
  # Add the patch to the Axes
  # fig_size = plt.rcParams["figure.figsize"]
  # print(fig_size)
  # os.chdir("")
  # cv2.imwrite('C:/Users/Kevin Thelly/Documents/College/ifp_2/Mask_RCNN/ifp_model/image.png',bbox_inches='tight', pad_inches=-0.5,orientation= 'landscape')
  cv2.imwrite('./devimages/image.png',image)
  # png('C:/Users/Kevin Thelly/Documents/College/ifp_2/Mask_RCNN/ifp_model/image.png', width = 800, height = 600)
  # plt.savefig('C:/Users/Kevin Thelly/Documents/College/ifp_2/Mask_RCNN/ifp_model/foo.png', bbox_inches='tight')
  # os.chdir("C:/Users/Kevin Thelly/Documents/College/ifp_2/Mask_RCNN//ifp/Server")
  # plt.savefig('foo.png')
  # plt.show()
  print("---------------------------------")
  print("function done")
print("-----------------------------------------")
print("model done")


# app = Flask(__name__)
# app.debug=True

# @app.route('/',methods=['GET','POST'])
# def run_model():
#   # people()
#   return("done")

# app.run()
people()