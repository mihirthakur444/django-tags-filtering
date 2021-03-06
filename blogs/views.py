from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify

from .models import Post
from .forms import PostForm
from taggit.models import Tag


def home_view(request):
    posts = Post.objects.order_by('-published')
    # Show most common tags
    common_tags = Post.tags.most_common()[:4]
    form = PostForm(request.POST)
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
    context = {
        'posts':posts,
        'common_tags':common_tags,
        'form':form,
    }
    return render(request, 'blogs/home.html', context)

def detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post':post,
    }
    return render(request, 'detail.html', context)

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'posts':posts,
    }
    return render(request, 'blogs/home.html', context)
