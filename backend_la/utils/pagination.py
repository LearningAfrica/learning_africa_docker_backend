from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class DefaultPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'
    page_query_param = 'page'
    max_page_size = 100

    def get_paginated_response(self, data):
        next_page_number = self.page.next_page_number() if self.page.has_next() else None
        prev_page_number = self.page.previous_page_number() if self.page.has_previous() else None

        return Response({
            'meta': {
                'totalDocs': self.page.paginator.count,
                'totalPages': self.page.paginator.num_pages,
                'page': self.page.number,
                'limit': self.page_size,
                'hasNextPage': self.page.has_next(),
                'hasPrevPage': self.page.has_previous(),
                'nextPage': next_page_number,
                'prevPage': prev_page_number,
            },
            'data': data
        })