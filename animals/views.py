from rest_framework.views import APIView, Response, status, Request
from animals.exceptions import NoUpdate

from animals.models import Animal
from .serializers import AnimalSerializer
from django.shortcuts import get_object_or_404


class AnimalView(APIView):
    def post(self, request: Request) -> Response:
        serializer = AnimalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        animal = Animal.objects.all()
        serializer = AnimalSerializer(animal, many=True)
        return Response(serializer.data)


class AnimalDetailsView(APIView):
    def get(self, request: Request, animal_id: int) -> Response:

        animal = get_object_or_404(Animal, id=animal_id)
        serializer = AnimalSerializer(animal)
        return Response(serializer.data)

    def patch(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        serializer = AnimalSerializer(animal, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except NoUpdate as errors:
            return Response(
                errors.args[0],
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return Response(serializer.data)

    def delete(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        animal.delete()
        return Response(status.HTTP_204_NO_CONTENT)