from django.test import TestCase
from django.db import IntegrityError
import math
from animals.models import Animal
from groups.models import Group
from traits.models import Trait


class AnimalTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.gato_group = {"name": "gato", "scientific_name": "Felis catus"}
        cls.gato_animal = {"name": "lolinha", "age": 5, "weight": 3, "sex": "Femea"}
        cls.gato_traits = {"name": "peludo"}

        cls.gatoGroup = Group.objects.create(**cls.gato_group)
        cls.gatoAnimal = Animal.objects.create(**cls.gato_animal, group=cls.gatoGroup)
        cls.gatoTraits = Trait.objects.create(**cls.gato_traits)

    def testing_dog_age_to_human_years(self):
        "verify dog age to humans"
        expected = 57
        result = self.gatoAnimal.convert_dog_age_to_human_years()

        self.assertEqual(expected, result)

    def testing_max_length(self):
        "verify max_length, the words"
        expected_animal_name = 50
        expected_animal_sex = 15
        expected_group_name = 20
        expected_group_sc_name = 50
        expected_trait_name = 20

        result_animal_name = Animal._meta.get_field("name").max_length
        result_animal_sex = Animal._meta.get_field("sex").max_length
        result_group_name = Group._meta.get_field("name").max_length
        result_group_sc = Group._meta.get_field("scientific_name").max_length
        result_trait = Trait._meta.get_field("name").max_length

        self.assertEqual(expected_animal_name, result_animal_name)
        self.assertEqual(expected_animal_sex, result_animal_sex)
        self.assertEqual(expected_group_name, result_group_name)
        self.assertEqual(expected_group_sc_name, result_group_sc)
        self.assertEqual(expected_trait_name, result_trait)

    def testing_unique_cases_group(self):
        "testing unique cases"

        message_group = "UNIQUE constraint failed: groups_group.scientific_name"

        with self.assertRaisesMessage(IntegrityError, message_group):
            Group.objects.create(**self.gato_group)

    def testing_unique_cases_trait(self):
        "testing unique cases"

        message_traits = "UNIQUE constraint failed: traits_trait.name"

        with self.assertRaisesMessage(IntegrityError, message_traits):
            Trait.objects.create(**self.gato_traits)