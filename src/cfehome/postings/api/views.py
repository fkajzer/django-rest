from rest_framework import generics
from postings.models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostRUDView(generics.RetrieveUpdateDestroyAPIView):
    pass

    lookup_field = 'pk'  # url(r'?P<pk>\d+')
    serializer_class = BlogPostSerializer
    # queryset = BlogPost.objects.all()

    def get_queryset(self):
        return BlogPost.objects.all()

#   use built in method, same as:
#    def get_object(self):
#        pk = self.kwargs.get('pk')
#        return BlogPost.objects.get(pk=pk)
