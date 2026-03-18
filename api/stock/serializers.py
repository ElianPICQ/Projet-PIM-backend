from rest_framework import serializers
from .models import StockProduct

class StockProductSerializer(serializers.ModelSerializer):
    comments = serializers.CharField(required=False, allow_blank=True, allow_null=True, default='')

    def validate_comments(self, value):
        return '' if value is None else value

    class Meta:
        model = StockProduct
        fields = '__all__'