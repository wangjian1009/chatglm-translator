from typing import List
from .page import Page

class Book:
    pdf_file_path: str
    pages: List[Page]
    
    def __init__(self, pdf_file_path: str):
        self.pdf_file_path = pdf_file_path
        self.pages = []

    def add_page(self, page: Page):
        self.pages.append(page)
