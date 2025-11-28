# model.py
# Defines SmallCNN (fast to train) and a convenience MobileNetV2 wrapper if you want transfer learning.

# model.py
# Defines SmallCNN (fast to train) and a convenience MobileNetV2 wrapper if you want transfer learning.


import torch
import torch.nn as nn
import torchvision.models as models


class SmallCNN(nn.Module):
    """A small, fast CNN for FER2013-style 48x48 grayscale inputs.
    - Input shape: (B, 1, 48, 48)
    - Output: logits for n_classes
    """
    def __init__(self, n_classes=7):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(2), # 24x24


            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(2), # 12x12


            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.AdaptiveAvgPool2d(1), # 1x1


            nn.Flatten(),
            nn.Dropout(0.4),
            nn.Linear(128, n_classes)
        )


    def forward(self, x):
        return self.net(x)




class MobileNetV2Wrapper(nn.Module):
    """Wraps torchvision MobileNetV2 to accept 3-channel inputs and produce n_classes outputs.
    Use for transfer learning on larger inputs (e.g., 224x224 RGB).
    """
    def __init__(self, n_classes=7, pretrained=True):
        super().__init__()
        backbone = models.mobilenet_v2(pretrained=pretrained)
        # replace classifier
        in_features = backbone.classifier[1].in_features
        backbone.classifier[1] = nn.Linear(in_features, n_classes)
        self.model = backbone


    def forward(self, x):
        return self.model(x)