from exact_clone.gallery.models import Category

def category_list(request):
    categories = Category.objects.all()[0:4]
    return {'categories':categories}
