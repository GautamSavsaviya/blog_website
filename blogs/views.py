from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Blog
from .forms import BlogsForm
import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    blogs_list = Blog.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(blogs_list, 15)
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)
    newest_blogs = blogs_list[:4]

    context = {
        'blogs': blogs,
        'range': range(1, 3),
        'newest_blogs': newest_blogs,
        'paginator': paginator
    }
    return render(request, 'blogs/index.html', context)


def detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    context = {
        'blog': blog,
    }
    return render(request, 'blogs/detail.html', context)


@login_required(login_url='users:login')
def my_blogs(request):
    published = request.GET.get('published')
    print(published)
    if published is None:
        blogs_list = Blog.objects.filter(user=request.user).order_by('-created_at')
    elif published:
        blogs_list = Blog.objects.filter(user=request.user, is_published=published).order_by('-created_at')
    else:
        blogs_list = Blog.objects.filter(user=request.user, is_published=published).order_by('-created_at')


    paginator = Paginator(blogs_list, 15)
    page_num = request.GET.get("page")
    blogs = paginator.get_page(page_num)

    context = {
        'blogs': blogs,
        'paginator': paginator,
    }
    return render(request, 'blogs/my-blogs.html', context)


@login_required(login_url='users:login')
def add_blog(request):
    if request.method == "POST":
        form = BlogsForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.user = request.user
            if form.instance.is_published:
                form.instance.published_at = datetime.datetime.now()
            form.save()
            return redirect('blogs:my_blogs')
    else:
        form = BlogsForm()

    context = {
        "form": form,
        'btn_name': "Add",
    }
    return render(request, 'blogs/add-blog.html', context)


@login_required(login_url='users:login')
def update_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    if request.method == "POST":
        form = BlogsForm(request.POST or None,
                         request.FILES or None, instance=blog)
        if form.is_valid():
            form.instance.user = request.user
            if form.instance.is_published:
                form.instance.published_at = datetime.datetime.now()
            else:
                form.instance.published_at = None
            form.save()
            return redirect('blogs:my_blogs')
    else:
        form = BlogsForm(instance=blog)

    context = {
        'form': form,
        'btn_name': "update",
    }
    return render(request, 'blogs/add-blog.html', context)


@login_required(login_url='users:login')
def delete_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    blog.is_deleted = True
    blog.save()
    return redirect('blogs:my_blogs')
