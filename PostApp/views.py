from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from django.contrib import messages
from .forms import PostForm, CommentForm, MailForm
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views import generic
from django.urls import reverse_lazy
from fpdf import FPDF
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()
# Create your views here.

@method_decorator([login_required(login_url='login'), never_cache], name='dispatch')
class PostListView(View):

  def get(self, request):

    try:
      posts = Post.objects.filter(status='published').order_by('-created_at')
    except Exception as e:
      logger.warning(f"Post Object is missing in PostListView | Error: {e}")

    return render(request, 'PostApp/post_list.html', {'posts': posts})

@method_decorator([login_required(login_url='login'), never_cache], name='dispatch')
class PostCreateView(View):

  def get(self, request):
    try:
      form = PostForm()
    except Exception as e:
      logger.warning("No PostForm object in PostCreateView")
      return HttpResponse(f"Error Occured: {e}", status=404)

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
    else:
      logger.warning("PostForm is not valid")
      return HttpResponse("Form is not Valid", status=400)


@method_decorator([login_required(login_url='login'), never_cache], name='dispatch')
class PostDetailView(View):

  def get(self, request, pk):

    form = CommentForm()
    post = get_object_or_404(Post, pk=pk)
    try:
      comments = Comment.objects.filter(post=post, parent=None)
      replies = Comment.objects.filter(post=post).exclude(parent=None)
    except Exception as e:
      logger.warning(f"Could not fetch Comment object in PostDetailView | Error: {e}")

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
    else:
      logger.warning("CommentForm is not valid")
      return redirect("post-detail")


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
  pdf_output = pdf.output(dest='S').encode('latin1')  # 'S' returns PDF as string
  response = HttpResponse(pdf_output, content_type='application/pdf')
  response['Content-Disposition'] = f'attachment; filename="{post.title}.pdf"'

  return response


class SendMailView(View):

  def get(self, request, pk):
    mail_form = MailForm()
    post = get_object_or_404(Post, pk=pk)
    return render(request, "Snippets/mail_form.html", {"mail_form":mail_form, "post":post})
  
  def post(self, request, pk):
    mail_form = MailForm(request.POST)
    post = get_object_or_404(Post, pk=pk)
    user = get_object_or_404(User, pk=post.author.pk)

    if mail_form.is_valid():
      recipient = mail_form.cleaned_data.get("recipient")

      try:
        send_mail(
          subject=post.title,
          message=post.content,
          from_email=user.email,
          recipient_list=[recipient]
        )
      except Exception as e:
        messages.error(request, f"Error sending the mail | Error: {e}")
        logger.warning(f"Error occured sending the mail in 'send_mail_view' | Error: {e}")
        return HttpResponse(f"Error occured sending the mail in 'send_mail_view' | Error: {e}")
      
      messages.success(request, "Mail sent successfully")
      logger.info("Form sent successfully")
      return HttpResponse("Email sent successfully")
    
    logger.warning("mail_form is not valid SendMailView")
    return render(request, "Snippets/mail_form.html", {"mail_form":mail_form, "post":post})
  