from rest_framework.pagination import PageNumberPagination as _PageNumberPagination


class PageNumberPagination(_PageNumberPagination):
    page_query_param = 'page'
    page_query_description = "当前的页数，默认为1"
    page_size_query_param = 'page_size'
    page_size_query_description = "当前页面的数据量，默认10条"
    page_size = 10
