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
from xhtml2pdf import pisa

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

    #Generate kode Unik dan QR Code nya

    class GenerateCertificate(View):
        def get(self, request, *args, **kwargs):
            #generate kode uniknya
            kode_unik = self.generate_unique_code()
            
            #generate qrcodenya
            qr = qrcode.QrCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(kode_unik)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("qrcode.png")
            
            #read sertifikat
            template = get_template('certificate_template.html')
            
            #bikin konteks kode unik
            context = {'kode_unik': kode_unik, 'qrcode': cv2.imread('qrcode.png')}
            
            #render sertifikat
            html = template.render(context)
            
            #generate pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
            pisaStatus = pisa.CreatePDF(html, dest=response)
            
            return response
        
        def generate_unique_code(self, length=6):
            #generate kode unik
            chars = string.ascii_uppercase + string.digits + string.digits
            code = ''.join(random.choice(chars) for _ in range(length))
            return code