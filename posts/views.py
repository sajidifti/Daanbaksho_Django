from multiprocessing import context
from winreg import DeleteValue
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import *
from donations.models import *
from daanbaksho import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .models import *
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import *


# Create your views here.

# Post
class PostListView(ListView):
    model = post
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = post



class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'short_desc', 'content','image']

    def form_valid(self, form):
        form.instance.post_user = self.request.user
        return super().form_valid(form)




class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title', 'short_desc', 'content','image']

    def form_valid(self, form):
        form.instance.post_user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/posts/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_user:
            return True
        return False


# Media
class MediaListView(ListView):
    model = postMedia
    context_object_name = 'medias'


class MediaDetailView(DetailView):
    model = postMedia



class MediaCreateView(LoginRequiredMixin, CreateView):
    model = postMedia
    fields = ['image']

    def form_valid(self, form):
        form.instance.post_user = self.request.user
        return super().form_valid(form)




class MediaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = postMedia
    fields = ['image']

    def form_valid(self, form):
        form.instance.post_user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_user:
            return True
        return False


class MediaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = postMedia
    success_url = '/media/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_user:
            return True
        return False
















# class PostCreateView(LoginRequiredMixin, CreateView):
#     form_class = PostCreateForm
#     template_name = 'posts/post_form.html'
#     success_url = '/posts/'

#     def form_valid(self, form):
#         form.instance.post_user = self.request.user
#         return super().form_valid(form)






# def posts(request):
#     posts = posts.objects.all()

#     context = {
#         'posts': posts,
#     }

#     return render(request, 'posts/posts.html', context)



# def createPost(request):
#     if request.method == 'POST':
#         p_title = request.POST.get('p_title')
#         p_desc = request.POST.get('p_desc')
#         p_content = request.POST.get('p_content')
#         image = request.POST.get('p_content')
#         post_user = request.user

#         post = post.objects.create(
#             total_items=p_title, items_description=image)


#         messages.success(
#             request, "Your Post Was Succesfully Published")

#         return redirect('donorClothDonationHistory')

#     return render(request, 'donations/cloth_donation_form.html')