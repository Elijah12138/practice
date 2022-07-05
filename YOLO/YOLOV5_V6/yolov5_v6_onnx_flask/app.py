from operator import ne
from flask import Flask, render_template, Response
from v5_dnn import *
import time
from cv2 import getTickCount, getTickFrequency

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
    def get_frame(self):
        success, image = self.video.read()
        return image

app = Flask(__name__)

@app.route('/')  # 主页
def index():
    return render_template('index.html')


def v5_dnn(camera):
    modelpath = 'yolov5n.onnx'
    confThreshold = 0.3
    nmsThreshold = 0.5
    objThreshold = 0.3
    yolonet = yolov5(modelpath, confThreshold=confThreshold, nmsThreshold=nmsThreshold,
                     objThreshold=objThreshold)
    while True:
        start = time.clock()
        frame = camera.get_frame()
        yolonet.detect(frame)
        end = time.clock()
        fps = 1. / (end - start)
        cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(v5_dnn(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
