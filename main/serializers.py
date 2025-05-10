from rest_framework import serializers
from .models import Property, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    image_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    user = serializers.ReadOnlyField(source='user.username')
    action = serializers.ChoiceField(
        choices=Property.ACTION_CHOICES,
        default='Ongoing',
        required=False
    )

    class Meta:
        model = Property
        fields = [
            'pid', 'property_type', 'title', 'seller_name', 'phone_number',
            'email', 'street_address', 'city', 'state', 'price', 'size',
            'bedrooms', 'bathrooms', 'built_year', 'legal_document',
            'map', 'status', 'images', 'image_files', 'user', 'action',
            'created_date', 'transaction_date'
        ]

    def create(self, validated_data):
        image_files = validated_data.pop('image_files', [])
        # Set the user from the request context
        validated_data['user'] = self.context['request'].user
        property_instance = Property.objects.create(**validated_data)
        
        for image_file in image_files:
            PropertyImage.objects.create(property=property_instance, image=image_file)
        
        return property_instance

    def update(self, instance, validated_data):
        image_files = validated_data.pop('image_files', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if image_files:
            for image_file in image_files:
                PropertyImage.objects.create(property=instance, image=image_file)
        
        return instance