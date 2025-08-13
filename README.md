# -Face_dectection_Pushup_Counter

This Python script uses computer vision libraries like OpenCV and Mediapipe to count push-ups and record the data in a CSV file. It can also detect faces using a Haar Cascade classifier.

## Features

- Counts push-ups in real-time using pose detection.
- Detects and highlights faces in the video feed.
- Records push-up counts and timestamps in a CSV file.

## Usage

Press 'q' to exit the program and it will automatically save the push-up count to a CSV file. The push-up count and timestamps will be saved in a CSV file named with the current date.

## Dependencies

Make sure you have the following Python libraries installed:

- OpenCV
- Mediapipe
- CSV

You can install them using pip:

```bash
pip install opencv-python mediapipe 
