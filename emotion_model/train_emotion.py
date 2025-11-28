# train_emotion.py

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as T
import pandas as pd
import numpy as np
from PIL import Image
from model import SmallCNN

class FERDataset(Dataset):
    def __init__(self, csv_file, split, transform=None):
        self.data = pd.read_csv(csv_file)
        self.data = self.data[self.data['Usage'] == split]
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        pixels = np.fromstring(row['pixels'], sep=' ')
        pixels = pixels.reshape(48, 48).astype('uint8')
        img = Image.fromarray(pixels)
        if self.transform:
            img = self.transform(img)
        label = int(row['emotion'])
        return img, label

def get_loaders(csv, batch_size=64, num_workers=2):
    transform = T.Compose([
        T.ToTensor(),
        T.Normalize((0.5,), (0.5,))
    ])
    train_ds = FERDataset(csv, 'Training', transform)
    val_ds = FERDataset(csv, 'PublicTest', transform)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    return train_loader, val_loader

def train(csv_path='fer2013.csv', epochs=12, out_path='emotion_smallcnn.pth'):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    train_loader, val_loader = get_loaders(csv_path)

    model = SmallCNN(n_classes=7).to(device)
    criterion = nn.CrossEntropyLoss()
    opt = optim.Adam(model.parameters(), lr=1e-3)

    best_val = 0.0
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            out = model(imgs)
            loss = criterion(out, labels)
            opt.zero_grad()
            loss.backward()
            opt.step()
            running_loss += loss.item() * imgs.size(0)
        avg_loss = running_loss / len(train_loader.dataset)

        # validation
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                preds = model(imgs).argmax(dim=1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)
        val_acc = correct / total
        print(f"Epoch {epoch+1}/{epochs} loss={avg_loss:.4f} val_acc={val_acc:.4f}")

        if val_acc > best_val:
            best_val = val_acc
            torch.save(model.state_dict(), out_path)
            print(f"Saved best model to {out_path} (val_acc={best_val:.4f})")

    print("Training complete")

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--csv', default='fer2013.csv')
    p.add_argument('--epochs', type=int, default=12)
    p.add_argument('--out', default='emotion_smallcnn.pth')
    args = p.parse_args()
    train(args.csv, args.epochs, args.out)