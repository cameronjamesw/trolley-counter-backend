from rest_framework import serializers
from .models import Trolley, FrontLabel, BackLabel, Shapes
from .mixins import LabelValidationMixin

class TrolleySerializer(serializers.ModelSerializer):
    front_labels = serializers.SerializerMethodField()
    back_labels = serializers.SerializerMethodField()
    total_label_count = serializers.SerializerMethodField()
    missing_front_labels = serializers.SerializerMethodField()
    missing_front_labels_count = serializers.SerializerMethodField()
    missing_back_labels = serializers.SerializerMethodField()
    missing_back_labels_count = serializers.SerializerMethodField()

    class Meta:
        model = Trolley
        fields = [
            'id', 'totes_count', 'notes', 'in_use',
            'created_at', 'updated_at',
            'front_label_count', 'back_label_count', 'total_label_count',
            'missing_front_labels', 'missing_back_labels',
            'missing_front_labels_count', 'missing_back_labels_count',
        ]

        read_only_fields = (
            'created_at', 'updated_at',
            'front_label_count', 'back_label_count', 'total_label_count',
            'missing_front_labels', 'missing_back_labels',
            'missing_front_labels_count', 'missing_back_labels_count',
        )

    def get_front_label_count(self, obj):
        return FrontLabel.objects.filter(trolley=obj).count()

    def get_back_label_count(self, obj):
        return BackLabel.objects.filter(trolley=obj).count()

    def get_total_label_count(self, obj):
        return self.get_front_label_count(obj) + self.get_back_label_count(obj)
    
    def get_missing_front_labels(self, obj):
        # Get unchecked FrontLabels for this trolley and return shape names
        missing = FrontLabel.objects.filter(trolley=obj, checked=False).values_list('shape', flat=True)
        return [Shapes(shape_id).label for shape_id in missing]

    def get_missing_back_labels(self, obj):
        # Same for BackLabels
        missing = BackLabel.objects.filter(trolley=obj, checked=False).values_list('shape', flat=True)
        return [Shapes(shape_id).label for shape_id in missing]
    
    def get_missing_front_labels_count(self, obj):
        return FrontLabel.objects.filter(trolley=obj, checked=False).count()

    def get_missing_back_labels_count(self, obj):
        return BackLabel.objects.filter(trolley=obj, checked=False).count()


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