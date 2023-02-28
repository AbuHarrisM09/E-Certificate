from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, redirect
from django.urls import reverse
import cv2
import numpy as np
import cvzone

from django.conf import settings
from .models import course
from .forms import courseList


# Create your views here.
def data(request):
    context = {}
    context['course'] = course.objects.all()
    return render(request, 'result_course.html', context)


def create(request):
    if request.method == 'POST':
        form = courseList(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            
            # Mengambil path gambar template
            image_path = settings.MEDIA_ROOT + '/' + str(course.template)

            # Menambahkan tanda tangan ke gambar template
            signature = request.FILES['signature']
            signature_path = settings.MEDIA_ROOT + '/signature/' + signature.name
            with open(signature_path, 'wb+') as destination:
                for chunk in signature.chunks():
                    destination.write(chunk)
            add_signature_to_image(image_path, signature_path)

            

            return redirect('../', course.id)
    else:
        form = courseList()

    context = {
        'form': form,
    }

    return render(request, 'create_course.html', context)

def detail(request, id):
    context = {
        'data': course.objects.get(id = id)
    }
    return render(request, 'detail_course.html', context)


def edit(request, id):
    context = {}

    obj = get_object_or_404(course, id = id)
    form = courseList(request.POST or None, request.FILES or None, instance = obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('course:detail_course', args=(obj.id,)))
        
    context['form'] = form
    return render(request, 'create_course.html', context)


def delete(request, id):
    context = {}

    obj = get_object_or_404(course, id = id)
    if request.method == 'POST':
        obj.delete()
        return HttpResponseRedirect('../../')
    return render(request, 'delete_course.html', context)

def add_signature_to_image(image_path, signature_path):
    # Load gambar menggunakan OpenCV
    img = cv2.imread(image_path)

    # Load tanda tangan menggunakan OpenCV
    signature = cv2.imread(signature_path, cv2.IMREAD_UNCHANGED)

    # Resize tanda tangan sesuai ukuran template
    resized_signature = cv2.resize(signature, (0, 0), None, 3, 3)

    # Pastikan ukuran gambar sama
    if resized_signature.shape[0] != img.shape[0] or resized_signature.shape[1] != img.shape[1]:
        resized_signature = cv2.resize(resized_signature, (img.shape[1], img.shape[0]))

    # Overlay gambar tanda tangan ke gambar template
    alpha_s = resized_signature[:, :, 3] / 255.0 if resized_signature.shape[2] == 4 else resized_signature[:, :, 0]

    alpha_l = 1.0 - alpha_s
    for c in range(0, 3):
        img[:, :, c] = (alpha_s * resized_signature[:, :, c] + alpha_l * img[:, :, c])

    # Simpan gambar yang sudah diedit
    cv2.imwrite(image_path, img)