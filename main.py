import requests
from bs4 import BeautifulSoup
import json


class MyParser:
    def __init__(self):
        # в конструкторе класса прописываю переменные, которые собираюсь использовать в методах
        self.json_url = "https://salomon.ru/catalog/muzhchiny/obuv/filter/available-is-y/" \
                        "size-is-10.5%20uk/apply/?PAGEN_1=1"
        self.url = "https://salomon.ru/catalog/muzhchiny/obuv/"
        self.json_url = "https://salomon.ru/catalog/muzhchiny/obuv/?PAGEN_1=2"
        self.base_url = "https://salomon.ru"
        # список заголовков для передачи в метод гет библиотеки requests
        # bx-ajax фича 1С
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                      "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36",
            "bx-ajax": "true"
        }

   #def get_page(self, url):
        # получаю страницу, которую хочу спарсить и сохраняю ее в офлайн документ
       # response = requests.get(url, headers=self.headers)  # Get response, sending arguments

       # with open("index.html", "w", encoding="utf-8") as file:
       #     file.write(response.text)

    def save_json(self, url):
        # запускаю новую сессию и далее получаю JSON файл
        # который зписываю для просмотра через онлайн JSON вьюер
        s = requests.Session()  # Create new session
        response = s.get(url, headers=self.headers)  # Get response, sending arguments

        with open("result.json", "w", encoding="utf-8") as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)

    def collect_data(self):
        # тут я получаю пагинацию посредством поиска в консоли разработчика браузера
        # информации о запросе к странице пагинации и так как это ссылка на JSON файл, а это словарь для
        # Python, то я обращаюсь к ключам в файле, чтобы узнать точное количество страниц
        # с товарами, чтобы переходить по всем страницам используя цикл for для генерации ссылок
        s = requests.Session()
        response = requests.get(self.json_url, headers=self.headers)
        data = response.json()
        pagination_count = data.get("pagination").get("pageCount")
        # в список записываю словари со спаршенными данными, но сайт кривой и на нем есть дубли карточек товаров
        # а это значит, что мы парсим дубли, чтобы это исправить напишем небольшой фильтр дублей
        result_data = []

        # список для работы с дублирующимися данными
        items_urls = []

        for page_count in range(1, pagination_count + 1):
            # записываю сюда ссылку куда буду поставлять номера страниц для перехода по ним
            url = f"https://salomon.ru/catalog/muzhchiny/obuv/filter/available-is-y/" \
                  f"size-is-10.5%20uk/apply/?PAGEN_1={page_count}"
            r = s.get(url=url, headers=self.headers)
            data = r.json()
            products = data.get("products")

            # так я вижу сколько страниц будем парсить и на какой странице мы сейчас.
            print(f"{page_count}/{pagination_count}")

            for product in products:
                product_colors = product.get("colors")
                # цикле ниже получаем из json файла информацию по продуктам, обращаясь к каждому ключу в словаре
                for pc in product_colors:
                    discount_percent = pc.get("price").get("discountPercent")
                    product_url = self.base_url + pc.get("link")
                    color_name = pc.get("color").get("title")

                    # записываем данные проверяя если есть на товар скидка и если его уже нет в списке
                    if discount_percent != 0 and pc.get("link") not in items_urls:
                        items_urls.append(pc.get("link"))
                        result_data.append({
                            "title": pc.get("title"),
                            "link": product_url,
                            "price": pc.get("price").get("base"),
                            "category": pc.get("category"),
                            "sale": pc.get("price").get("sale"),
                            "discount_percent": discount_percent,
                            "color_name": color_name
                        })
        with open("result_data.json", "w", encoding="utf-8") as file:
            json.dump(result_data, file, indent=4, ensure_ascii=False)

    def main(self):
      #  self.get_page(self.url)
        self.save_json(self.json_url)
        self.collect_data()


parser = MyParser()
parser.main()
