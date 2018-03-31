from rest_framework import serializers
from postings.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = BlogPost
        fields = [
            'url',
            'id',
            'user',
            'title',
            'content',
            'timestamp',
        ]

        read_only_fields = ['id', 'user']


    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    # converts to json, validates data passed
    def validate_title(self, value):
        qs = BlogPost.objects.filter(title__iexact=value)  # includes itself
        if self.instance and qs:  # excludes itself
            qs = qs.exlude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "the title has already been used")

        return value
