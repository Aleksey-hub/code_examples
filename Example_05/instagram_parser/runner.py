'''
1) Написать приложение, которое будет проходиться по указанному списку двух и/или более пользователей и
    собирать данные об их подписчиках и подписках.
2) По каждому пользователю, который является подписчиком или на которого подписан исследуемый объект нужно извлечь имя,
    id, фото (остальные данные по желанию). Фото можно дополнительно скачать.
3) Собранные данные необходимо сложить в базу данных. Структуру данных нужно заранее продумать, чтобы:
4) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь
'''

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instagram_parser import settings
from instagram_parser.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    scrapy_settings = Settings()
    scrapy_settings.setmodule(settings)

    process = CrawlerProcess(settings=scrapy_settings)
    # Список пользователей у которых собираются данные об их подписчиках и подписках
    users = ['prostonadezhda1', 'teh_remo_61']
    process.crawl(InstagramSpider, users=users)

    process.start()
