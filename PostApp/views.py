from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from django.contrib import messages
from .forms import *
from django.views import View
from django.shortcuts import get_object_or_404
from .templatetags import get_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views import generic
from django.urls import reverse_lazy
from fpdf import FPDF
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

# Create your views here.

@method_decorator([login_required(login_url='login'), never_cache], name='dispatch')
class PostListView(View):
  def get(self, request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    if not posts:
      messages.info(request, "No published posts available.")

    return render(request, 'PostApp/post_list.html', {'posts': posts})

@method_decorator([login_required(login_url='login'), never_cache], name='dispatch')
class PostCreateView(View):
  def get(self, request):
    form = PostForm()
    return render(request, "PostApp/create_post.html", {'form': form})

  def post(self, request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      uploaded_file = request.FILES.get("post_doc")
      if uploaded_file:
        file_content = uploaded_file.read().decode('utf-8', errors='ignore')
        post.content = file_content
      post.author = request.user
      post.save()
      messages.success(request, "Post created successfully.")
      return redirect('post-list')


@method_decorator([login_required(login_url='login'), never_cache], name='dispatch')
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

@method_decorator([login_required(login_url='login'), never_cache], name='dispatch')
class PostEditView(generic.UpdateView):
  model = Post
  fields = ['title', 'content', 'post_image']
  template_name = 'PostApp/post_edit.html'

  def get_success_url(self):
    return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})

@method_decorator([login_required(login_url='login'), never_cache], name='dispatch')
class PostDeleteView(generic.DeleteView):
  model = Post
  template_name = 'PostApp/post_detail.html'
  success_url = reverse_lazy('post-list')

@login_required
def download_pdf(request, pk):
  post = Post.objects.get(pk=pk)
  pdf = FPDF()
  content = post.content
  content = strip_tags(content)
  title = strip_tags(post.title)

  pdf.add_page()
  pdf.set_font("Arial", size=12)
  text_content = f"{title}\n\n{content}"
  pdf.multi_cell(0, 10, text_content) # 0 for full width, 10 for line height

  # breakpoint()
  # Output PDF to response
  # pdf.output(dest='F').encode('latin1')  # Ensure PDF is written correctly
  pdf_output = pdf.output(dest='S').encode('latin1')  # 'S' returns PDF as string
  response = HttpResponse(pdf_output, content_type='application/pdf')
  response['Content-Disposition'] = f'attachment; filename="{post.title}.pdf"'

  # response.write(pdf_output)
  return response
