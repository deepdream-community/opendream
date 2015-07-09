# imports and basic notebook setup
from cStringIO import StringIO
import numpy as np
import scipy.ndimage as nd
import PIL.Image
from IPython.display import clear_output, Image, display
from google.protobuf import text_format

import cv2 #Move this line to the beginning of the script
import caffe

import deepdream as dd
showarray = dd.showarray
preprocess = dd.preprocess
deprocess = dd.deprocess
make_step = dd.make_step
deepdream = dd.deepdream


img = np.float32(PIL.Image.open('dancer_000000.bmp'))
h,w,c = img.shape
hallu = deepdream(net, img)
np.clip(hallu, 0, 255, out=hallu)
PIL.Image.fromarray(np.uint8(hallu)).save('newdancer_000000.jpg')
grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
for i in xrange(98):
    previousImg = img
    previousGrayImg = grayImg    
    img = np.float32(PIL.Image.open('dancer_%06d.bmp'%(i+1)))
    grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    flow = cv2.calcOpticalFlowFarneback(previousGrayImg, grayImg, pyr_scale=0.5, levels=3, winsize=15, iterations=3, poly_n=5, poly_sigma=1.2, flags=0)
    flow = -flow
    flow[:,:,0] += np.arange(w)
    flow[:,:,1] += np.arange(h)[:,np.newaxis]
    halludiff = hallu - previousImg
    halludiff = cv2.remap(halludiff, flow, None, cv2.INTER_LINEAR)   
    hallu = img + halludiff
    hallu = deepdream(net, hallu)
    np.clip(hallu, 0, 255, out=hallu)
    PIL.Image.fromarray(np.uint8(hallu)).save('newdancer_%06d.jpg'%(i+1))