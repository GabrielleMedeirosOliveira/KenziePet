from tokenize import group
from rest_framework import serializers
from animals.exceptions import NoUpdate

from groups.models import Group
from traits.models import Trait
from .models import Animal, Options
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=Options.choices, default=Options.other)

    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    age_in_human_years = serializers.SerializerMethodField(
        method_name="convert_dog_age_to_human_years"
    )

    def convert_dog_age_to_human_years(self, obj: Animal):
        return obj.convert_dog_age_to_human_years()

    def create(self, validated_data):
        group_data = validated_data.pop("group")
        traits_data = validated_data.pop("traits")

        group_obj, _ = Group.objects.get_or_create(**group_data)
        animal_obj = Animal.objects.create(**validated_data, group=group_obj)

        for key in traits_data:
            traits_obj, _ = Trait.objects.get_or_create(**key)
            animal_obj.traits.add(traits_obj)

        return animal_obj

    def update(self, instance, validated_data):
        errors = {}
        for key, value in validated_data.items():
            if key == "sex" or key == "group" or key == "traits":
                errors[key] = f"{key}: You can not update {key} property."
                continue
            setattr(instance, key, value)

        if errors:
            raise NoUpdate(errors)

        instance.save()

        return instance