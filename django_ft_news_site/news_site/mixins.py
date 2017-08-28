from django.views.generic.base import ContextMixin

class BaseContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        kwargs['title'] = "Bootstrap Sample"
        kwargs['project_name'] = "Bootstrap Sample"
        kwargs['show_header_banner'] = False
        kwargs['show_footer_banner'] = False
        return kwargs
