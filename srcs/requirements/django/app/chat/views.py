from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
  ListView,
  CreateView
)
from django.urls import reverse_lazy
from .models import Comment
from .forms import CommentForm
from django.http import JsonResponse
from django.template.loader import render_to_string

def home(request):
  context = {
    'comments' : Comment.objects.all()
  }
  return render(request, 'chat/home.html', context)

class CommentListView(ListView):
  model = Comment
  template_name = 'chat/home.html'
  context_object_name = 'comments'
  ordering = ['time']
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = CommentForm()
    return context
  
  
class CommentCreateView(LoginRequiredMixin, CreateView):
  model = Comment
  fields = ['content']

  def form_valid(self, form):
    form.instance.author = self.request.user
    self.object = form.save()
    
    rendered_comment = render_to_string('chat/_comment.html', {'comment': self.object})
    return JsonResponse({
        'success': True,
        'comment_html': rendered_comment,
    })

  def form_invalid(self, form):
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)  
  
def about(request):
  return render(request, 'chat/about.html', {'title': "About"})
