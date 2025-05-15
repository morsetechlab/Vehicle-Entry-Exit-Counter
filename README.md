# ระบบนับจำนวนรถเข้า-ออกด้วย YOLOv11 + ByteTrack

ระบบนับรถเข้า-ออกแบบเรียลไทม์ ด้วยเทคนิค Object Detection และ Object Tracking โดยใช้โมเดล **YOLOv11** สำหรับการตรวจจับ และ **ByteTrack** สำหรับการติดตามวัตถุด้วย track ID เพื่อวิเคราะห์การเคลื่อนผ่านเส้นเข้า/ออก (IN/OUT) ภายในบริเวณที่สนใจ (Polygon ROI) สามารถใช้งานได้กับวัตถุที่มีขนาดเล็กเนื่องจากจำกัดพื้นที่ตรวจจับ

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

## วิธีใช้งาน (How to use)

1. วางวิดีโอไว้ในโฟลเดอร์ `videos/`
2. วางโมเดล YOLOv11 (`yolo11x.pt`) ไว้ในโฟลเดอร์ `weights/` หากไม่มีโมเดลจะถูกโหลดอัตโนมัติเมื่อรันสคริปต์
3. แก้ไขบรรทัดใน `count_vehicle.py` ให้ตรงกับชื่อไฟล์ของคุณ:

```python
video_name = "parking.mp4"
model_name = "yolo11x.pt"
```

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

- Open source computer vision library [OpenCV](https://opencv.org)
- YOLOv11 [Ultralytics](https://github.com/ultralytics/ultralytics)
- พัฒนาโดย **MorseTech Lab**

---

## 🛡️ License

Project นี้เผยแพร่ภายใต้ [GNU Affero General Public License v3.0 (AGPLv3)](LICENSE) เพื่อให้สอดคล้องกับเงื่อนไขการใช้งานของไลบรารีที่เกี่ยวข้อง
