from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Contact, WebhookLog
from .serializers import ContactSerializer
import logging

# Create your views here.
logger = logging.getLogger(__name__)
class ContactPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = "page_size"
    max_page_size = 50  # Limit max page size

# Contact ViewSet
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    pagination_class = ContactPagination  

    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name", "email","id"]





from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ContactWebhookView(APIView):
    """
    Handles incoming webhook events from GoHighLevel.
    """

    def post(self, request):
        """
        Process webhook events.
        """
        print("sdfadf")
        payload = request.data
        webhook_id = payload.get("webhookId")
        event_type = payload.get("type")
        contact_data = {
            "id":payload.get("id"),
            "firstName":payload.get("firstName",""),
            "lastName":payload.get("lastName",""),
            "email":payload.get("email"),
            "phone":payload.get("phone",""),
            
            }

        if WebhookLog.objects.filter(webhook_id=webhook_id).exists():
            return Response({"error": "Duplicate webhook detected"}, status=status.HTTP_409_CONFLICT)
        
        # Log webhook
        WebhookLog.objects.create(webhook_id=webhook_id, received_at=now())

        print(f"webhook: {webhook_id} \npayload",contact_data,event_type)
        # Process events
        if event_type == "ContactCreate":
            self.create_contact(contact_data)
        elif event_type == "ContactDelete":
            self.delete_contact(contact_data)
        elif event_type == "ContactUpdate":
            self.update_contact(contact_data)
        elif event_type == "ContactDndUpdate":
            self.update_contact_dnd(contact_data)
        elif event_type == "ContactTagUpdate":
            self.update_contact_tags(contact_data)
        # elif event_type == "NoteCreate":
        #     self.create_note(contact_data)
        # elif event_type == "NoteDelete":
        #     self.delete_note(contact_data)
        # elif event_type == "TaskCreate":
        #     self.create_task(contact_data)
        # elif event_type == "TaskDelete":
        #     self.delete_task(contact_data)

        return Response({"message": "Webhook processed successfully"}, status=status.HTTP_200_OK)

    def create_contact(self, data):
        """ Creates a new contact """
        Contact.objects.create(
            id=data["id"],
            first_name=data.get("firstName", ""),
            last_name=data.get("lastName", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
        )
    
    def update_contact(self, data):
        """ Updates a contact """
        contact = Contact.objects.filter(id=data["id"]).first()
        if contact:
            contact.first_name = data.get("firstName", contact.first_name)
            contact.last_name = data.get("lastName", contact.last_name)
            contact.email = data.get("email", contact.email)
            contact.phone = data.get("phone", contact.phone)
            contact.save()
            logger.info(f"Updated contact: {data['id']}")
        else:
            logger.warning(f"Contact {data['id']} not found for update")

    def delete_contact(self, data):
        """ Deletes a contact """
        Contact.objects.filter(id=data["id"]).delete()
