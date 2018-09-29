from PIL import Image
import numpy as np
import time
import os
import requests
import json

RANDOM_IMAGE_SIZE = 480

def put_mjpeg(relative_file_path, cam_id='test', mjpeg_cam_url='http://localhost:5050/cam_info'):
    """
    cam_id: string
    relative_file_path: path of the jpeg file which is relative to "images" folder of "docker-mjpeg-server"
    """
    data = {"file_path": relative_file_path}
    mjpeg_cam_put_url = '%s/%s' % (mjpeg_cam_url, cam_id)
    response = requests.put(mjpeg_cam_put_url, json.dumps(data), headers= {'Content-Type': 'application/json'})
    return response.status_code

out_folder = 'images'
while True:
    img_name = 'img_%s.png' %  str(time.time())
    imarray = np.random.rand(RANDOM_IMAGE_SIZE, RANDOM_IMAGE_SIZE, 3) * 255
    im = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
    im.save(os.path.join(out_folder, img_name))
    print('Generated image @', img_name)
    put_mjpeg(relative_file_path=img_name)
    time.sleep(0.04)
