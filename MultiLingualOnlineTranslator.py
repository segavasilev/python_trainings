from urllib.parse import urljoin
import requests
import bs4
import sys

LANGUAGES = [
        'arabic',
        'german',
        'english',
        'spanish',
        'french',
        'hebrew',
        'japanese',
        'dutch',
        'polish',
        'portuguese',
        'romanian',
        'russian',
        'turkish'
    ]


class OnlineTranslator:

    def __init__(self, sys_input=None):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.link = 'https://context.reverso.net/translation/'
        self.languages = LANGUAGES
        self.mode = 'a'
        self.id = 1
        self.sys_input = sys_input
        self.src = self.sys_input[0].lower()
        self.tar = self.sys_input[1].lower()
        self.word = self.sys_input[2].lower()
        self.direction_list = None
        self.response = None
        self.input_check()

    def input_check(self):
        while True:
            if self.src in LANGUAGES and (self.tar in LANGUAGES or self.tar == 'all'):
                self.parse_input()
                break
            elif self.src not in LANGUAGES:
                print(f"Sorry, the program doesn't support {self.src}")
                break
            elif self.tar not in LANGUAGES:
                print(f"Sorry, the program doesn't support {self.tar}")
                break


    def parse_input(self):
        if self.tar != 'all':
            self.direction_list = [f'{self.src}-{self.tar}']
        else:
            target_languages = [i for i in LANGUAGES if i != self.src]
            self.direction_list = [f'{self.src}-{target}' for target in target_languages]
        self.request()


    def request(self):
        session = requests.Session()
        for lang_pair in self.direction_list:
            link = urljoin(self.link, '{}'.format('/'.join([lang_pair, self.word])))
            self.response = session.get(link, headers=self.headers)
            try:
                if self.response.status_code == 200:
                    self.output(*self.washing(), lang_src=lang_pair.split('-')[0], lang_tar=lang_pair.split('-')[1])
                elif self.response.status_code == 404:
                    print(f'Sorry, unable to find {self.word}.')
            except:
                print('Something wrong with your internet connection.')


    def washing(self):
        translation_examples = []
        soup = bs4.BeautifulSoup(self.response.text, 'html.parser')
        translation_words = [i.text.strip() for i in
                                 soup.find("div", {"id": "translations-content"}).find_all("a")]
        for item in soup.find_all(class_='example'):
            try:
                src = item.find(class_='src ltr').find(class_='text').text.strip()
            except:
                try:
                    src = item.find(class_='src rtl arabic').find(class_='text').text.strip()
                except:
                    try:
                        src = item.find(class_='src rtl').find(class_='text').text.strip()
                    except:
                        pass
            try:
                tar = item.find(class_='trg ltr').find(class_='text').text.strip()
            except:
                try:
                    tar = item.find(class_='trg rtl arabic').find(class_='text').text.strip()
                except:
                    try:
                        tar = item.find(class_='trg rtl').find(class_='text').text.strip()
                    except:
                        pass
            translation_examples.append('\n'.join([src, tar]))
        return translation_words, translation_examples

    def output(self, translation_words, translation_examples, lang_src, lang_tar):
        with open(f'{self.word}.txt', self.mode, encoding="utf-8") as file:
            if self.id < len(LANGUAGES):
                print(
                    f'{lang_tar.capitalize()} Translations\n{translation_words[0]}\n\n{lang_tar.capitalize()} Examples\n{translation_examples[0]}\n\n')
                file.write(
                    f'{lang_tar.capitalize()} Translations\n{translation_words[0]}\n\n{lang_tar.capitalize()} Examples\n{translation_examples[0]}\n\n\n')
            else:
                print(
                    f'{lang_tar.capitalize()} Translations\n{translation_words[0]}\n\n{lang_tar.capitalize()} Examples\n{translation_examples[0]}')
                file.write(
                    f'{lang_tar.capitalize()} Translations\n{translation_words[0]}\n\n{lang_tar.capitalize()} Examples\n{translation_examples[0]}')
        self.id += 1


if __name__ == '__main__':
    #print('Hello, welcome to the translator. Translator supports:')
    #[print(num, '->', value) for num, value in enumerate(OnlineTranslator.lang, start=1)]
    args = sys.argv[1:]
    run = OnlineTranslator(args)