from rest_framework import serializers
from .models import FrontLabel, BackLabel, Shapes


class BaseLabelSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        # If 'trolley' is required for validation, make sure it's present
        trolley = attrs.get('trolley') or (
            self.instance.trolley if self.instance else None
            )

        # Only call model validations if trolley is available
        if trolley:
            instance = self.instance or self.Meta.model(
                trolley=trolley, **attrs
                )

            # Set pk if updating
            if self.instance:
                instance.pk = self.instance.pk

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
        extra_kwargs = {
            'id': {'read_only': True},
            'trolley': {'required': False}
        }

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
        extra_kwargs = {
            'id': {'read_only': True},
            'trolley': {'required': False}
        }

    def get_shape_name(self, obj):
        return Shapes(obj.shape).label
