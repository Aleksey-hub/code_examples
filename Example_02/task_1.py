# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с сайта HH.
# Приложение должно анализировать несколько страниц сайта.
# Получившийся список должен содержать в себе минимум:
#  - Наименование вакансии.
#  - Предлагаемую зарплату (отдельно минимальную и максимальную).
#  - Ссылку на саму вакансию.
#  - Сайт, откуда собрана вакансия.
# Сохраните в json либо csv.
import json
import re

import requests
from bs4 import BeautifulSoup

required_vacancy = input('Введите интересующую вас должность: ')  # для получения task_1.json было введено: 'python разработчик'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36'
}
params = {
    'clusters': 'true',
    'area': 3,
    'enable_snippets': 'true',
    'st': 'searchVacancy',
    'text': required_vacancy,
    'page': 0
}
url = 'https://ekaterinburg.hh.ru/'

vacancies = []
while True:
    response = requests.get(url + 'search/vacancy/', params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    vacancy_list = soup.find_all(attrs={'class': 'vacancy-serp-item'})

    for vacancy in vacancy_list:
        vacancy_data = {}

        a = vacancy.find('a', attrs={'class': 'bloko-link'})
        link = a.get('href')
        name_vacancy = a.getText()

        salary = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})

        if salary:
            salary = salary.getText()
            if salary.find('до') != -1:
                salary_min = None
                salary_max = int(re.sub(r'до\s(\d+)\s(\d+)\s+(\w+\.?\w*)', r'\1\2', salary))
                salary_currency = re.sub(r'до\s(\d+)\s(\d+)\s+(\w+\.?\w*)', r'\3', salary)
            elif salary.find('от') != -1:
                salary_min = int(re.sub(r'от\s(\d+)\s(\d+)\s+(\w+\.?\w*)', r'\1\2', salary))
                salary_max = None
                salary_currency = re.sub(r'от\s(\d+)\s(\d+)\s+(\w+\.?\w*)', r'\3', salary)
            else:
                salary_min = int(re.sub(r'(\d+)\s(\d+)\D+(\d+)\s(\d+)\s+(\w+\.?\w*)', r'\1\2', salary))
                salary_max = int(re.sub(r'(\d+)\s(\d+)\D+(\d+)\s(\d+)\s+(\w+\.?\w*)', r'\3\4', salary))
                salary_currency = re.sub(r'(\d+)\s(\d+)\D+(\d+)\s(\d+)\s+(\w+\.?\w*)', r'\5', salary)
        else:
            salary_min, salary_max, salary_currency = None, None, None

        vacancy_data['name_vacancy'] = name_vacancy  # Наименование вакансии
        vacancy_data['salary_min'] = salary_min  # Минимальная предлагаемая зарплата
        vacancy_data['salary_max'] = salary_max  # Максимальная предлагаемая зарплата
        vacancy_data['salary_currency'] = salary_currency  # Валюта зарплаты
        vacancy_data['link'] = link  # Ссылка на вакансию
        vacancy_data['website'] = url  # Сайт, откуда собрана вакансия

        vacancies.append(vacancy_data)

    # Проверяем наличие кнопки "дальше"
    button_next = soup.find('span', attrs={'class': 'bloko-form-spacer'}, text='дальше')
    if button_next:
        params['page'] += 1
    else:
        break

with open('task_1.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies, f, ensure_ascii=False)
