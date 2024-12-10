from django.core.paginator import Paginator
from django.shortcuts import render
from .models import BlogPost
from .utils import get_user_country

def post_list(request):
    country = get_user_country(request=request)
    

    posts = BlogPost.objects.all().order_by('created_at')
    filtered_posts = posts.filter(country=country)
    print(country)

    paginator = Paginator(posts, 28)
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)
    

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'filtered_posts': filtered_posts,
        'country': country,
    })
