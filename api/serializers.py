from rest_framework import serializers
from .models import Trolley, FrontLabel, BackLabel, Shapes
from .label_serializers import FrontLabelSerializer, BackLabelSerializer

class TrolleySerializer(serializers.ModelSerializer):
    front_label_count = serializers.IntegerField(read_only=True, source='front_label_count')
    back_label_count = serializers.IntegerField(read_only=True, source='back_label_count')
    total_label_count = serializers.IntegerField(read_only=True, source='total_label_count')
    missing_front_labels = serializers.ListField(
        child=serializers.CharField(), read_only=True, source='missing_front_labels'
    )
    missing_back_labels = serializers.ListField(
        child=serializers.CharField(), read_only=True, source='missing_back_labels'
    )
    missing_front_labels_count = serializers.IntegerField(read_only=True, source='missing_front_labels_count')
    missing_back_labels_count = serializers.IntegerField(read_only=True, source='missing_back_labels_count')

    front_labels = FrontLabelSerializer(many=True, required=False, source='frontlabel_set')
    back_labels = BackLabelSerializer(many=True, required=False, source='backlabel_set')

    class Meta:
        model = Trolley
        fields = [
            'id', 'totes_count', 'notes', 'in_use', 'created_at', 'updated_at',
            'front_label_count', 'back_label_count', 'total_label_count',
            'missing_front_labels', 'missing_back_labels',
            'missing_front_labels_count', 'missing_back_labels_count',
            'front_labels', 'back_labels',
        ]
        read_only_fields = (
            'created_at', 'updated_at',
            'front_label_count', 'back_label_count', 'total_label_count',
            'missing_front_labels', 'missing_back_labels',
            'missing_front_labels_count', 'missing_back_labels_count',
        )
    
    def create(self, validated_data):
        front_labels_data = validated_data.pop('front_labels', [])
        back_labels_data = validated_data.pop('back_labels', [])
        trolley = Trolley.objects.create(**validated_data)

        # Create front labels linked to trolley
        for label_data in front_labels_data:
            FrontLabel.objects.create(trolley=trolley, **label_data)

        # Create back labels linked to trolley
        for label_data in back_labels_data:
            BackLabel.objects.create(trolley=trolley, **label_data)

        return trolley

    def update(self, instance, validated_data):
        front_labels_data = validated_data.pop('front_labels', [])
        back_labels_data = validated_data.pop('back_labels', [])

        # Update trolley fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update front labels
        self._update_nested_labels(instance, FrontLabel, front_labels_data)

        # Update back labels
        self._update_nested_labels(instance, BackLabel, back_labels_data)

        return instance

    def _update_nested_labels(self, trolley, model, labels_data):
        """
        Update or create nested labels for the trolley.
        labels_data: list of dicts with 'id' (optional), 'shape', 'checked'
        """
        existing_labels = model.objects.filter(trolley=trolley)
        existing_labels_map = {label.id: label for label in existing_labels}

        sent_ids = set()
        for label_data in labels_data:
            label_id = label_data.get('id', None)
            if label_id and label_id in existing_labels_map:
                # Update existing label
                label = existing_labels_map[label_id]
                label.shape = label_data.get('shape', label.shape)
                label.checked = label_data.get('checked', label.checked)
                label.save()
                sent_ids.add(label_id)
            else:
                # Create new label
                model.objects.create(trolley=trolley, **label_data)
