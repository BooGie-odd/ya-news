from unittest import skip

from django.test import TestCase

from news.models import News



class TestNews(TestCase):

    TITLE = 'Заголовок новости'
    TEXT = 'Тестовый текст'

    @classmethod
    def setUpTestData(cls):
       cls.news = News.objects.create(
           title=cls.TITLE,
           text=cls.TEXT,
       )

    @skip('123')
    def test_succesful_creation(self):
        news_count = News.objects.count()
        self.assertEqual(news_count, 1)

    @skip('123')
    def test_title(self):
        self.assertEqual(self.news.title, self.TITLE)
