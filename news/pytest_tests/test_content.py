import pytest

from pytest_lazy_fixtures import lf
from django.conf import settings
from django.urls import reverse

from news.models import News, Comment

@pytest.mark.django_db
def test_news_count(all_news, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(all_news, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_order(client, all_comments, news_id_for_args):
    url = reverse('news:detail', args=news_id_for_args)
    response = client.get(url)
    news = response.context['news']
    all_comment = news.comment_set.all()
    all_timestmps = [comment.created for comment in all_comment]
    sorted_timestmps = sorted(all_timestmps)
    assert all_timestmps == sorted_timestmps


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, form_in_list',
    (
        (lf('author_client'), True),
        (lf('client'), False),
    )
)
def test_anonymous_client_has_no_form(
    parametrized_client, form_in_list, news_id_for_args
):
    url = reverse('news:detail', args=news_id_for_args)
    response = parametrized_client.get(url)
    assert ('form' in response.context) is form_in_list

