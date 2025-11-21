from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from .forms import PostForm, CommentForm
from django.views import View
from django.shortcuts import get_object_or_404

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
  


class CommentsView(View):
    # Handle displaying existing comments and comments form
    def get(self, request, post_id):
        # 1. Get the post the comments belong to
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_at')

        return render(request, 'CommentsApp/comments.html', {'post': post, 'form': form, 'comments': comments})

    # Handles the submission of a comment
    def post(self, request, post_id):
        post = get_object_or_404(Post, id = post_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post # post object created above
            comment.author = request.user
