# Import necessary libraries
import os
import cv2
import numpy as np
import time
from tqdm import tqdm
from ultralytics import YOLO
import torch
import supervision as sv

# Set device to GPU (MPS for Mac) or fallback to CPU
device = "mps" if torch.backends.mps.is_available() else "cpu"

# Set paths for input video, YOLO model, and output video
video_name = "parking.mp4"
video_path = os.path.join(".", "videos", video_name)
model_name = "yolo11x.pt"
model_path = os.path.join(".", "weights", model_name)
output_name = "parking_count_output.mp4"
output_path = os.path.join(".", "outputs", output_name)

# Load YOLO model and prepare for inference
model = YOLO(model_path)
model.to(device)
model.fuse()

# Map class name to class index
name_to_id = {v: k for k, v in model.model.names.items()}

# Get video metadata
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cap.release()

# Create VideoWriter for output
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Initialize ByteTrack tracker
tracker = sv.ByteTrack(
    track_activation_threshold=0.5,
    lost_track_buffer=120,
    minimum_matching_threshold=0.80,
    frame_rate=int(fps),
    minimum_consecutive_frames=3
)

# Define Region of Interest (ROI) polygon
polygon = np.array([[874, 676], [1151, 501], [1416, 536], [1164, 727]])
x_min, y_min = polygon.min(axis=0)
x_max, y_max = polygon.max(axis=0)
padding = 50
crop_x1, crop_y1 = max(0, x_min - padding), max(0, y_min - padding)
crop_x2, crop_y2 = min(width, x_max + padding), min(height, y_max + padding)

# Adjust polygon coordinates relative to crop area
polygon_cropped = polygon.copy()
polygon_cropped[:, 0] -= crop_x1
polygon_cropped[:, 1] -= crop_y1

# Create a mask for the ROI polygon
crop_mask = np.zeros((crop_y2 - crop_y1, crop_x2 - crop_x1), dtype=np.uint8)
cv2.fillPoly(crop_mask, [polygon_cropped], 255)

# Define IN and OUT lines
in_lines = [
    ((1069, 548), (1314, 580)),
    ((1314, 583), (1234, 638)),
    ((1234, 638), (1084, 618)),
]
out_line = ((970, 653), (1027, 622))

# Check if line segments intersect (used for direction detection)
def direction(p1, p2, a, b):
    def ccw(x, y, z):
        return (z[1]-x[1]) * (y[0]-x[0]) > (y[1]-x[1]) * (z[0]-x[0])
    return ccw(p1, a, b) != ccw(p2, a, b) and ccw(p1, p2, a) != ccw(p1, p2, b)

# Initialize tracking history and counters
track_history = dict()
counted_in_ids = set()
counted_out_ids = set()

# Open video for processing
cap = cv2.VideoCapture(video_path)

with tqdm(total=total_frames, desc="Processing") as pbar:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Crop and apply ROI mask
        cropped = frame[crop_y1:crop_y2, crop_x1:crop_x2]
        masked = cv2.bitwise_and(cropped, cropped, mask=crop_mask)

        # Perform object detection
        results = model(masked, device=device)[0]
        if results.boxes is None or len(results.boxes.cls) == 0:
            video_writer.write(frame)
            pbar.update(1)
            continue

        # Filter for cars and trucks
        cls = results.boxes.cls.cpu().numpy()
        xyxy = results.boxes.xyxy.cpu().numpy()
        conf = results.boxes.conf.cpu().numpy()
        mask = np.isin(cls, [name_to_id["car"], name_to_id["truck"]])
        xyxy = xyxy[mask]
        conf = conf[mask]

        if len(xyxy) == 0:
            video_writer.write(frame)
            pbar.update(1)
            continue

        # Map coordinates back to full frame
        xyxy[:, [0, 2]] += crop_x1
        xyxy[:, [1, 3]] += crop_y1

        # Filter detections within ROI polygon
        centers = np.array([[(x1 + x2) / 2, (y1 + y2) / 2] for x1, y1, x2, y2 in xyxy])
        inside_mask = np.array([
            cv2.pointPolygonTest(polygon.astype(np.float32), tuple(c), False) >= 0 for c in centers
        ])
        xyxy = xyxy[inside_mask]
        conf = conf[inside_mask]

        if len(xyxy) == 0:
            video_writer.write(frame)
            pbar.update(1)
            continue

        # Create detections and update tracker
        det = sv.Detections(xyxy=xyxy, confidence=conf)
        det = tracker.update_with_detections(det)

        for i in range(len(det)):
            x1, y1, x2, y2 = det.xyxy[i]
            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
            track_id = det.tracker_id[i]
            if track_id is None:
                continue

            # Update movement history
            if track_id not in track_history:
                track_history[track_id] = []
            track_history[track_id].append((cx, cy))
            if len(track_history[track_id]) > 2:
                track_history[track_id].pop(0)

            # Check for IN crossing
            if track_id not in counted_in_ids and len(track_history[track_id]) == 2:
                p1, p2 = track_history[track_id]
                for line_start, line_end in in_lines:
                    if direction(p1, p2, line_start, line_end):
                        counted_in_ids.add(track_id)
                        break

            # Check for OUT crossing
            if track_id not in counted_out_ids and len(track_history[track_id]) == 2:
                p1, p2 = track_history[track_id]
                if direction(p1, p2, out_line[0], out_line[1]):
                    counted_out_ids.add(track_id)

            # Draw tracking circle and ID label
            cv2.circle(frame, (cx, cy), 5, (255, 0, 255), -1)
            cv2.putText(frame, f"id: {track_id}", (cx, cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        # Draw IN/OUT lines and ROI polygon
        for line in in_lines:
            cv2.line(frame, line[0], line[1], (0, 255, 0), 3)
        cv2.line(frame, out_line[0], out_line[1], (0, 0, 255), 3)
        cv2.polylines(frame, [polygon], True, (50, 180, 200), 3)

        # Calculate and display FPS, IN, OUT overlay
        current_time = time.time()
        if 'prev_time' not in locals():
            prev_time = current_time
            fps_val = 0.0
        else:
            fps_val = 1.0 / (current_time - prev_time)
            prev_time = current_time

        info_lines = [
            f"IN: {len(counted_in_ids)}",
            f"OUT: {len(counted_out_ids)}",
            f"FPS: {fps_val:.1f}"
        ]

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 3
        text_color = (0, 255, 0)
        bg_color = (0, 0, 0)

        line_spacing = 20
        text_sizes = []
        total_height = 0
        max_width = 0
        for line in info_lines:
            (tw, th), _ = cv2.getTextSize(line, font, font_scale, thickness)
            text_sizes.append(((tw, th), line))
            total_height += th + line_spacing
            max_width = max(max_width, tw)

        x_pad, y_pad = 20, 120
        x0 = frame.shape[1] - max_width - 2 * x_pad
        y0 = y_pad
        x1 = frame.shape[1] - x_pad
        y1 = y0 + total_height
        cv2.rectangle(frame, (x0, y0), (x1, y1), bg_color, thickness=-1)

        y_text = y0 + 40
        for ((tw, th), text) in text_sizes:
            cv2.putText(
                frame, text,
                (x1 - tw - 10, y_text),
                font, font_scale, text_color, thickness, cv2.LINE_AA
            )
            y_text += th + line_spacing

        # Display and save frame
        cv2.imshow("Vehicle IN/OUT Count", frame)
        video_writer.write(frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        pbar.update(1)

# Release resources
cap.release()
video_writer.release()
cv2.destroyAllWindows()

print("-" * 40)
print("Processing Completed")
print(f"IN count: {len(counted_in_ids)}")
print(f"OUT count: {len(counted_out_ids)}")
print(f"Output saved: {output_path}")
print("-" * 40)