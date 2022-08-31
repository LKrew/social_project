from django.views.generic import ListView, CreateView, DeleteView, DetailView
from posts import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http  import Http404, HttpResponseRedirect
from braces.views import SelectRelatedMixin
from . import models, forms
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.

User = get_user_model()

class PostList(LoginRequiredMixin,ListView):
    model = models.Post

class UserPostList(LoginRequiredMixin,ListView):
    model = models.Post
    template_name = 'posts/user_profile.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class NewPost(LoginRequiredMixin,SelectRelatedMixin,CreateView):
    fields = ['message']
    model = models.Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        form.instance.author = self.request.user
        self.object.save()
        return super().form_valid(form)
    
class DeletePost(LoginRequiredMixin, DeleteView):
    model = models.Post
    success_url = '/posts/post_list/'

    def get_queryset(self):
        return super().get_queryset()

    def form_valid(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

class SinglePost(LoginRequiredMixin, DetailView):
    model = models.Post


# class NewComment(LoginRequiredMixin,CreateView):
#     fields = ['text']
#     model = models.Comment
#     template_name = 'posts/comment_form.html'

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         print(self.request)
#         self.object.post = 
#         form.instance.author = self.request.user
#         self.object.save()
#         return super().form_valid(form)
    
@login_required
def new_comment(request, pk):
    #pk = request.POST.get('pk')
    post = get_object_or_404(models.Post, pk=pk)
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('posts:single', pk=post.pk)
    else:
        form = forms.CommentForm()
    return render(request, 'posts/comment_form.html', {'form': form})

@login_required
def like_post(request, pk):
    if request.method == "POST":
        #make sure user can't like the post more than once. 
        user = User.objects.get(username=request.user.username)
        #find whatever post is associated with like
        post = models.Post.objects.get(pk=pk)

        newLike = models.LikedPost(user=user, post=post)
        newLike.alreadyLiked = True

        post.like_count += 1
        #adds user to Post 
        post.likes.add(user)
        post.save()
        newLike.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def unlike_post(request, pk):
    if request.method == "POST":
        #make sure user can't like the post more than once. 
        user = User.objects.get(username=request.user.username)
        #find whatever post is associated with like
        post = models.Post.objects.get(pk=pk)

        newLike = models.LikedPost(user=user, post=post)
        newLike.alreadyLiked = True

        post.like_count -= 1
        #delete user to Post 
        post.likes.remove(user)
        post.save()
        newLike.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def like_comment(request, pk):
    if request.method == "POST":
        #make sure user can't like the post more than once. 
        user = User.objects.get(username=request.user.username)
        #find whatever post is associated with like
        comment = models.Comment.objects.get(pk=pk)

        newLike = models.LikedComment(user=user, comment=comment)
        newLike.alreadyLiked = True

        comment.like_count += 1
        #adds user to Post 
        comment.likes.add(user)
        comment.save()
        newLike.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def unlike_comment(request, pk):
    if request.method == "POST":
        #make sure user can't like the post more than once. 
        user = User.objects.get(username=request.user.username)
        #find whatever post is associated with like
        comment = models.Comment.objects.get(pk=pk)

        newLike = models.LikedComment(user=user, comment=comment)
        newLike.alreadyLiked = True

        comment.like_count -= 1
        #delete user to Post 
        comment.likes.remove(user)
        comment.save()
        newLike.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


