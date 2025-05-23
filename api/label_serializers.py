from rest_framework import serializers
from .models import FrontLabel, BackLabel
from .mixins import LabelValidationMixin

class BaseLabelSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        instance = self.Meta.model(**attrs)
        if self.instance:
            instance.pk = self.instance.pk

        validator = LabelValidationMixin()
        validator.trolley = instance.trolley
        validator.shape = instance.shape
        validator.pk = instance.pk
        validator.validate_max_totes()
        validator.validate_unique_shape()

        return attrs

class FrontLabelSerializer(BaseLabelSerializer):
    class Meta:
        model = FrontLabel
        fields = ['id', 'trolley', 'shape', 'checked', 'created_at']
        read_only_fields = ['created_at']

class BackLabelSerializer(BaseLabelSerializer):
    class Meta:
        model = BackLabel
        fields = ['id', 'trolley', 'shape', 'checked', 'created_at']
        read_only_fields = ['created_at']