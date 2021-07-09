# Everyone’s familiar with online translators. They giving us a handy way to
# translate on the go. In this project, you’re about to write an app that translates
# the words you type and gives you many usage examples based on the context.

import requests
import sys
from bs4 import BeautifulSoup

from fake_useragent import UserAgent


class Translator:
    ua = UserAgent(cache=False)
    headers = {'User-Agent': ua.chrome}

    def __init__(self):
        self.menu = {'1': 'Arabic', '2': 'German', '3': 'English',
                     '4': 'Spanish', '5': 'French', '6': 'Hebrew',
                     '7': 'Japanese', '8': 'Dutch', '9': 'Polish',
                     '10': 'Portuguese', '11': 'Romanian',
                     '12': 'Russian', '13': 'Turkish', '0': 'All'}

    def welcome(self):
        print('Hello, you\'re welcome to the translator. Translator supports:')
        for key, value in self.menu.items():
            print(key, value, sep='. ')

        from_lang = input('Type the number of your language:\n')
        to_lang = input('Type the number of language you want to translate to:\n')
        word = input('Type the word you want to translate:\n')
        self.translate(self.menu.get(from_lang, '3'), self.menu.get(to_lang, '0'), word)

    def translate(self, from_lang, to_lang, word):
        try:
            message = ''
            if to_lang.lower() != 'all':
                message = self.__get_message(*self.__get_translate(from_lang, to_lang, word))
            else:
                for lang in self.menu.values():
                    if lang.lower() not in [from_lang.lower(), 'all']:
                        message += self.__get_message(*self.__get_translate(from_lang, lang, word, limit=1))
            print(message)
            with open(f'{word.lower()}.txt', 'w', encoding='utf-8') as f:
                f.write(message)
        except TypeError:
            print('Sorry, unable to find brrrrrrrrrrr')

    @staticmethod
    def __get_message(words=None, examples=None, to_lang=None):  # TODO *args
        if words is None or examples is None or to_lang is None:
            return None
        else:
            message = f'{to_lang.title()} Translations:\n'
            message += '\n'.join(words)
            message += f'\n\n{to_lang.title()} Examples:\n'
            for example in examples:
                message += f'{example[0]}\n{example[1]}\n\n'

            return message

    def __get_translate(self, from_lang, to_lang, word, limit=None):
        try:
            href = f'https://context.reverso.net/translation/{from_lang.lower()}-{to_lang.lower()}/{word.lower()}'
            soup = BeautifulSoup(requests.get(href, headers=self.headers).content, 'html.parser')

            raw_words = soup.find("div", {"id": "translations-content"}).find_all('a', {'class': 'translation'},
                                                                                  limit=limit)
            words = [word.text.strip() for word in raw_words]

            raw_examples = soup.find('section', {'id': 'examples-content'}).find_all('div', {'class': 'example'},
                                                                                     limit=limit)
            examples = [[texts.text.strip() for texts in example.find_all('span', {'class': 'text'})] for example in
                        raw_examples]
            return words, examples, to_lang
        except ConnectionError:
            print('Something wrong with your internet connection')
        except AttributeError:
            print('Sorry, the program doesn\'t support korean')


if __name__ == '__main__':
    trans = Translator()
    if len(sys.argv) == 4:
        trans.translate(*sys.argv[1:])
    else:
        trans.welcome()
