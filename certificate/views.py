import cv2
import numpy as np
from .forms import ImageForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def create(request):
    if request.method == 'POST' and request.FILES['image']:
        # memuat gambar
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        # membaca gambar
        img = cv2.imread(uploaded_file_url[1:])

        # menambahkan teks
        font = cv2.FONT_HERSHEY_PLAIN
        text = request.POST['text'] # memperoleh teks yang diinputkan
        color = (0, 0, 0)
        thickness = 2
        org = (50, 400)
        img = cv2.putText(img, text, org, font, thickness, color, cv2.LINE_AA)

        # menyimpan gambar
        cv2.imwrite(uploaded_file_url[1:], img)

        return render(request, 'result.html', {'uploaded_file_url': uploaded_file_url})

    return render(request, 'create.html')
