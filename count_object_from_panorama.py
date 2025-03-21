# -*- coding: utf-8 -*-
"""count_object_from_panorama.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AsDiYHfNvmysXMJUxrYCckzWn0uM_f10
"""

!pip install ultralytics

#Import packages
import cv2
import numpy as np
import imutils
from google.colab.patches import cv2_imshow

def extract_frames(video_path, skip_frames):
    """Extracts frames from a video at regular intervals."""
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video
        if frame_count % skip_frames == 0:
            frames.append(frame)
        frame_count += 1

    cap.release()
    return frames

def stitch_images(images):
    """Stitches images to create a panorama using feature matching."""
    stitcher = cv2.Stitcher_create()
    (status, panorama) = stitcher.stitch(images)

    if status != cv2.Stitcher_OK:
        print("Error: Image stitching failed!")
        return None

    return panorama

def create_panorama(video_path, output_path,skip_frames):
    """Extracts frames, stitches them, and saves the panorama."""
    print("Extracting frames from video...")
    frames = extract_frames(video_path,skip_frames)

    if len(frames) < 2:
        print("Not enough frames for stitching!")
        return

    print("Stitching images to create a panorama...")
    panorama = stitch_images(frames)

    if panorama is not None:
        cv2.imwrite(output_path, panorama)
        print(f"Panorama saved as {output_path}")
        cv2_imshow(imutils.resize(panorama, width=1000))

    else:
        print("Failed to generate panorama.")
    return panorama

def detect_objects(image,output_path_OD):
    # Load the YOLOv8 model
    model = YOLO("yolov8s.pt")  # Use a pretrained YOLO model

    results = model(image) # get objects from yolo
    object_count = 0
    for box in results[0].boxes.xyxy:  # Bounding boxes
        object_count = object_count + 1
        x1, y1, x2, y2 = map(int, box[:4])
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"Object {object_count}", (x1, y1 - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imwrite(output_path_OD, image)
    cv2_imshow(image) # show the image
    return object_count

# Example usage
if __name__ == "__main__":
    video_file = "/inputs/input_object_count_video.mp4"  # Change to your video file
    output_file ="/outputs/output_panorama_object_count.jpg"              # change to your output file to save the panorama
    skip_frames =  50
    image = create_panorama(video_file,output_file,skip_frames)
    output_file_OD ="/outputs/output_object_count.jpg"              # change to your output file to save the panorama
    object_count = detect_objects(image,output_file_OD)
    print("Number of objects are :", object_count )