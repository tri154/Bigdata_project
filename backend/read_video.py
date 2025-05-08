import cv2
global frame_number
frame_number = 0
def read_frame():
    video_path = 'test_video/object_tracking_output_opencv.mp4'

    cap = cv2.VideoCapture(video_path)
    global frame_number
    # Set the frame position
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    frame_number += 1

    # Read the frame
    ret, frame = cap.read()

    if ret:
        return frame
    else:
        print("Failed to read the frame.")
    cap.release()
    return None


if __name__ == '__main__':
    print(read_frame())