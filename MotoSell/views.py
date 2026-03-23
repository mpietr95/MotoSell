from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Vehicle
from .serializers import VehicleSerializer


# a. Wszystkie opublikowane oferty — dostęp publiczny
class VehicleListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        vehicles = Vehicle.objects.filter(
            published_at__isnull=False,
            is_deleted=False,
        )
        serializer = VehicleSerializer(vehicles, many=True, context={'request': request})
        return Response(serializer.data)

    # c. Dodanie nowej oferty
    def post(self, request):
        serializer = VehicleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# b. Oferty zalogowanego użytkownika — dostęp prywatny
class MyVehicleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vehicles = Vehicle.objects.filter(
            user=request.user,
            is_deleted=False,
        )
        serializer = VehicleSerializer(vehicles, many=True, context={'request': request})
        return Response(serializer.data)


# d. Edycja oferty — tylko właściciel
class VehicleEditView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_vehicle(self, pk, user):
        try:
            vehicle = Vehicle.objects.get(pk=pk, is_deleted=False)
        except Vehicle.DoesNotExist:
            return None, Response({'detail': 'Nie znaleziono oferty.'}, status=status.HTTP_404_NOT_FOUND)
        if vehicle.user != user:
            return None, Response({'detail': 'Brak uprawnień.'}, status=status.HTTP_403_FORBIDDEN)
        return vehicle, None

    def put(self, request, pk):
        vehicle, error = self.get_vehicle(pk, request.user)
        if error:
            return error
        serializer = VehicleSerializer(vehicle, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        vehicle, error = self.get_vehicle(pk, request.user)
        if error:
            return error
        serializer = VehicleSerializer(vehicle, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# e. Publikacja oferty — tylko właściciel
class VehiclePublishView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk, is_deleted=False)
        except Vehicle.DoesNotExist:
            return Response({'detail': 'Nie znaleziono oferty.'}, status=status.HTTP_404_NOT_FOUND)
        if vehicle.user != request.user:
            return Response({'detail': 'Brak uprawnień.'}, status=status.HTTP_403_FORBIDDEN)
        vehicle.published_at = timezone.now().date()
        vehicle.save()
        serializer = VehicleSerializer(vehicle, context={'request': request})
        return Response(serializer.data)


# f. Miękkie usunięcie oferty — tylko właściciel
class VehicleDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk, is_deleted=False)
        except Vehicle.DoesNotExist:
            return Response({'detail': 'Nie znaleziono oferty.'}, status=status.HTTP_404_NOT_FOUND)
        if vehicle.user != request.user:
            return Response({'detail': 'Brak uprawnień.'}, status=status.HTTP_403_FORBIDDEN)
        vehicle.is_deleted = True
        vehicle.save()
        return Response({'detail': 'Oferta została usunięta.'}, status=status.HTTP_200_OK)
