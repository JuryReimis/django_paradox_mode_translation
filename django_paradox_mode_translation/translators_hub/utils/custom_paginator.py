from django.core.paginator import Paginator, Page


class CustomPaginator(Paginator):
    custom_href = None

    def __init__(self, *args, **kwargs):
        super(CustomPaginator, self).__init__(*args, **kwargs)

    def _get_page(self, *args, **kwargs):
        return CustomPage(*args, **kwargs)

    def get_custom_immutable_href(self):
        return self.custom_href

    def set_custom_immutable_href(self, href_name_value: tuple):
        self.custom_href = "&".join(map(lambda name_value: f"{name_value[0]}={name_value[1]}", href_name_value))

    def get_page_number_href(self, page_number):
        if self.custom_href:
            return f"?page={page_number}&{self.custom_href}"
        else:
            return f"?page={page_number}"

    def get_page_range_with_custom_href(self) -> list:
        if self.custom_href:
            final_range = [(i, f"?page={i}&{self.custom_href}") for i in self.page_range]
        else:
            final_range = [(i, f"?page={i}") for i in self.page_range]
        return final_range

    def get_next_page_number(self):
        return self.num_pages


class CustomPage(Page):

    def __init__(self, *args, **kwargs):
        super(CustomPage, self).__init__(*args, **kwargs)

    def get_next_page_custom_href(self) -> str:
        return self.paginator.get_page_number_href(self.next_page_number())

    def get_previous_page_custom_href(self) -> str:
        return self.paginator.get_page_number_href(self.previous_page_number())





