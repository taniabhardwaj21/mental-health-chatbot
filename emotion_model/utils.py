# utils.py
# Utility helpers: detection, alignment stub, smoothing buffer


import cv2
import numpy as np
from collections import deque
from PIL import Image

# utils.py
# Utility helpers: detection, alignment stub, smoothing buffer


import cv2
import numpy as np
from collections import deque
from PIL import Image


cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')




def detect_first_face_bgr(img_bgr):
    """Detects the first face in a BGR numpy image and returns (x,y,w,h) or None."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    if len(faces) == 0:
        return None
    return tuple(map(int, faces[0]))




def align_face_stub(img_pil, face_box=None):
    """Stub for alignment.
    Real alignment requires landmarks (eyes, nose) and a similarity transform.
    For now we simply crop the face_box if given. Keep this function so you can upgrade later.
    """
    if face_box is None:
        return img_pil
    x,y,w,h = face_box
    return img_pil.crop((x, y, x+w, y+h))




class Smoother:
    """Keeps a sliding window of probability vectors and returns averaged probabilities."""
    def __init__(self, n=5):
        self.n = n
        self.buf = deque(maxlen=n)


    def add(self, probs_dict):
        # convert to vector in LABELS order
        vec = [probs_dict[k] for k in sorted(probs_dict.keys(), key=lambda k: k)]
        self.buf.append(np.array(vec))


    def average(self):
        if len(self.buf) == 0:
            return None
        avg = np.mean(np.stack(list(self.buf)), axis=0)
        # map back to dict by LABELS order
        # IMPORTANT: consumer should use LABELS from inference.py for label order
        return avg.tolist()