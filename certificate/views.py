import cv2
import qrcode
import string
import random
import numpy as np
from .forms import ImageForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import View

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
        thickness = 7
        org = (50, 350)
        img = cv2.putText(img, text, org, font, thickness, color, cv2.LINE_AA)

        #kode unik
        kode_unik = generate_unique_code()
        font = cv2.FONT_HERSHEY_PLAIN
        text = kode_unik
        color = (0, 0, 0)
        thickness = 1
        org = (50, 50)
        font_scale = 1  # ubah nilai ukuran font menjadi 0.5
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_width = text_size[0]
        text_height = text_size[1]
        text_x = org[0] - text_width // 2
        text_y = org[1] + text_height // 2
        img = cv2.putText(img, text, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)


        #generate qrcodenya
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(kode_unik)
        qr.make(fit=True)  
        img_qr = qr.make_image(fill_color="black", back_color="white")
        img_qr.save("qrcode.png")

        # Menambahkan QR code ke dalam foto
        qr = cv2.imread('qrcode.png')
        x_offset = 500
        y_offset = 50
        img[y_offset:y_offset+qr.shape[0], x_offset:x_offset+qr.shape[1]] = qr

        # menyimpan gambar
        cv2.imwrite(uploaded_file_url[1:], img)

        return render(request, 'result.html', {'uploaded_file_url': uploaded_file_url})

    return render(request, 'create.html')

    #Generate kode Unik dan QR Code nya
def generate_unique_code(length=6):
    #generate kode unik
    chars = string.ascii_uppercase + string.digits + string.digits
    code = ''.join(random.choice(chars) for _ in range(length))
    return code