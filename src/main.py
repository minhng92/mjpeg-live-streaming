#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)

__curr_idx = {}
__camera = Camera
__idx_limit = 250

def gen(camera, cam_id):
    """Video streaming generator function."""
    while True:
        ##print('Send frame: ', cam_id)
        frame = camera.frames(cam_id)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/cam_info/<cam_id>', methods=['PUT'])
def update_camera_info(cam_id):
    
    if request.json and 'file_path' in request.json:
        file_path = os.path.join('/app/images', request.json['file_path'])
        __idx_limit = request.json.get('limit', 250)
        
        # 180914
        if cam_id not in __camera.frame_recyler:
            __camera.frame_recyler[cam_id] = []

        file_list = __camera.cam_img_files.get(cam_id, [])
        
        #print("update cam: ", file_path, __idx_limit, len(file_list))
        
        if __curr_idx.get(cam_id, 0) >= __idx_limit:
            __curr_idx[cam_id] = 0
        
        if len(file_list) < __idx_limit:
            file_list.append(file_path)
        else:
            file_list[__curr_idx[cam_id]] = file_path
            
        __curr_idx[cam_id] = __curr_idx.get(cam_id, 0) + 1
        __camera.max_idx = __curr_idx
        __camera.cam_img_files[cam_id] = file_list

        # 180914: remove old files if the file# of this camera exceeds FRAME_RECYLER_MAX_FILES_LIMIT
        __camera.frame_recyler[cam_id].append(os.path.abspath(file_path))
        if len(__camera.frame_recyler[cam_id]) > 2*__camera.FRAME_RECYLER_MAX_FILES_LIMIT:
            del_list = __camera.frame_recyler[cam_id][:__camera.FRAME_RECYLER_MAX_FILES_LIMIT]
            __camera.frame_recyler[cam_id] = __camera.frame_recyler[cam_id][__camera.FRAME_RECYLER_MAX_FILES_LIMIT:]
            for img_del_path in del_list:
                try:
                    os.remove(img_del_path)
                except:
                    pass
        
    return Response({'status': 0})
    
@app.route('/mjpeg/<cam_id>', methods=['GET'])
def mjpeg(cam_id):
    """Video streaming route. Put this in the src attribute of an img tag."""
    #print("Get images")
    return Response(gen(__camera, cam_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5050)
    print('Application started...')
