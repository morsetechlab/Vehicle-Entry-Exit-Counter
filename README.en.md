# [📘 เวอร์ชั่นภาษาไทยที่นี่](README.md)

![Task: Vehicle Counting](https://img.shields.io/badge/Task-Vehicle%20Counting-blue?style=flat&logo=car&logoColor=white)
![Model: YOLOv11 + ByteTrack](https://img.shields.io/badge/Model-YOLOv11%20%2B%20ByteTrack-purple?style=flat&logo=yolov5&logoColor=white)
![Framework: OpenCV](https://img.shields.io/badge/Framework-OpenCV-red?style=flat&logo=opencv&logoColor=white)
![Real-time Ready](https://img.shields.io/badge/Real--time-Yes-green?style=flat&logo=clockify&logoColor=white)

---

# Real-time Vehicle Entry-Exit Counting using YOLOv11 + ByteTrack  
> A real-time vehicle detection and tracking system using YOLOv11 for object detection and ByteTrack for robust object tracking. Designed to count vehicles crossing defined IN/OUT lines within a specified polygonal ROI. Ideal for parking lots, IoT systems, and edge devices.

This system leverages object detection and tracking techniques to count vehicles passing through designated IN/OUT lines inside a polygonal region of interest (ROI), using either live camera feeds or video files. It maintains accurate Track IDs even under partial occlusion and supports real-time overlay of key metrics such as IN count, OUT count, and FPS on the output video.

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

## System in Action

The GIF below demonstrates how the system detects and counts vehicles as they move through the defined IN/OUT lines within a polygonal ROI.

<p align="center">
  <img src="output.gif" alt="Vehicle Counting Demo" style="width: 100%;" />
</p>

▶️ **Watch Full Demo** on [YouTube](https://www.youtube.com/watch?v=17F-Efu0Z5M)

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

<!--
tags: Vehicle Counting, YOLOv11, ByteTrack, Object Detection, Object Tracking, Entry Exit Line, Parking Lot Monitoring, Computer Vision, OpenCV, Ultralytics, Real-time Analytics, Python, Edge Device
-->

<!-- Open Graph / Twitter Meta -->
<!--
<meta property="og:title" content="YOLOv11 Vehicle Counter: Real-time Entry/Exit Counting with ByteTrack" />
<meta property="og:description" content="Real-time vehicle detection and tracking system using YOLOv11 and ByteTrack. Counts vehicles crossing custom IN/OUT lines inside polygonal ROI." />
<meta property="og:image" content="https://raw.githubusercontent.com/morsetechlab/yolov11-vehicle-counter/main/output.gif" />
<meta property="og:url" content="https://github.com/morsetechlab/yolov11-vehicle-counter" />
<meta property="og:type" content="website" />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="YOLOv11 Vehicle Counter: Entry/Exit Tracking with ByteTrack" />
<meta name="twitter:description" content="Detect and count vehicles in real-time using YOLOv11 and ByteTrack. Ideal for parking lots, IoT devices, and traffic analytics." />
<meta name="twitter:image" content="https://raw.githubusercontent.com/morsetechlab/yolov11-vehicle-counter/main/output.gif" />
-->
