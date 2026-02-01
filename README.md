# Face Recognition with ArcFace ONNX, 5-Point Alignment, and Face Locking

## Overview

This project implements a **modular, CPU-only, explainable real-time face recognition system** using the **ArcFace ONNX model** with **5-point facial landmark alignment**, extended with a **Face Locking mechanism** and **action detection**.

The system is designed to be transparent, educational, and practical.  
Each stage of the pipeline is implemented as an independent module so that detection, alignment, embedding, recognition, locking, tracking, and action analysis can be understood and tested separately.

This project extends the original ArcFace ONNX recognition pipeline by introducing identity persistence (face locking), stable tracking, and action history logging.

## Key Features

- Multi-face detection using Haar Cascade
- 5-point facial landmark extraction using MediaPipe FaceMesh
- Face alignment to 112×112 resolution
- ArcFace ONNX embedding extraction (CPU-only)
- Cosine similarity-based identity recognition
- Manual identity selection for face locking
- Face locking and stable identity tracking
- Action detection (face movement)
- Action history logging with timestamps
- Modular and extensible architecture
- Cross-platform support (Windows, Linux, macOS)

---

## Project Structure


```
face-recognition-5pt/
├── data/
│   ├── db/
│   │   ├── face_db.json        # metadata (names, timestamps, etc.)
│   │   └── face_db.npz         # L2-normalized embeddings
│   └── enroll/
│       ├── <Identity_Name>/
│       │   └── *.jpg           # aligned 112×112 enrollment images
├── models/
│   └── embedder_arcface.onnx   # ArcFace ONNX model
├── src/
│   ├── align.py                # Face alignment module
│   ├── camera.py               # Webcam feed handler
│   ├── detect.py               # Face detection
│   ├── embed.py                # ArcFace embedding extraction
│   ├── enroll.py               # Enrollment pipeline
│   ├── evaluate.py             # Threshold evaluation
│   ├── haar_5pt.py             # Haar cascade + 5-point detector
│   ├── landmarks.py            # Facial landmark detection
│   └── recognize.py            # Real-time recognition
│   ├── face_lock/
│   │ ├── lock_manager.py # Face locking logic
│   │ ├── action_detector.py # Action detection logic
│   │ ├── history_logger.py # Action history logging
├── init_project.py             # Project structure initialization
├── README.md
└── book/                       # (optional) book-related files
```

## System Pipelines

### 1. Enrollment Pipeline
1. Face Detection  
2. 5-Point Landmark Detection  
3. Face Alignment (Warping to 112×112)  
4. ArcFace Embedding Extraction  
5. Store L2-normalized embedding in database
6. Store embedding in database

### 2. Recognition Pipeline
1. Face Detection  
2. 5-Point Landmark Detection  
3. Face Alignment  
4. ArcFace Embedding Extraction  
5. Cosing similarity matching
6. Identity recognition

### 3. Extended Pipeline with Face Locking

Recognition Result  
1. Manual Identity Selection  
2. Face Lock Activation  
3.  Stable Identity Tracking  
4.  Action Detection  
5.  Action History Logging  

## Face Locking Concept

Face locking is an extension of face recognition.  
Instead of re-recognizing identities in every frame, the system locks onto a selected identity and tracks it continuously.

### Face Locking Workflow

Recognition  
→ If recognized identity == target identity  
→ Lock face  
→ Track same face across frames  
→ Ignore other faces  
→ Detect actions  
→ Log actions  
→ Unlock if face disappears for a sustained period  

---

## Face Locking Logic

### Manual Identity Selection

A target identity is manually defined in the system:

```python
lock_manager = FaceLockManager(target_identity="Promesse")
```

## Setup Instructions

### Requirements
- Python 3.9+
- Webcam (for recognition modules)
- Supported OS: macOS, Linux, Windows

### Step 1: Create & Activate Virtual Environment

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### Step 2: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install opencv-python numpy onnxruntime scipy tqdm mediapipe
```

### Step 3: Initialize Project Structure

```bash
python init_project.py
```

This script creates all necessary directories and placeholder files. Safe to re-run—never overwrites existing files.

### Step 4: Grant Camera Permissions

**macOS:** 
System Settings → Privacy & Security → Camera → Allow Terminal / VS Code

**Windows / Linux:** 
Ensure no other application is using your webcam

## Quick Validation

### Camera Check
```bash
python -m src.camera
```

Expected output:
- Live video window opens
- FPS counter displayed
- Smooth motion
- Press `q` to exit

If this fails, verify camera permissions and availability before proceeding.

## Module Testing Commands

Test individual components to validate setup:

```bash
# Camera feed and FPS benchmark
python -m src.camera

# Face detection with bounding boxes
python -m src.detect

# 5-point landmarks visualization
python -m src.landmarks

# Face alignment to 112×112
python -m src.align

# ArcFace embedding extraction
python -m src.embed

# Enroll identities into database
python -m src.enroll

# Evaluate and tune similarity threshold
python -m src.evaluate

# Live real-time recognition with webcam
python -m src.recognize
```

## Usage Workflow

1. **Enroll identities:** `python -m src.enroll`
   - Follow prompts to capture and register new faces
   - Embeddings saved to database

2. **Recognize faces:** `python -m src.recognize`
   - Real-time webcam feed with live recognition
   - Shows identity matches with confidence scores

3. **Evaluate threshold:** `python -m src.evaluate`
   - Fine-tune similarity threshold for your use case

## Troubleshooting

### Camera not detected
- Check permissions 
- Verify no other application is using the camera
- Try changing camera index in `src/camera.py`

### Poor recognition accuracy
- Ensure good lighting during enrollment
- Enroll multiple angles/poses per identity
- Adjust threshold in `src/evaluate.py`
- Verify faces are frontal (5-point alignment works best with minimal head tilt)

### Performance issues
- Use ONNX Runtime instead of other inference engines
- Reduce frame resolution for faster processing
- Limit number of identities in database