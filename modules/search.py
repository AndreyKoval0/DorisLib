import wikipedia
import requests
import random
from bs4 import BeautifulSoup
from .base import Module

wikipedia.set_lang('ru')

class Search(Module):

    @staticmethod
    def init_soup(link):
        doc = requests.get(link).text
        soup = BeautifulSoup(doc, "lxml")
        return soup

    def exec(self, service, question=''):
        if service == 'yandex':
            soup = self.init_soup("https://yandex.ru/search/?text=" + question)
            for pas in soup.find_all("div", {"class": "fact-answer typo typo_text_l typo_line_m fact__answer"}):
                return pas.text
        elif service == 'wiki':
            return wikipedia.page(wikipedia.search(question)[0]).content.split("\n")[0]
        elif service == 'news':
            if question == None:
                soup = self.init_soup("https://yandex.ru/news/")
                news = []
                for pas in soup.find_all('article', {'class': 'mg-card news-card news-card_double news-card_type_image mg-grid__item mg-grid__item_type_card'}):
                    news.append(f"{pas.find('h2', {'class': 'news-card__title'}).text}. {pas.find('div', {'class': 'news-card__annotation'}).text}")
                return random.choice(news)
            soup = self.init_soup(f"https://ria.ru/search/?query={question.split('.')[0]}")
            news_link = soup.find('a', {'class': 'list-item__title color-font-hover-only'})
            if news_link != None:
                news_link = news_link["href"]
                doc = requests.get(news_link).text
                soup = BeautifulSoup(doc, 'lxml')
                return soup.find('div', {'class': 'article__body js-mediator-article mia-analytics'}).text.split("\n\n\n\n")[0]
        return "Ошибка поиска"