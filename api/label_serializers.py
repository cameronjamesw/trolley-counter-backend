from rest_framework import serializers
from .models import FrontLabel, BackLabel
from .mixins import LabelValidationMixin

class BaseLabelSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        # Build model instance for validation
        instance = self.instance or self.Meta.model(**attrs)

        # Set pk if updating existing instance
        if self.instance:
            instance.pk = self.instance.pk

        # Call the validation methods on the model instance
        instance.validate_max_totes()
        instance.validate_unique_shape()

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