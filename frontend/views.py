from django.views.generic import (
    TemplateView, 
)


class LandingPageView(TemplateView):
    """Головна сторінка (Landing Page) з презентацією платформи."""
    template_name = 'frontend/index.html'
