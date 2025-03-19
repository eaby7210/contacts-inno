from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Contact
from .serializers import ContactSerializer

# Create your views here.

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
    search_fields = ["first_name", "last_name", "email"]