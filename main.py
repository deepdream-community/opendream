#!/usr/bin/python
import numpy as np
import scipy.ndimage as nd
from random import randint


from cStringIO import StringIO
import PIL.Image
from google.protobuf import text_format

import os
import sys
import argparse

import caffe
from deepdream import deepdream, net
import random
try:
	import cv2
except ImportError:
	raise Exception ("OpenCV is not available:")

###############################################################################
# openCV Preview Window
# ------------
##############################################################################
def show(img, blob):
	cv2.namedWindow('image_process', cv2.WINDOW_AUTOSIZE)
	cv2.setWindowTitle('image_process', 'Current Blob: '+blob)
	open_cv_image = cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR) 
	open_cv_image = open_cv_image[:, :, ::-1].copy() 
	cv2.imshow('image_process', open_cv_image.view())
	cv2.waitKey(25)

##############################################################################
# Main function
# -------------
# Usage: Usage: $ python main.py -f [source/filename.jpg] -o [output dir] 
#                                -s [scale] -i [iterations] -b [all/blobname] 
#                                -z [0/1] -p [0/1] -g [0/1]
# Arguments:
# '-f', '--filename'  : Input file
# ''-o', '--outputdir': Output directory
# '-s', '--scaleCoef' : Scale Coefficient (default=0.5)
# '-i', '--iterations': Iterations (default=100)
# '-b', '--blob'      : Blob name (default=random)
# '-z', '--zoom'      : Zoom (default=0)
# '-p', '--preview'   : Preview Window (default=0)
# '-g', '--gpu'		  : Enable GPU (default=0, Assumes device ID:0)
##############################################################################

if __name__ == '__main__':
  # get  args if we can.
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--filename', type=str)
  parser.add_argument('-o', '--outputdir', default='out', type=str)
  parser.add_argument('-s', '--scaleCoef', default=0.05, type=float)
  parser.add_argument('-i', '--iterations', default=100, type=int)
  parser.add_argument('-b', '--blob', default=random.choice(net.blobs.keys()), type=str)
  parser.add_argument('-z', '--zoom', default=0, type=int)
  parser.add_argument('-p', '--preview', default=0, type=int)
  parser.add_argument('-g', '--gpu', default=0, type=int)
  args = parser.parse_args()
  
  if args.filename == None:
    print 'Error: No source file'
    print 'Usage: $ python main.py -f [source/filename.jpg] -o [output dir] -s [scale] -i [iterations] -b [all/blobname] -z [0/1] -p [0/1] -g [0/1]'
    exit()
    
  if args.gpu == 1:
	caffe.set_mode_gpu()
	caffe.set_device(0)

  # PIL is stupid, go away PIL
  img = np.float32(PIL.Image.open(args.filename))
  print 'Loaded', args.filename

  # split file name so we can make a special folder
  fn = args.filename.split('/')[-1].split('.')
  ext = fn[-1]
  fn = fn[0]
  framepath = args.outputdir+'/'+fn
  
  # make sure output path exists
  if not os.path.exists(args.outputdir):
    os.makedirs(args.outputdir)
  
  print "Output: ", framepath
  if not os.path.exists(framepath):
      os.makedirs(framepath)

  # see ya on the other side
  frame = img
  h, w = frame.shape[:2]
  s = args.scaleCoef # scale coefficient

  # run all blobs, adopted from script by Cranial_Vault
  if args.blob == 'all':
      PIL.Image.fromarray(np.uint8(frame)).save(framepath+'/source.'+ext)
      j = 0
      for blob in net.blobs.keys():
          
          safeblob = blob.replace('/', '-')
          
          #Show preview window
          if args.preview == 1:
  			show(PIL.Image.fromarray(np.uint8(frame)), safeblob)
          
          try:
            # if we've already generated this image, then don't bother
            if not os.path.exists(framepath+'/'+safeblob+'.'+ext):
                frame = deepdream(net, img, end=blob)
                PIL.Image.fromarray(np.uint8(frame)).save(framepath+'/'+safeblob+'.'+ext)
                print j, str(blob)
            else:
                print 'Skipping', blob, 'Output file exists.'
          except ValueError as err:
            print 'ValueError:', str(blob), err
            pass
          except KeyError as err:
            print 'KeyError:', str(blob), err
  else:
      safeblob = args.blob.replace('/', '-')
      for i in xrange(args.iterations):
          #Show preview window
          if args.preview == 1:
  			show(PIL.Image.fromarray(np.uint8(frame)), safeblob)
          
          # save the original as 000.ext and hallucinations as 00i.ext
          # this also checks the save path so that we don't crash after 1 deepdream
          PIL.Image.fromarray(np.uint8(frame)).save(framepath+'/'+safeblob+'--'+str(i).zfill(3)+'.'+ext)

          # only in dreams
          frame = deepdream(net, frame, end=args.blob)

          # zoom a little
          if args.zoom == 1:
           frame = nd.affine_transform(frame, [1-s,1-s,1], [h*s/2,w*s/2,0], order=1)
