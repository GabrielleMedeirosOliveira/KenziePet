from django.db import models
import math


class Options(models.TextChoices):
    macho = "Macho"
    femea = "Femea"
    other = "Não informado"


class Animal(models.Model):

    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=15, choices=Options.choices, default=Options.other
    )

    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="animals"
    )
    traits = models.ManyToManyField("traits.Trait", related_name="animals")

    def convert_dog_age_to_human_years(self):
        human_age = 16 * math.log(self.age) + 31
        return round(human_age)