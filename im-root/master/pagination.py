from rest_framework.pagination import PageNumberPagination

class SmallsetPagination(PageNumberPagination):
    page_size = 3


class BigsetPagination(PageNumberPagination):
    page_size = 10

