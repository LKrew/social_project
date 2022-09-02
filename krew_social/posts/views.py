from django.views.generic import ListView, CreateView, DeleteView, DetailView
from posts.models import Post, LikedPost, Comment, LikedComment, Repost
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http  import Http404, HttpResponseRedirect
from . import forms
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from itertools import chain
# Create your views here.

User = get_user_model()

class PostList(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'posts/post_list.html'

    def get_queryset(self): 
        posts = Post.objects.all()
        reposts = Repost.objects.all()
        post_list = sorted(chain(posts, reposts),key = lambda instance : instance.created_at)
        return post_list
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all()
        reposts = Repost.objects.all()
        context['post_list'] = sorted(chain(posts, reposts),key = lambda instance : instance.created_at, reverse=True)
        return context

class UserPostList(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'posts/user_profile.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()
        
    def get_context_data(self, **kwargs):
        context = super(UserPostList, self).get_context_data(**kwargs)
        context['post_user'] = self.post_user
        context['reposts'] = Repost.objects.select_related('author').filter(author__username__iexact=self.kwargs.get('username'))
        return context

class NewPost(LoginRequiredMixin,CreateView):
    fields = ['message']
    model = Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        form.instance.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    
class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/posts/post_list/'

    def get_queryset(self):
        return super().get_queryset()

    def form_valid(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    
    def get_success_url(self) -> str:
        return reverse('posts:posts')

    def get_queryset(self):
        return super().get_queryset()

    def form_valid(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

class DeleteRepost(DeleteView):
    model = Repost

    def get_success_url(self) -> str:
        return reverse('posts:posts')
    
    def get_queryset(self):
        return super().get_queryset()

    def form_valid(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

class SinglePost(LoginRequiredMixin, DetailView):
    model = Post

    
@login_required
def new_comment(request, pk):
    #pk = request.POST.get('pk')
    post = get_object_or_404(Post, pk=pk)
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
def repost(request, pk):
    if request.method == "POST":

        user = User.objects.get(username=request.user.username)
        
        post = Post.objects.get(pk=pk)

        repost = Repost(author=user, post=post)
        
        #adds user to Post 
        post.save()
        repost.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def like_post(request, pk):
    if request.method == "POST":
        #make sure user can't like the post more than once. 
        user = User.objects.get(username=request.user.username)
        #find whatever post is associated with like
        post = Post.objects.get(pk=pk)

        newLike = LikedPost(author=user, post=post)
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
        post = Post.objects.get(pk=pk)

        newLike = LikedPost(author=user, post=post)
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
        comment = Comment.objects.get(pk=pk)

        newLike = LikedComment(author=user, comment=comment)
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
        comment = Comment.objects.get(pk=pk)

        newLike = LikedComment(author=user, comment=comment)
        newLike.alreadyLiked = True

        comment.like_count -= 1
        #delete user to Post 
        comment.likes.remove(user)
        comment.save()
        newLike.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


