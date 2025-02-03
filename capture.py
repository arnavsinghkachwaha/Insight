import cv2
import os
import numpy as np

def cropFrame(frame):
    zoom_factor = 1.5 
    top_offset = 200 
    h, w = frame.shape[:2]
    target_h = int(w * 3 / 4)
    zoomed_h = int(target_h / zoom_factor)
    zoomed_w = int(w / zoom_factor)
    start_y = top_offset
    end_y = start_y + zoomed_h
    if end_y > h:
        end_y = h
    cropped_frame = frame[start_y:end_y, (w - zoomed_w) // 2 : (w + zoomed_w) // 2]
    resized_frame = cv2.resize(np.array(cropped_frame), (640, 480))
    return (resized_frame)

# Directory where the cropped frames are saved
frames_dir = r'/Users/arnavkachwaha/Desktop/INSIGHT/Raw/frames'
os.makedirs(frames_dir, exist_ok=True)

# Base path for videos
video_base_path = r'/Users/arnavkachwaha/Desktop/INSIGHT/Raw/videos'
# Process videos
for i in range(541,564):
    video_name = f"vid{i}.mov"
    video_path = os.path.join(video_base_path, video_name)

    # Open the video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video {video_path}")
        continue

    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps / 2)  # Extract 1 frames per second

    count = 0
    frame_save_count = 1  # Start counting from 1 for each video
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # resized_frame = cropFrame(frame)
            if count % interval == 0:
                frame_filename = os.path.join(frames_dir, f"vid{i}.frame{frame_save_count}.png")
                cv2.imwrite(frame_filename, frame)
                print(f"Saved {frame_filename}")
                frame_save_count += 1
            count += 1
        else:
            print("End of video or error reading frame.")
            break

    cap.release()
    print(f"Total frames extracted from {video_name}: {frame_save_count - 1}")


