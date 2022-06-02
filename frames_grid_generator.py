import numpy
import cv2
import sys
import datetime

background = numpy.full((1080, 1920, 3), (0, 216, 255), numpy.uint8)
background_w, background_h = background.shape[1], background.shape[0]

cap = cv2.VideoCapture(sys.argv[1])
count = 0

rows = 4
columns = 4
resize = 15 # (resize * rows) % (rows + 1) == 0
total_frames = rows * columns

x_offset = (resize * rows) // (rows + 1)
y_offset = (resize * columns) // (columns + 1)

frame_w = background_w // rows - resize
frame_h = background_h // columns - resize

FPS = int(cap.get(cv2.CAP_PROP_FPS))
total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
step = total_frame_count // (total_frames + 2)

frames = {}
index = 0
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        current_time = str(datetime.timedelta(seconds=(count // FPS))) # divide current frames count by FPS
        frame = cv2.resize(frame, (frame_w, frame_h), interpolation=cv2.INTER_LINEAR)
        frame = cv2.putText(frame, current_time, (0, frame_h - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA, False)
        frames[index] = frame
        count += step
        cap.set(1, count)
        index += 1
        if count > (total_frame_count - step):
            cap.release()
            break
    else:
        cap.release()
        break

x, y = x_offset, y_offset
for i in range(0, total_frames):
    background[y:y + frame_h, x:x + frame_w] = frames[i + 1]
    x += frame_w + x_offset
    if x > background_w - frame_w:
        x = x_offset
        y += frame_h + y_offset

cv2.imwrite("framesgrid.jpg", background)
