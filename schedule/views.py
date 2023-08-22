from django.views import generic as g

from .models import Coach, SportType, TrainingInfo


class CoachListView(g.ListView):
    model = Coach
    template_name = 'coach_list.html'

    def get_queryset(self):
        print(self.model.objects.all().first().images.first().image)
        return self.model.objects.all()


class CoachDetailView(g.DetailView):
    model = Coach
    context_object_name = 'coach'
    template_name = 'coach_detail.html'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        return self.model.objects.get(slug_field=slug)
