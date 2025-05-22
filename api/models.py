from django.core.exceptions import ValidationError
from django.db import models

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
    id = models.AutoField(primary_key=True)
    totes_count = models.IntegerField(choices=Count.choices, default=Count.EIGHT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(max_length=200)
    in_use = models.BooleanField(default=True)

    def __str__(self):
        return f"Trolley number {self.id}"

class FrontLabel(models.Model):
    trolley = models.ForeignKey(Trolley, on_delete=models.CASCADE)
    shape = models.IntegerField(choices=Shapes.choices, default=Shapes.SQUARE)
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"A back, {self.get_shape_display()} label, linked to trolley number: {self.trolley.id} | Created at {self.created_at}"

    def clean(self):
        if self.trolley and not self.pk:  # Only validate on creation
            count = FrontLabel.objects.filter(trolley=self.trolley).count()
            if self.trolley.totes_count == 1 and count >= 8:
                raise ValidationError(("Small trolleys cannot have more than 8 totes."))
            elif self.trolley.totes_count != 1 and count >= 10:
                raise ValidationError(("Big trolleys cannot have more than 10 totes."))
            
        
        # Check if this shape is already used for the same trolley
        if FrontLabel.objects.filter(trolley=self.trolley, shape=self.shape).exists():
            shape_name = Shapes(self.shape).label  # Get display name like "Square"
            raise ValidationError((f"The shape '{shape_name}' is already assigned to this trolley."))

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure clean() is called before saving
        super().save(*args, **kwargs)


class BackLabel(models.Model):
    trolley = models.ForeignKey(Trolley, on_delete=models.CASCADE)
    shape = models.IntegerField(choices=Shapes.choices, default=Shapes.SQUARE)
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"A back, {self.get_shape_display()} label, linked to trolley number: {self.trolley.id} | Created at {self.created_at}"

    def clean(self):
        if self.trolley and not self.pk:  # Only validate on creation
            count = BackLabel.objects.filter(trolley=self.trolley).count()
            if self.trolley.totes_count == 1 and count >= 8:
                raise ValidationError(("Small trolleys cannot have more than 8 totes."))
            elif self.trolley.totes_count != 1 and count >= 10:
                raise ValidationError(("Big trolleys cannot have more than 10 totes."))
            
        
        # Check if this shape is already used for the same trolley
        if BackLabel.objects.filter(trolley=self.trolley, shape=self.shape).exists():
            shape_name = Shapes(self.shape).label  # Get display name like "Square"
            raise ValidationError((f"The shape '{shape_name}' is already assigned to this trolley."))

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure clean() is called before saving
        super().save(*args, **kwargs)