from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse

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
            form.save()
            return HttpResponseRedirect('../')
    return render(request, 'create_course.html', {'form': courseList()})


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