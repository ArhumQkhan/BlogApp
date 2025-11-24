from django.shortcuts import render, redirect
from .models import Post, Comment
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
    form = CommentForm()
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.order_by('-created_at')
    return render(request, "PostApp/post_detail.html", {'post': post, 'form': form, 'comments': comments})
  
  def post(self, request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = post
      comment.author = request.user
      parent_id = request.POST.get("parent_id")
      if parent_id:
        parent_comment = Comment.objects.get(pk=parent_id)
        comment.parent = parent_comment
      comment.save()
      messages.success(request, "Comment added successfully.")
      return redirect('post-detail', pk=pk)

