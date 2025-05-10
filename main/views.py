from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Property
from .serializers import PropertySerializer
from rest_framework.permissions import IsAuthenticated


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]
    lookup_field = 'pid'

    def perform_create(self, serializer):
        # Automatically set the user to the authenticated user
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='ongoing')
    def get_ongoing_properties(self, request):
        ongoing_properties = Property.objects.filter(action='Ongoing')
        serializer = self.get_serializer(ongoing_properties, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='sold')
    def get_sold_properties(self, request):
        sold_properties = Property.objects.filter(action='Sold')
        serializer = self.get_serializer(sold_properties, many=True)
        return Response(serializer.data)