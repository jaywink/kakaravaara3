from django.http import Http404
from django.utils.translation import get_language

from shoop.simple_cms.views import PageView


class KakaravaaraIndexView(PageView):

    def get_object(self, queryset=None):
        return self.model.objects.get(identifier="index")

    def get(self, request, *args, **kwargs):
        # get currently active language
        self.object = self.get_object()
        if not self.object.has_translation(get_language()):
            # Page hasn't been translated into the current language; that's always a 404
            raise Http404()

        self.object.set_current_language(get_language())

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
