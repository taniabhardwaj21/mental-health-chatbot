# inference.py
# Loading and prediction helpers


import io
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as T
import cv2


try:
    from emotion_model.model import SmallCNN
except ImportError:
    from model import SmallCNN


# labels used during training (FER2013)
LABELS = ['angry','disgust','fear','happy','sad','surprise','neutral']


import os
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'emotion_smallcnn.pth')


# preprocessing used at training time
_transform_gray = T.Compose([
    T.Resize((48,48)),
    T.ToTensor(),
    T.Normalize((0.5,), (0.5,))
])




def load_model(device=None, model_path=MODEL_PATH):
    device = device or (torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu'))
    model = SmallCNN(n_classes=len(LABELS))
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device).eval()
    return model, device




def predict_from_pil(model, device, pil_img, face_box=None):
    """Given a PIL image (RGB) and optional face box (x,y,w,h), returns softmax probabilities dict.
    If face_box provided, crops it; else assumes image is already a face.
    """
    if face_box is not None:
        x,y,w,h = face_box
        pil_img = pil_img.crop((x, y, x+w, y+h))
    # convert to grayscale because model trained on grayscale
    pil_gray = pil_img.convert('L')
    inp = _transform_gray(pil_gray).unsqueeze(0).to(device)
    with torch.no_grad():
        out = torch.softmax(model(inp), dim=1).cpu().numpy()[0]
    probs = {LABELS[i]: float(out[i]) for i in range(len(LABELS))}
    return probs




def predict_from_bytes(model, device, image_bytes):
    pil = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    # try a simple face detection with Haarcascade; if none found, assume the image is a face
    img_np = np.array(pil)[:,:,::-1].copy()
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    if len(faces)>0:
        x,y,w,h = faces[0]
        print(f"Face detected: {x},{y},{w},{h}")
        return predict_from_pil(model, device, pil, face_box=(x,y,w,h))
    else:
        print("No face detected, using full frame")
        return predict_from_pil(model, device, pil, face_box=None)