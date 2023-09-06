from django.views import generic as g

from .models import Coach, SportType, TrainingInfo


class CoachListView(g.ListView):
    queryset = Coach.objects.all()
    template_name = 'coach_list.html'


class CoachDetailView(g.DetailView):
    model = Coach
    context_object_name = 'coach'
    template_name = 'coach_detail.html'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        return self.model.objects.get(slug_field=slug)


class SportTypeListView(g.ListView):
    queryset = SportType.objects.all()
    context_object_name = 'sport_types'
    template_name = 'sport_type_list.html'


class SportTypeDetailView(g.DateDetailView):
    model = SportType
    context_object_name = 'sport_type'
    template_name = 'sport_type_detail.html'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        if self.request.method == 'POST' and 'create' in self.request.POST:
            return self.model.custom_manager.get_queryset()
        return self.model.objects.get_queryset()

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        return self.model.objects.get(slug_name=slug)
