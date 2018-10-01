import time
import os
from base_camera import BaseCamera

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    cam_img_files = {}
    curr_idx = {}
    max_idx = {}
    default_file = os.path.join(CURRENT_FOLDER, 'default.jpg')
    idx_limit = 250

    frame_recyler = {}
    FRAME_RECYLER_MAX_FILES_LIMIT = 200

    @staticmethod
    def frames(cam_id):
        while True:
            #time.sleep(1)
            img_files = Camera.cam_img_files.get(cam_id, None)
            curr_frame_idx = Camera.curr_idx.get(cam_id, -1)
            max_frame_idx = Camera.max_idx.get(cam_id, 0)
            #print(cam_id, curr_frame_idx, max_frame_idx)
            if img_files is not None and curr_frame_idx != -1:
                if os.path.isfile(img_files[curr_frame_idx]):
                    f = open(img_files[curr_frame_idx], 'rb').read()
                else:
                    f = open(Camera.default_file, 'rb').read()
                
                if curr_frame_idx != max_frame_idx - 1 and max_frame_idx != 0:
                    curr_frame_idx += 1
            else:
                f = open(Camera.default_file, 'rb').read()
                if not img_files:
                    img_files = []
                img_files.append(Camera.default_file)
                Camera.cam_img_files[cam_id] = img_files
                #print('bug')
                curr_frame_idx = 0
                
            Camera.curr_idx[cam_id] = curr_frame_idx % Camera.idx_limit
            
            return f
