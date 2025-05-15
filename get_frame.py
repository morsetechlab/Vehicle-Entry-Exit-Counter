# get_frame.py

import cv2
import os

# Set input video path and output image path
video_path = os.path.join("videos", "parking.mp4")
output_image_path = os.path.join("outputs", "frame_100.jpg")  # Name of output image

frame_number = 100  # You can change this to the frame you want to extract

# Open the video file
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise FileNotFoundError(f"Cannot open video: {video_path}")

# Check if the frame number is within the total number of frames
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
if frame_number >= total_frames:
    raise ValueError(f"Frame {frame_number} exceeds total frames ({total_frames})")

# Set the position to the desired frame
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ret, frame = cap.read()
cap.release()

if not ret:
    raise RuntimeError(f"Cannot read frame {frame_number} from video.")

# Create outputs folder if it doesn't exist
os.makedirs("outputs", exist_ok=True)

# Save the extracted frame as an image
cv2.imwrite(output_image_path, frame)
print(f"✅ Saved frame {frame_number} to: {output_image_path}")
