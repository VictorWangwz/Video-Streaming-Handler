from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from  django.views.decorators import gzip
from .models import Stream
from django.http.response import StreamingHttpResponse
from django.http import HttpResponseServerError
import cv2
import threading
import pdb
from django.views.decorators.csrf import csrf_exempt
import subprocess

@require_POST
@csrf_exempt
def on_publish(request):
    # nginx-rtmp makes the stream name available in the POST body via `name`
    stream_key = request.POST['name']
    return HttpResponse("OK")

@require_POST
@csrf_exempt
def on_play(request):
    # nginx-rtmp makes the stream name available in the POST body via `name`
    pdb.set_trace()
    stream_key = request.POST['name']
    return HttpResponse("OK")


@require_POST
@csrf_exempt
def on_publish_done(request):
    # When a stream stops nginx-rtmp will still dispatch callbacks
    # using the original stream key, not the redirected stream name.
    stream_key = request.POST['name']

    return HttpResponse("OK")



class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()




def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    camera_generator = gen(VideoCamera())
    try:
        return StreamingHttpResponse(camera_generator, content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")