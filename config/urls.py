from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', lambda request: HttpResponse(status=204)),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    path('', include([
        path('', include('geo_analytics.urls')),
        path('', include('logistics.urls')),
        path('', include('smart_planning.urls')),
        path('', include('warehousing.urls')),
        path('', include('users.urls')),
        path('', include('frontend.urls'))
    ])),
]