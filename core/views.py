from django.shortcuts import render, get_object_or_404
from .models import Category, Video, Suggestion
from .forms import SuggestionForm

def home(request):
    categories = Category.objects.all()
    selected_slug = request.GET.get('category')
    show_recommended = request.GET.get('recommended')

    if show_recommended:
        videos = Video.objects.filter(recommended=True)
        selected_category = None
    elif selected_slug:
        selected_category = get_object_or_404(Category, slug=selected_slug)
        videos = Video.objects.filter(category=selected_category)
    else:
        selected_category = None
        videos = Video.objects.all()

    return render(request, 'core/home.html', {
        'categories': categories,
        'videos': videos,
        'selected_category': selected_category,
        'show_recommended': bool(show_recommended),
    })

def video_detail(request, youtube_id):
    video = get_object_or_404(Video, youtube_id=youtube_id)
    return render(request, 'core/video_detail.html', {'video': video})

def suggest(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'core/suggest_success.html')
    else:
        form = SuggestionForm()
    return render(request, 'core/suggest.html', {'form': form})