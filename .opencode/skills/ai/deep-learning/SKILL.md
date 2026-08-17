---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: deep-learning
description: Deep learning with PyTorch covering training loops, CNNs, transfer learning, regularization and evaluation for neural network, vision or LLM models.
category: ai
version: 0.1.0
author: devtiagoabreu
tags: [deep-learning, pytorch, neural-networks, cnn, transfer-learning, training]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Python 3.9 or newer
  - PyTorch installed (`pip install torch`)
  - A CUDA GPU for anything beyond small experiments
  - '`numpy`, `matplotlib` for data handling and visualization'
provides:
  - Reproducible training loop patterns
  - CNN architecture building blocks
  - Transfer learning workflows
  - Regularization and debugging techniques
  - Model evaluation and checkpointing
difficulty: intermediate
frameworks: [pytorch, torchvision, lightning]
languages: [python]
---

# Deep Learning with PyTorch

## Overview

Build, train, evaluate, and debug neural networks that are **reproducible** and
**correct**. This skill focuses on the workflow that actually produces working
models: data loading, training loops, monitoring, and evaluation — not on
copying architectures.

## Prerequisites

- Python 3.9 or newer with PyTorch installed (`pip install torch`)
- A CUDA GPU for anything beyond small experiments
- `numpy` and `matplotlib` for data handling and visualization

## Core Principles

- **Fix the seed** everywhere (Python, NumPy, PyTorch, CUDA) so runs are reproducible.- **Pin versions** in `requirements.txt` (torch, torchvision, CUDA runtime). GPU bit-rot is real.
- **Track everything**: loss, metrics, LR, gradients. If you can't plot it, you can't debug it.
- **Start tiny**: a model that overfits one batch trains faster than one that fails on the full set.
- **Evaluate on data the model has never seen**, in the same distribution it will see in production.

## Reproducible Setup

```python
import random
import numpy as np
import torch

def seed_everything(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

## 1. Data Loading

Use `torch.utils.data.Dataset` + `DataLoader` (never hand-rolled batches):

```python
from torch.utils.data import Dataset, DataLoader

class ImageDataset(Dataset):
    def __init__(self, paths, labels, transform=None):
        self.paths = paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        img = load_image(self.paths[idx])  # PIL or numpy
        if self.transform:
            img = self.transform(img)
        return img, self.labels[idx]

train_loader = DataLoader(
    train_ds, batch_size=32, shuffle=True,
    num_workers=4, pin_memory=True, persistent_workers=True,
)
```

### Transform pipeline

Compose vision transforms: `Resize -> RandomHorizontalFlip -> ToTensor -> Normalize(mean, std)`. For pretrained ImageNet models reuse the model's own normalization stats.

## 2. Model Definition

```python
import torch.nn as nn

class SmallCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1), nn.Flatten(),
            nn.Dropout(0.3), nn.Linear(128, num_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))
```

## 3. Training Loop (single script, reproducible)

```python
import torch
from torch.utils.tensorboard import SummaryWriter

def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss = 0.0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item() * images.size(0)
    return total_loss / len(loader.dataset)

def evaluate(model, loader, criterion, device):
    model.eval()
    total, correct, loss = 0, 0, 0.0
    with torch.inference_mode():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss += criterion(outputs, labels).item() * images.size(0)
            correct += (outputs.argmax(1) == labels).sum().item()
            total += labels.size(0)
    return loss / total, correct / total

device = "cuda" if torch.cuda.is_available() else "cpu"
model = SmallCNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)
writer = SummaryWriter()

for epoch in range(1, 51):
    train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
    val_loss, val_acc = evaluate(model, val_loader, criterion, device)
    scheduler.step()
    writer.add_scalars("loss", {"train": train_loss, "val": val_loss}, epoch)
    writer.add_scalar("acc/val", val_acc, epoch)
    torch.save({"epoch": epoch, "model": model.state_dict(),
                "optimizer": optimizer.state_dict()}, f"ckpt-{epoch}.pt")
    print(f"epoch {epoch}: train {train_loss:.4f} | val {val_loss:.4f} acc {val_acc:.3f}")
```

## 4. Transfer Learning (recommended over training from scratch)

Fine-tune a pretrained backbone when you have limited data:

```python
import torchvision.models as models

backbone = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
backbone.fc = nn.Linear(backbone.fc.in_features, num_classes)

# Freeze backbone, train head first
for param in backbone.parameters():
    param.requires_grad = False
backbone.fc.requires_grad_(True)
# ... train head ...

# Then unfreeze and fine-tune the last blocks with a low LR
for param in backbone.parameters():
    param.requires_grad = True
# optimizer = AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-5)
```

**Rule of thumb:** more data → more of the network can be fine-tuned. Small dataset → freeze most layers.

## 5. Common Failure Modes and Fixes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Loss stays ~constant | Wrong loss/activation, LR too low | Check final layer + `CE + logits`; try `lr=1e-3` AdamW |
| Loss explodes to NaN | LR too high, bad init, no grad clip | Lower LR, `clip_grad_norm_`, check for `inf` |
| High train acc, low val acc | Overfitting | Add dropout/weight decay, augment data, reduce capacity |
| High val, low train | Underfitting / too strong regularization | Reduce dropout, increase capacity, more epochs |
| Train loss ~0, val random | Data leakage or label bug | Verify splits; shuffle by group not row |
| Slow to converge | Feature scale issues | Normalize inputs, use `nn.BatchNorm`, larger LR warmup |

### Gradient checking

If a model won't learn, verify gradients flow: after one backward pass,
`assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters() if p.requires_grad)`.

## 6. Evaluation

- **Classification:** accuracy, precision/recall/F1 (macro), confusion matrix. Never report only accuracy on imbalanced data.
- **Regression:** MAE, RMSE, R².
- **Calibration:** check if probabilities are calibrated (`torchmetrics.CalibrationError`).
- **Confidence intervals:** bootstrap or repeated eval with different seeds.

Always evaluate on a **held-out test set** (not validation) as the final step, and save the exact test predictions + model version for audit.

## 7. GPU Best Practices

- Use `pin_memory=True` and `persistent_workers=True` in DataLoader.
- Prefer `torch.inference_mode()` (not `no_grad`) for evaluation.
- Batch size: pick largest that fits memory, then scale LR proportionally.
- Mixed precision (`torch.autocast` + `GradScaler`) gives ~2× speedup with negligible accuracy loss.
- Check GPU memory with `nvidia-smi` before blaming the code.

## Examples

### Example 1: Binary classification (custom Dataset + simple MLP)

```python
class MLP(nn.Module):
    def __init__(self, in_dim, hidden=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(hidden, 1),
        )
    def forward(self, x):
        return self.net(x).squeeze(1)  # logits for BCEWithLogitsLoss
```

### Example 2: Early stopping

```python
best_val = 0.0
patience = 0
for epoch in range(1, max_epochs + 1):
    train_loss = train_one_epoch(...)
    val_loss, val_acc = evaluate(...)
    if val_acc > best_val:
        best_val = val_acc
        torch.save(model.state_dict(), "best.pt")
        patience = 0
    else:
        patience += 1
        if patience >= 5:
            print("early stop")
            break
```

## Notes

- Never train from scratch when a pretrained backbone works — fine-tune.
- Keep experiments versioned: config (seed, LR, arch) + data hash + metrics in one record.
- Use a framework like PyTorch Lightning or Hugging Face Trainer for long-lived projects; raw loops are fine for experiments.
- Always record the device, torch version, and dataset split used, or the run is not reproducible.

## References

- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [torchvision models & weights](https://pytorch.org/vision/stable/models.html)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [PyTorch Lightning](https://lightning.ai/docs/pytorch/stable/)
