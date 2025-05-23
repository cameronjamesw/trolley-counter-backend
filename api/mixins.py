from django.core.exceptions import ValidationError

class LabelValidationMixin:
    def validate_max_totes(self):
        from .models import Count, FrontLabel, BackLabel  # Local import to avoid circular dependency

        # Determine the max allowed based on tote count
        max_allowed = 8 if self.trolley.totes_count == Count.EIGHT else 10

        # Determine model type: front or back
        is_front_label = isinstance(self, FrontLabel)
        is_back_label = isinstance(self, BackLabel)

        if is_front_label:
            current_count = FrontLabel.objects.filter(trolley=self.trolley).count()
        elif is_back_label:
            current_count = BackLabel.objects.filter(trolley=self.trolley).count()
        else:
            raise ValidationError("Unknown label type.")

        # If creating a new instance (no PK), check the limit
        if not self.pk and current_count >= max_allowed:
            label_side = "front" if is_front_label else "back"
            raise ValidationError(
                f"Trolley {self.trolley.id} already has the maximum allowed number of {label_side} labels ({max_allowed})."
            )

    def validate_unique_shape(self):
        from .models import Shapes, FrontLabel, BackLabel  # Local import

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
