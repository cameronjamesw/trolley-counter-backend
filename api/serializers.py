from rest_framework import serializers
from .models import Trolley, FrontLabel, BackLabel

class TrolleySerializer(serializers.ModelSerializer):
    class Meta:
        model = Trolley
        fields = '__all__'


class FrontLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontLabel
        fields = '__all__'


class BackLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackLabel
        fields = '__all__'