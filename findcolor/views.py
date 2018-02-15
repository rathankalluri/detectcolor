# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import numpy as np
import cv2
import os

# Create your views here.
def index(requests):
	return render(requests, 'findcolor/index.html')
	
def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = colorfinder(filename,fs)
        #uploaded_file_url = fs.url(filename)
		return render(request, 'findcolor/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
		
    return render(request, 'findcolor/upload.html')
	
def colorfinder(filename,fs):
	url = os.path.join(settings.MEDIA_ROOT,filename)
	image = cv2.imread(url)
	
	boundaries = [([1,1,150],[119,119,255]),([150,1,1],[255,199,199]),([1,150,1],[119,255,119]),([0,200,220],[100,255,255])]
	fname, ext = os.path.splitext(filename)
	count = 0
	uploaded_file_url = {}
	for (lower, upper) in boundaries:
		
		count = count + 1
		lower = np.array(lower, dtype = 'uint8')
		upper = np.array(upper, dtype = 'uint8')
		
		mask = cv2.inRange(image, lower, upper)
		output = cv2.bitwise_and(image, image, mask = mask)
		
		fn = os.path.join(settings.MEDIA_ROOT, fname+'-'+str(count)+'.jpg')
		cv2.imwrite(fn,np.hstack([image, output]))
		uploaded_file_url[fname+'-'+str(count)+'.jpg'] = os.path.join(settings.MEDIA_URL,fname+'-'+str(count)+'.jpg')
		
	return uploaded_file_url