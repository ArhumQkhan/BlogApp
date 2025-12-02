from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from django.contrib import messages
from .forms import PostForm, CommentForm
from django.views import View
from django.shortcuts import get_object_or_404
from .templatetags import get_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.urls import reverse_lazy
import logging

logger = logging.getLogger(__name__)

# Create your views here.

@method_decorator(login_required, name='dispatch')
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
    comments = Comment.objects.filter(post=post, parent=None)
    replies = Comment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
      if reply.parent.pk not in replyDict.keys():
        replyDict[reply.parent.pk] = [reply]
      else:
        replyDict[reply.parent.pk].append(reply)

    return render(request, "PostApp/post_detail.html", {'post': post, 'form': form, 'comments': comments, 'replyDict': replyDict})
  
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


@login_required
def post_like_view(request, pk):
  post = get_object_or_404(Post, id=pk)
  user_exists = post.likes.filter(username=request.user.username).exists()
  
  if user_exists:
    post.likes.remove(request.user)
  else:
    post.likes.add(request.user)

  return render(request, 'Snippets/likes.html', {'post':post})


class PostEditView(generic.UpdateView):
  model = Post
  fields = ['title', 'content']
  template_name = 'PostApp/post_edit.html'

  def get_success_url(self):
    return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})

class PostDeleteView(generic.DeleteView):
  model = Post
  template_name = 'PostApp/post_detail.html'
  success_url = reverse_lazy('post-list')
