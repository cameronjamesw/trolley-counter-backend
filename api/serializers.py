from rest_framework import serializers
from .models import Trolley, FrontLabel, BackLabel, Count
from .label_serializers import FrontLabelSerializer, BackLabelSerializer

class TrolleySerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    front_label_count = serializers.IntegerField(read_only=True)
    back_label_count = serializers.IntegerField(read_only=True)
    total_label_count = serializers.IntegerField(read_only=True)
    missing_front_labels = serializers.ListField(
        child=serializers.CharField(), read_only=True)
    missing_back_labels = serializers.ListField(
        child=serializers.CharField(), read_only=True)
    missing_front_labels_count = serializers.IntegerField(read_only=True)
    missing_back_labels_count = serializers.IntegerField(read_only=True)

    front_labels = FrontLabelSerializer(many=True, required=False)
    back_labels = BackLabelSerializer(many=True, required=False)

    class Meta:
        model = Trolley
        fields = [
            'id', 'creator', 'totes_count', 'notes', 'in_use', 'created_at', 
            'updated_at','front_label_count', 'back_label_count',
            'total_label_count', 'missing_front_labels', 'missing_back_labels',
            'missing_front_labels_count', 'missing_back_labels_count',
            'front_labels', 'back_labels',
        ]
        read_only_fields = (
            'creator', 'created_at', 'updated_at',
            'front_label_count', 'back_label_count', 'total_label_count',
            'missing_front_labels', 'missing_back_labels',
            'missing_front_labels_count', 'missing_back_labels_count',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['totes_count'] = Count(instance.totes_count).label
        return rep
    
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
