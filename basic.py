# imports and basic notebook setup
from cStringIO import StringIO
import numpy as np
import scipy.ndimage as nd
import PIL.Image
# from IPython.display import clear_output, Image, display
from google.protobuf import text_format
import os
import sys
import argparse
import caffe

# magic happens here
from deepdream import showarray, preprocess, deprocess, make_step, deepdream, net



###############################################################################
# openCV stuff
# ------------
# this is a decent way to show an image in a window (or over a network via X),
# but it's a huge pain in the ass to convert between cv2 and PIL and i have
# not been successful thus far.
#
# from what i've read, PIL is dead and openCV is standard now, so
# we should probably work towards phasing out PIL and using openCV instead. it
# has support for all languages and is probably faster than PIL.
#
# plus it has a ton of cool features like face detection, motion, image
# resizing, transformations, edge detection, various neat effects, webcams...
##############################################################################
import cv2
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
def show(img):
  open_cv_image = img[:, :, ::-1].copy() #.view(dtype=np.uint8)
  print(open_cv_image)
  cv2.imshow('image', open_cv_image.view(dtype=np.uint8))
  cv2.waitKey(30)


##############################################################################
# main function
# -------------
# don't ask, __name__ == '__main__' is just how python do.
#
# passing in arguments is totally 1337 and allows other applications to
# interface with us. this means that we can automate stuff! yeah!
# try not to commit  any hardcoded values. if possible, you should be
# passing in all parameters via command line and then setting defaults if they
# do not exist. argparse is a great library for this, i just did it the quick
# and dirty way because it was late. 
# 
# TODO: parametrize stuff
#          --scaleCoef
#         --iterations
#         --whatever parameters deepdream.deepdream has
#       break out as many tedious functions as possible and put them in a
#         utils.py or something
##############################################################################
if __name__ == '__main__':
  # # first arg is the filename of the image you want to target unintuitive? perhaps.
  # fn = sys.argv[1]
  # if not fn:
  #   print 'no source file given'
  #   exit()
  # # ^^^fuck this. it'd be nice to have the option of not using switches,
  # #    but i have a terrible, terrible feeling about it.

  # get  args if we can. nargs='?' just means it isn't required, default is the default value.
  parser = argparse.ArgumentParser()
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--filename', type=str)
  parser.add_argument('-o', '--outputdir', default='out', type=str)
  parser.add_argument('-s', '--scaleCoef', default=0.05, type=float)
  parser.add_argument('-i', '--iterations', default=100, type=int)
  args = parser.parse_args()

  if args.filename == None:
    print 'no source file'
    print 'ex: $ python basic.py -f source/file.jpg'
    exit()

  # PIL is stupid, go away PIL
  img = np.float32(PIL.Image.open(args.filename))
  print 'loaded', args.filename


  # split file name so we can make a special folder
  fn = args.filename.split('/')[-1].split('.')
  ext = fn[-1]
  fn = fn[0]
  framepath = args.outputdir+'/'+fn
  
  # make sure output path exists
  if not os.path.exists(args.outputdir):
    os.makedirs(args.outputdir)

  # # for the love of god, lets not crash after the first
  # # deepdream due to an ENOENT error... (-_-)
  # show(img)
  print "i will save at", framepath
  if not os.path.exists(framepath):
      os.makedirs(framepath)

  # code interaction is awesome!
  # uncomment this to fondle the data on open
  # useful so you don't run for hours with faulty params
  # (ctrl+d continues execution)
  import code
  code.interact(local=locals())

  # see ya on the other side
  frame = img
  h, w = frame.shape[:2]
  s = args.scaleCoef # scale coefficient
  for i in xrange(args.iterations):
      # save the original as 000.ext and hallucinations as 00i.ext
      # this also checks the save path so that we don't crash after 1 deepdream
      PIL.Image.fromarray(np.uint8(frame)).save(framepath+'/'+str(i).zfill(3)+'.'+ext)

      # only in dreams
      frame = deepdream(net, frame)

      # zoom a little
      frame = nd.affine_transform(frame, [1-s,1-s,1], [h*s/2,w*s/2,0], order=1)