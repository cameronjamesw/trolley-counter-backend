from rest_framework import serializers
from .models import FrontLabel, BackLabel, Shapes


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
    creator = serializers.ReadOnlyField(source='creator.username')
    shape_name = serializers.SerializerMethodField()

    class Meta:
        model = FrontLabel
        fields = ['id', 'creator', 'trolley', 'shape',
                  'shape_name', 'checked', 'created_at']
        read_only_fields = ['created_at']

    def get_shape_name(self, obj):
        return Shapes(obj.shape).label


class BackLabelSerializer(BaseLabelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    shape_name = serializers.SerializerMethodField()

    class Meta:
        model = BackLabel
        fields = ['id', 'creator', 'trolley', 'shape',
                  'shape_name', 'checked', 'created_at']
        read_only_fields = ['created_at']

    def get_shape_name(self, obj):
        return Shapes(obj.shape).label
