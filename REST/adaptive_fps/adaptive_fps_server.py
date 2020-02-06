#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:47:42 2019

@author: viktor
"""

"""
Created on Thu Mar 28 15:30:51 2019

@author: viktor
"""
import sys
sys.path.append("..")

#import argparse
import numpy as np
import cv2
from flask import Flask, request, jsonify
import base64

class FlowAlgo:

    def get_flow(self, prev_frame, next_frame):
        return None


class FlowAlgoFarner(FlowAlgo):
    pyr_scale = 0.5
    levels = 5
    winsize = 15
    iterations = 3
    poly_n = 5
    poly_sigma = 1.2
    flags = 0
     
    def get_flow(self, prev_frame, next_frame):
        return cv2.calcOpticalFlowFarneback(prev_frame, next_frame, None, self.pyr_scale, self.levels, self.winsize, self.iterations, self.poly_n, self.poly_sigma, self.flags)

    
##################### Movement detector #########################

        
class MovementDetector:
    threshold = 0.5
    resize_factor = 0.1
    flow_algo = FlowAlgoFarner()
    last_img = None
    flow_img = None
    flow_to_watch_img = None
    movement_sum = 0
    
    def process_frame(self, img):
        img_small = cv2.resize(img, (0, 0), fx=self.resize_factor, fy=self.resize_factor)
        img_grey = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)

        if self.last_img is None:
            self.last_img = img_grey
            return True
        
        img_flow = self.flow_algo.get_flow(self.last_img, img_grey)
        avg_x = np.average(img_flow[..., 0])
        avg_y = np.average(img_flow[..., 1])
        mag, ang = cv2.cartToPolar(img_flow[..., 0], img_flow[..., 1])
        hsv = np.zeros_like(img_small)    
        hsv[...,1] = 255
        hsv[...,0] = ang*180/np.pi/2     
        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)           
        bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
        self.movement_sum += avg_x * avg_x + avg_y * avg_y
        moves = self.movement_sum > self.threshold
        if moves:
            self.movement_sum = 0
            
        self.flow_to_watch_img = bgr
        self.flow_img = img_flow
        
        if moves:
            self.last_img = img_grey
        
        return moves



app = Flask(__name__)

movement_detector = MovementDetector()

@app.route('/api/add_message', methods=['GET', 'POST'])
def add_message():
    content = request.json
    global movement_detector
    movement_detector.resize_factor = content['resize_factor']
    movement_detector.threshold = content['threshold']
    enc = content['image']
    dec = base64.b64decode(enc)
    jpg_as_np = np.frombuffer(dec, dtype=np.uint8)
    image = cv2.imdecode(jpg_as_np, flags = 1)
    moves = movement_detector.process_frame(image)
    
    return jsonify({"keep_frame" : int(moves)})

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug = True)

        
