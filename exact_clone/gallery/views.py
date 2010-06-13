# Create your views here.
from django.views.generic.simple import direct_to_template
from django.http import Http404, HttpResponse
from exact_clone.gallery.models import Category, SecondaryCategory, Photo


def index(request, primary_slug, secondary_slug=None):
    try:
        category = Category.objects.get(slug=primary_slug)
    except Category.DoesNotExist:
        raise Http404()


    if secondary_slug:
        try:
            sub_category = SecondaryCategory.objects.get(slug=secondary_slug)
        except SecondaryCategory.DoesNotExist:
            raise Http404()

    else:
        sub_categories = category.secondarycategory_set.all()[0:]
        if sub_categories.count():
            sub_category = sub_categories[0]
        else:
            sub_category = None

    return direct_to_template(request, 'gallery/index.html', {'category':category, 'selected_sub_cat':sub_category}) 


def detail(request, photo_slug):
    try:
        photo = Photo.objects.get(slug=photo_slug)
    except Photo.DoesNotExist:
        raise Http404()

    sub_category = photo.category
    category = sub_category.parent

    return direct_to_template(request, 'gallery/details.html', {'photo':photo, 'category':category, 'selected_sub_cat':sub_category})
