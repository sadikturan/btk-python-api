from rest_framework import serializers
from .models import Comment
from products.models import Product
from drf_spectacular.utils import extend_schema_field

class CommentProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug"]

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = CommentProductSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'rating','description','active','created','update','product','user']
        extra_kwargs = { 'product': {'read_only': True} }

    @extend_schema_field(serializers.CharField())
    def get_user(self, obj):
        return obj.user.username if obj.user else None

