from django.core.exceptions import ValidationError

class LabelValidationMixin:
    def validate_max_totes(self):
        from .models import Count, FrontLabel, BackLabel  # Local import to avoid circular dependency

        max_allowed = 8 if self.trolley.totes_count == Count.EIGHT else 10
        model_name = self.__class__.__name__

        if model_name == "FrontLabel":
            current_count = FrontLabel.objects.filter(trolley=self.trolley).count()
            label_side = "front"
        elif model_name == "BackLabel":
            current_count = BackLabel.objects.filter(trolley=self.trolley).count()
            label_side = "back"
        else:
            raise ValidationError("Unknown label type.")

        if not self.pk and current_count >= max_allowed:
            raise ValidationError(
                f"Trolley {self.trolley.id} already has the maximum allowed number of {label_side} labels ({max_allowed})."
            )


    def validate_unique_shape(self):
        from .models import Shapes, FrontLabel, BackLabel
        model_name = self.__class__.__name__

        if model_name == "FrontLabel":
            label_class = FrontLabel
            label_type = "front"
        elif model_name == "BackLabel":
            label_class = BackLabel
            label_type = "back"
        else:
            raise ValidationError("Unknown label type.")

        conflict_qs = label_class.objects.filter(trolley=self.trolley, shape=self.shape)
        if self.pk:
            conflict_qs = conflict_qs.exclude(pk=self.pk)

        if conflict_qs.exists():
            shape_name = Shapes(self.shape).label
            raise ValidationError(
                f"The shape '{shape_name}' is already assigned as a {label_type} label for this trolley."
            )
