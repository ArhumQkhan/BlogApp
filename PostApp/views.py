from django.shortcuts import render, redirect
from .models import Post, Attachment
from django.contrib import messages
from .forms import PostForm
from django.views import View

# Create your views here.

class PostListView(View):
  def get(self, request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    if not posts:
      messages.info(request, "No published posts available.")

    return render(request, 'PostApp/post_list.html', {'posts': posts})


class PostCreateView(View):
  def get(self, request):
    form = PostForm()
    return render(request, "PostApp/create_post.html", {'form': form})

  def post(self, request):
    form = PostForm(request.POST)
    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      post.save()
      messages.success(request, "Post created successfully.")
      return redirect('post-list')

class PostDetailView(View):
  def get(self, request, pk):
    post = Post.objects.get(pk=pk)
    if not post:
      messages.info(request, "No, Post available")

    return render(request, "PostApp/post_detail.html", {'post': post})