from .models import category
from django.db.models import Avg
def menu_links(request):
    categories = category.objects.all()
    return dict(categories=categories)