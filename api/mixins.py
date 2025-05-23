from django.core.exceptions import ValidationError
from .models import Count, Shapes

class LabelValidationMixin:
    def validate_max_totes(self):
        from .models import FrontLabel, BackLabel  # Local import to avoid circular import
        total_labels = (
            FrontLabel.objects.filter(trolley=self.trolley).count() +
            BackLabel.objects.filter(trolley=self.trolley).count()
        )
        max_allowed = 8 if self.trolley.totes_count == Count.EIGHT else 10

        # Only raise if it's a new label (no pk)
        if total_labels >= max_allowed and not self.pk:
            raise ValidationError(
                f"Trolley {self.trolley.id} already has the maximum allowed number of labels ({max_allowed})."
            )

    def validate_unique_shape(self):
        from .models import FrontLabel, BackLabel  # Local import

        label_classes = [FrontLabel, BackLabel]
        label_types = ["FrontLabel", "BackLabel"]

        for label_class, label_type in zip(label_classes, label_types):
            conflict_qs = label_class.objects.filter(trolley=self.trolley, shape=self.shape)
            if self.pk:
                conflict_qs = conflict_qs.exclude(pk=self.pk)
            if conflict_qs.exists():
                shape_name = Shapes(self.shape).label
                raise ValidationError(
                    f"The shape '{shape_name}' is already assigned as a {label_type} for this trolley."
                )
