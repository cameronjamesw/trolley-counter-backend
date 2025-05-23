from django.core.exceptions import ValidationError
from .models import FrontLabel, BackLabel, Count, Shapes

class LabelValidationMixin:
    def validate_max_totes(self):
        total_labels = (
            FrontLabel.objects.filter(trolley=self.trolley).count() +
            BackLabel.objects.filter(trolley=self.trolley).count()
        )
        max_allowed = 8 if self.trolley.totes_count == Count.EIGHT else 10
        if total_labels >= max_allowed and not self.pk:
            raise ValidationError(f"Trolley {self.trolley.id} already has the maximum allowed number of labels ({max_allowed}).")

    def validate_unique_shape(self):
        if FrontLabel.objects.filter(trolley=self.trolley, shape=self.shape).exists():
            if not isinstance(self, FrontLabel) or (self.pk and not FrontLabel.objects.filter(pk=self.pk, shape=self.shape).exists()):
                shape_name = Shapes(self.shape).label
                raise ValidationError(f"The shape '{shape_name}' is already assigned as a FrontLabel for this trolley.")
        if BackLabel.objects.filter(trolley=self.trolley, shape=self.shape).exists():
            if not isinstance(self, BackLabel) or (self.pk and not BackLabel.objects.filter(pk=self.pk, shape=self.shape).exists()):
                shape_name = Shapes(self.shape).label
                raise ValidationError(f"The shape '{shape_name}' is already assigned as a BackLabel for this trolley.")
