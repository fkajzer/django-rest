from .views import BlogPostRUDView
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<pk>\d+)$', BlogPostRUDView.as_view(), name='post-rud'),
]
