# [📘 English version available here](README.en.md)

![Task: Vehicle Entry-Exit Counting](https://img.shields.io/badge/Task-Vehicle%20Counting-blue?style=flat)
![Model: YOLOv11 + ByteTrack](https://img.shields.io/badge/Model-YOLOv11%20%2B%20ByteTrack-purple?style=flat)
![Framework: OpenCV](https://img.shields.io/badge/Framework-OpenCV-red?style=flat)
![Real-time Ready](https://img.shields.io/badge/Real--time-Yes-green?style=flat)


---

# ระบบนับจำนวนรถเข้า-ออกด้วย YOLOv11 + ByteTrack  
> ระบบตรวจจับและติดตามยานพาหนะแบบเรียลไทม์ โดยใช้ YOLOv11 สำหรับการตรวจจับ และ ByteTrack สำหรับการติดตามวัตถุ พร้อมวิเคราะห์การเคลื่อนผ่านเส้น IN/OUT ภายในพื้นที่ที่กำหนด เหมาะสำหรับลานจอดรถ ระบบ IoT และอุปกรณ์ Edge

ระบบนี้ใช้เทคนิค Object Detection และ Object Tracking เพื่อนับจำนวนวัตถุที่เคลื่อนผ่านเส้นทางเข้า/ออกภายใน Polygon ROI จากวิดีโอหรือกล้องแบบเรียลไทม์ โดยสามารถติดตามวัตถุด้วย Track ID อย่างแม่นยำแม้ในกรณีที่มีการบดบัง (Occlusion) และรองรับการแสดงผล overlay เช่น IN / OUT / FPS บนวิดีโอที่ประมวลผลแล้ว

---

## โครงสร้างโปรเจกต์

```
.
├── count_vehicle.py        # สคริปต์หลักสำหรับนับจำนวนรถ
├── get_frame.py            # สคริปต์ดึงเฟรมจากวิดีโอเพื่อใช้วาด Polygon บน Roboflow PolygonZone
├── videos/                 # วิดีโอต้นฉบับ
├── weights/                # ไฟล์โมเดล YOLOv11 (.pt) 
├── outputs/                # ไฟล์วิดีโอหรือภาพผลลัพธ์
├── README.md               # เอกสารประกอบนี้
├── requirements.txt        # รายการไลบรารีที่จำเป็น
```

---

## 🎯 จุดเด่นของระบบ

- ตรวจจับยานพาหนะ (รถยนต์ รถกระบะ ฯลฯ) ด้วย YOLOv11
- ติดตามวัตถุด้วย ByteTrack โดยใช้ Track ID เดิมแม้จะมี Occlusion
- ครอบพื้นที่สนใจด้วย Polygon และตรวจจับเฉพาะในพื้นที่นั้น
- นับเฉพาะวัตถุที่เคลื่อน “ผ่านเส้น” IN/OUT
- แสดง overlay แบบ real-time ได้แก่ IN / OUT / FPS

---

## ตัวอย่างการทำงานของระบบ

ภาพ GIF ด้านล่างแสดงให้เห็นการทำงานของระบบนับรถเข้า-ออกแบบเรียลไทม์ โดยตรวจจับยานพาหนะที่เคลื่อนผ่านเส้น IN/OUT ภายในพื้นที่ Polygon ROI

<p align="center">
  <img src="output.gif" alt="Vehicle Counting Demo" style="width: 100%;" />
</p>

▶️ **ชมวิดีโอสาธิตแบบเต็ม** ได้ที่ [YouTube](https://www.youtube.com/watch?v=17F-Efu0Z5M)

---

## วิธีใช้งาน (How to use)

1. วางวิดีโอไว้ในโฟลเดอร์ `videos/`
2. วางโมเดล YOLOv11 (`yolo11x.pt`) ไว้ในโฟลเดอร์ `weights/` หากไม่มีโมเดลจะถูกโหลดอัตโนมัติเมื่อรันสคริปต์
3. แก้ไขบรรทัดใน `count_vehicle.py` ให้ตรงกับชื่อไฟล์ของคุณ:

```python
video_name = "parking.mp4"
model_name = "yolo11x.pt"
```

> 🔗 Download: [parking.mp4](https://drive.google.com/file/d/1SHUg4CTJOr1VHGALDlz6n41lb7jXkLBc/view?usp=sharing)

4. รันโปรแกรม:

```bash
python count_vehicle.py
```

5. กด `q` เพื่อหยุดการทำงาน วิดีโอที่ผ่านการประมวลผลจะถูกบันทึกไว้ในโฟลเดอร์ `outputs/`

---

## Polygon ROI and IN/OUT Line

สามารถใช้ `get_frame.py` เพื่อดึงเฟรมจากวิดีโอเพื่อไปวาด ROI บนเว็บไซต์ [https://polygonzone.roboflow.com](https://polygonzone.roboflow.com)

```bash
python get_frame.py  # ดึงเฟรมที่ 100 (สามารถเปลี่ยนเลขในสคริปต์ได้)
```

ผลลัพธ์จะถูกเก็บไว้ใน `outputs/frame_100.jpg`

---

## Requirements

```
numpy
torch
opencv-python
ultralytics
supervision
```

ติดตั้งไลบรารี:

```bash
pip install -r requirements.txt
```

---

## 💡 ตัวอย่างการนำไปใช้งาน Real-World Application

- ตรวจนับรถเข้า-ออกในลานจอดรถ
- วิเคราะห์ความแออัดของถนนในเขตเมือง
- ใช้กับกล้องบนอุปกรณ์ IoT หรือ Edge Device เพื่อประมวลผลแบบ local

---

## Attribution

- Open source computer vision library [OpenCV](https://opencv.org/)
- YOLOv11 [Ultralytics](https://github.com/ultralytics/ultralytics/)
- พัฒนาโดย [MorseTech Lab](https://www.morsetechlab.com/)

---

## 🛡️ License

Project นี้เผยแพร่ภายใต้ [GNU Affero General Public License v3.0 (AGPLv3)](LICENSE) เพื่อให้สอดคล้องกับเงื่อนไขการใช้งานของไลบรารีที่เกี่ยวข้อง

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
