# [📘 เวอร์ชั่นภาษาไทยที่นี่](README.md)

---

# Vehicle Entry/Exit Counting System with YOLOv11 + ByteTrack

A real-time vehicle counting system using Object Detection and Object Tracking techniques. This project leverages **YOLOv11** for vehicle detection and **ByteTrack** for robust multi-object tracking via track ID. The system detects whether vehicles pass through predefined IN/OUT lines inside a specific area defined by a polygon ROI. It is also optimized for scenarios with small object sizes and limited regions of interest.

---

## Project Structure

```
.
├── count_vehicle.py        # Main script for vehicle counting
├── get_frame.py            # Extract a video frame to define ROI on Roboflow PolygonZone
├── videos/                 # Input videos
├── weights/                # YOLOv11 model files (.pt)
├── outputs/                # Processed video and image outputs
├── README.md               # This documentation
├── requirements.txt        # Python dependencies
```

---

## 🎯 Key Features

- Detects vehicles (cars, pickups, etc.) using YOLOv11
- Tracks moving vehicles using ByteTrack with consistent track IDs even with occlusion
- Focuses detection within a user-defined polygon region (ROI)
- Counts only vehicles that actually **pass through** the IN/OUT lines
- Displays real-time overlay with IN / OUT / FPS info on screen

---

## How to Use

1. Place your video in the `videos/` folder
2. Place your YOLOv11 model (`yolo11x.pt`) in the `weights/` folder  
   If not found, it will be automatically downloaded at runtime
3. Edit these lines in `count_vehicle.py` to match your file names:

```python
video_name = "parking.mp4"
model_name = "yolo11x.pt"
```

> 🔗 Download demo video: [parking.mp4](https://drive.google.com/file/d/1SHUg4CTJOr1VHGALDlz6n41lb7jXkLBc/view?usp=sharing)

4. Run the script:

```bash
python count_vehicle.py
```

5. Press `q` to stop. The processed video will be saved to the `outputs/` folder.

---

## Polygon ROI and IN/OUT Line Definition

Use `get_frame.py` to extract a video frame and define the polygon ROI using the tool at [https://polygonzone.roboflow.com](https://polygonzone.roboflow.com)

```bash
python get_frame.py  # Extracts frame 100 (changeable inside the script)
```

The saved image will be located at `outputs/frame_100.jpg`

---

## Requirements

```
numpy
torch
opencv-python
ultralytics
supervision
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 💡 Real-World Applications

- Count vehicle entries/exits in parking areas
- Analyze traffic flow and congestion in urban environments
- Deploy on edge devices or IoT cameras for on-site processing

---

## Attribution

- Open source computer vision library [OpenCV](https://opencv.org)
- Real-time object detection framework [YOLOv11](https://github.com/ultralytics/ultralytics)
- Developed by [MorseTech Lab](https://www.morsetechlab.com/)

---

## 🛡️ License

This project is licensed under the [GNU Affero General Public License v3.0 (AGPLv3)](https://www.gnu.org/licenses/agpl-3.0.html)  
to comply with all related open-source libraries and promote responsible use.
