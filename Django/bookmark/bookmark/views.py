from django.shortcuts import render
from django.http import HttpResponse
from bookmark.models import Bookmark
# from django.http import Http404
from django.shortcuts import get_object_or_404

def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(id__gte=50)
    context = {
        'bookmarks': bookmarks,
    }
    return render(request, 'bookmark_list.html', context)

def bookmark_detail(request, pk):
    # try:
    #     bookmark = Bookmark.objects.get(pk=pk)
    # except:
    #     raise Http404
    # try문이나 get_object_or_404나 둘다 가능
    bookmark = get_object_or_404(Bookmark, pk=pk)

    context = {'bookmark': bookmark}
    return render(request, 'bookmark_detail.html', context)