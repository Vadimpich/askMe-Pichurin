from django.core.paginator import Paginator

def paginate(request, queryset, items_per_page=10):
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Обработка неверных значений уже встроена в функцию
    return page_obj
