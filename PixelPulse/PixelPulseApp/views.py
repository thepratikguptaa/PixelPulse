from django.shortcuts import render
from .models import Post
from .forms import PostForm
from django.shortcuts import get_object_or_404, redirect

# Create your views here.

def index(request):
    return render(request, 'index.html')


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user = request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
        pass
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})

def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user = request.user)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'post_confirm_delete.html', {'post': post})