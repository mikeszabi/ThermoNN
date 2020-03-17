#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:00:10 2019

@author: viktor
"""

import requests
import cv2
import base64
import os

def adaptive_fps_client(img, resize_factor, threshold):
    retval, buffer = cv2.imencode('.jpg', img)
    img_buffer = base64.b64encode(buffer)
    json_img = {'image' : img_buffer.decode('UTF-8'), 'resize_factor' : resize_factor, 'threshold' : threshold}
    res = requests.post('http://localhost:5000/api/add_message', json = json_img)
    reply = res.json()
    return reply['keep_frame']
    
    
def multi_frame_test(images_path, resize_factor, threshold, image_size):
    for img_name in sorted(os.listdir(images_path)):
        image_path = os.path.join(images_path, img_name)
        img = cv2.resize(cv2.imread(image_path), image_size)
        moves = adaptive_fps_client(img, resize_factor, threshold)
        if not moves:
            img[..., 0] = 0
        cv2.imshow('image', img)
        cv2.waitKey(1)
        
    cv2.destroyAllWindows()

def main():
    image_size = (272, 512)
    images_path = '/home/viktor/Downloads/---' 
    resize_factor = 0.25 
    threshold = 0.5
    
    multi_frame_test(images_path, resize_factor, threshold, image_size)        
        
if __name__ == '__main__':
    main()

