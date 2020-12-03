from __future__ import print_function
#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Test scprit

"""

import os, argparse
import numpy as np
import cv2

from keras.models import Model
from keras.layers import Input

from BaseModel import ShortCutNet
from helper import init_gpu

# set gpu id with "0", "1", "2"
init_gpu("0")


ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True,
                help = 'path to input image')
ap.add_argument('-od', '--output-dir', default='output',
                help='output directory')
ap.add_argument('--debug', default=False, action='store_true',
                help='turn on debug mode')
args = ap.parse_args()

if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

# PATH
path_weights = './ModelSave/DeblurSHC19ConvLayers.hdf5'

# input image dimensions
num_of_dim = 1

# Kernel to crop
kernel_crop = 24

def main():

    input_dim = (None, None, num_of_dim)

    #DeblurNet = ShortCutNet().DeblurResidualNet(input_dim, 6)
    DeblurNet = ShortCutNet().DeblurSHCNet(input_dim, 15)
    DeblurNet.summary()

    input_blur = Input(shape=(input_dim))
    out_deblur = DeblurNet(input_blur)

    # Model
    model = Model(inputs = input_blur, outputs = out_deblur)
    model.summary()
    model.load_weights(path_weights, by_name=True)

    # test
    x = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE) # Read as gray image
    x = x.reshape(x.shape[0], x.shape[1], num_of_dim) / 255.0

    pred = model.predict(np.expand_dims(x, axis=0))

    pred = pred.reshape(x.shape[0] - kernel_crop, x.shape[1] - kernel_crop, num_of_dim)
    outfilename = os.path.join(args.output_dir, os.path.basename(args.image)[:-4]+'_final.jpg')
    cv2.imwrite( outfilename, pred * 255.0)
    print('Saved to file {}'.format(outfilename))

if __name__ == '__main__':
    main()