from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post
from .forms import *
from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import datetime

def post_index(request):
    post_list = Post.objects.all()

    query = request.GET.get('q')
    if query:
        post_list = post_list.filter( 
            Q(title__icontains=query) | 
            Q(marka__icontains=query) |
            Q(model__icontains=query) |
            Q(kategori__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    kiralik = request.GET.get('kiralanmis')
    if kiralik:
        post_list = post_list.exclude(kiralayan="Yok").distinct()

    bosta = request.GET.get('kiralanmamis')
    if bosta:
        post_list = post_list.filter( 
            Q(kiralayan = "Yok")
        ).distinct()

    paginator = Paginator(post_list, 5) # Show 25 contacts per page

    page = request.GET.get('sayfa')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'post/index.html', {'posts':posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post,
    }
    return render(request, 'post/detail.html', context)

def post_create(request):

    if not request.user.is_authenticated:
        return Http404()
    
    # if request.method == "POST":
    #    print(request.POST)

    #title = request.POST.get('title')
    #content = request.POST.get('content')
    #Post.objects.create(title=title, content=content)

    #if request.method == "POST":
        # Formdan Gelen Bilgileri Kaydet
        #form = PostForm(request.POST)
        #if form.is_valid():
        #    form.save()
    #else:
        #Formu Kullanıcıya Göster
        #form = PostForm()

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user

        post.kiralayan = "Yok"
        post.baslama_tarih = "2023-06-22 14:54"
        post.bitis_tarih = "2023-06-22 14:54"

        post.save()
        messages.success(request, 'Başarılı Bir Şekilde Oluşturdunuz.', extra_tags='mesaj-basarili')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form,
    }

    return render(request, 'post/form.html', context)
 
def post_update(request, slug):
    if not request.user.is_authenticated:
        return Http404()
    
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()        
        messages.success(request, 'Başarılı Bir Şekilde Güncellediniz.')
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'post/form.html', context)

def post_delete(request, slug):
    if not request.user.is_authenticated:
        return Http404()
    
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post:index')

def post_kirala(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        form = KiralaForm(request.POST, instance=post)
        if form.is_valid():
            form.instance.kiralayan = request.user.username
            form.save()
            messages.success(request, 'Başarılı Bir Şekilde Kiraladınız.')
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = KiralaForm(instance=post, initial={'kiralayan': request.user.get_username()})
    
    context = {'form': form}
    return render(request, 'post/kirala_form.html', context)

def post_kirala_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    post.kiralayan = "Yok"
    post.save()
    messages.success(request, 'Kiralama kaydı silindi.')

    context = {
        'post': post,
    }
    
    return render(request, 'post/detail.html', context)



# Create your views here.
