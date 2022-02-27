from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Tag
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
# Create your views here.
def home(request):
    posts = Post.objects.filter(active=True, featured=True)
    tags = Tag.objects.all()
    context = {
        'posts': posts.order_by,
        'tags': tags
        }
    return render(request, "base/index.html", context)


def posts(request):
    posts = Post.objects.filter(active=True).order_by('-created')
    page = request.GET.get('page')
    paginator = Paginator(posts, 3)

    # Re-arange so that tags filter posts
    # tag = request.POST.get('tag')
    # if tag == None:
    #     posts = Post.objects.filter(active=True).order_by("-created")
    # else:
    #     posts = Post.objects.filter(active=True, tag__name=tag).order_by("-created")

    # tags = Tag.objects.all()

    # try: 
    #     posts= paginator.page(page)
    # except PageNotAnInteger:
    #     posts= paginator.page(1)
    # except EmptyPage:
    #     posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        # 'tags': tags
        
    }
    return render(request, 'base/posts.html', context)


@login_required(login_url='home')
def postCreate(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'forms/post_form.html', context)


@login_required(login_url='home')

def postUpdate(request, pk):
    post= Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form =PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'forms/post_form.html', context)

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    success_url= '/'

    def test_func(self):
        post= self.get_object()
        if self.request.user.is_authenticated:
            return True
        return False


def search_posts(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(
            Q(headline__icontains = searched) |
            Q(sub_headline__icontains = searched) |
            Q(body__icontains = searched)
        )
        page = request.GET.get('page')
        paginator = Paginator(posts, 3)

        try: 
            posts= paginator.page(page)
        except PageNotAnInteger:
            posts= paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            'searched': searched,
            'posts':posts,
        }

        return render(request, 'base/search_posts.html', context)
    else:
        return render(request, 'base/search_posts.html')

def about(request):
    return  render(request, 'base/my_story.html')