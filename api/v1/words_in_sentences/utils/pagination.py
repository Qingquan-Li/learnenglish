# https://www.django-rest-framework.org/api-guide/pagination/

from rest_framework import pagination


class CustomSentencePagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
    # page_query_param = 'page'  # default

    # def get_paginated_response(self, data):
    #     return Response(OrderedDict([
    #         ('count', self.page.paginator.count),
    #         ('next', self.get_next_link()),
    #         ('previous', self.get_previous_link()),
    #         ('results', data)
    #     ]))
    # Override get_paginated_response:
    # www.django-rest-framework.org/api-guide/pagination/#custom-pagination-styles
    # from rest_framework.response import Response
    # def get_paginated_response(self, data):
    #     return Response(
    #         data
    #     )


class CustomTagPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 1000
    # page_query_param = 'page'  # default
