from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "country",
            "location_id",
            "type",
            "date_added",
            "date_updated",
            "dnd",
        ]