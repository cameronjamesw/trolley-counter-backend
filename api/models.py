from django.contrib.auth.models import User
from django.db import models
from .mixins import LabelValidationMixin

# Create your models here.


class Count(models.IntegerChoices):
    EIGHT = 1, 'Eight Totes'
    TEN = 2, 'Ten Totes'


class Shapes(models.IntegerChoices):
    SQUARE = 1, 'Square'
    CIRCLE = 2, 'Circle'
    TRIANGLE = 3, 'Triangle'
    CROSS = 4, 'Cross'
    SQUIGGLE = 5, 'Squiggle'
    HEART = 6, 'Heart'
    FLOWER = 7, 'Flower'
    PENGUIN = 8, 'Penguin'
    BOWTIE = 9, 'Bowtie'
    AIRPLANE = 10, 'Airplane'


class Trolley(models.Model):
    creator = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True, default=None,
                                related_name="trollies")
    totes_count = models.IntegerField(
        choices=Count.choices, default=Count.EIGHT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(max_length=200, blank=True)
    in_use = models.BooleanField(default=True)

    def __str__(self):
        return f"Trolley number {self.id}"

    @property
    def front_label_count(self):
        return self.frontlabel_set.count()

    @property
    def back_label_count(self):
        return self.backlabel_set.count()

    @property
    def total_label_count(self):
        return self.front_label_count + self.back_label_count

    @property
    def missing_front_labels(self):
        missing_shapes = self.frontlabel_set.filter(
            checked=False).values_list('shape', flat=True)
        return [Shapes(shape).label for shape in missing_shapes]

    @property
    def missing_back_labels(self):
        missing_shapes = self.backlabel_set.filter(
            checked=False).values_list('shape', flat=True)
        return [Shapes(shape).label for shape in missing_shapes]

    @property
    def missing_front_labels_count(self):
        return self.frontlabel_set.filter(checked=False).count()

    @property
    def missing_back_labels_count(self):
        return self.backlabel_set.filter(checked=False).count()


class FrontLabel(LabelValidationMixin, models.Model):
    creator = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True, default=None,
                                related_name="front_labels")
    trolley = models.ForeignKey(Trolley, on_delete=models.CASCADE)
    shape = models.IntegerField(choices=Shapes.choices, default=Shapes.SQUARE)
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"A front, {self.get_shape_display()} label, linked to trolley "
            f"number: {self.trolley.id} | Created at {self.created_at}"
        )

    def clean(self):
        super().clean()
        if self.trolley:
            self.validate_max_totes()
            self.validate_unique_shape()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class BackLabel(LabelValidationMixin, models.Model):
    creator = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True, default=None,
                                related_name="back_labels")
    trolley = models.ForeignKey(Trolley, on_delete=models.CASCADE)
    shape = models.IntegerField(choices=Shapes.choices, default=Shapes.SQUARE)
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"A back, {self.get_shape_display()} label, linked to trolley"
            f" number: {self.trolley.id} | Created at {self.created_at}"
            )

    def clean(self):
        super().clean()
        if self.trolley:
            self.validate_max_totes()
            self.validate_unique_shape()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
