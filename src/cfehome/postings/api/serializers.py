from rest_framework import serializers
from postings.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta():
        model = BlogPost
        fields = [
            'pk',
            'user',
            'title',
            'content',
            'timestamp',
        ]

        read_only_fields = ['user']

    # converts to json, validates data passed

    def validate_title(self, value):
        qs = BlogPost.objects.filter(title__iexact=value)  # includes itself
        if self.instance:  # excludes itself
            qs = qs.exlude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "the title has already been used")

        return value
