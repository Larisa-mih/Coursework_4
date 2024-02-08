import json
from abc import abstractmethod


class FileManager:
    """Класс для работы с файлами"""

    @abstractmethod
    def get_vacancies_by_keyword(self, keyword):
        """Функция чтения из файла"""
        pass

    @abstractmethod
    def write_file(self, vacancies):
        """Функция записи в файл"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancies):
        """Функция удаления из файла"""
        pass

    @abstractmethod
    def get_list_vacancies(self):
        """Функция получения списка вакансий"""
        pass


class JsonFileManager(FileManager):
    """Класс для работы с файлами формата json"""

    def __init__(self, filename):
        self.filename = filename

    def write_file(self, vacancies):
        """
        Функция записи в файл.
        :param vacancies: Список объектов класса Vacancy
        :return: None
        """
        data = self.data_to_json(vacancies)
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))

    @staticmethod
    def data_to_json(vacancies):
        """
        Распаковывает список объектов класса Vacancy и записывает в новый
        :param vacancies: список объектов класса Vacancy
        :return: vacancies_list: список словарей с вакансиями в нужном формате
        """
        vacancies_list = []
        for vacancy in vacancies:
            vacancy_dict = {
                'name_vacancy': vacancy.name_vacancy,
                'url': vacancy.url,
                'requirements': vacancy.requirements,
                'employer': vacancy.employer,
                'city': vacancy.city,
                'salary_from': vacancy.salary_from,
                'salary_to': vacancy.salary_to
            }

            vacancies_list.append(vacancy_dict)
        return vacancies_list

    def get_list_vacancies(self):
        """Функция получения списка вакансии"""
        with open(self.filename, 'r', encoding='utf-8') as f:
            data_for_filter = f.read()
        data = json.loads(data_for_filter)
        return data

    def get_vacancies_by_keyword(self, keyword: dict):
        """
         Метод получения вакансий из файла по ключевому слову.
        :param keyword: Словарь с ключевыми словами для поиска
        :return list_of_vacancies: список вакансий, выбранных по ключевым словам
        """
        with open(self.filename, 'r', encoding='utf-8') as f:
            data_for_filter = f.read()
        data = json.loads(data_for_filter)
        list_of_vacancies = []
        for vacancy in data:
            for key, value in keyword.items():
                if key == 'salary_input':
                    try:
                        int(vacancy['salary_from']) >= value
                    except TypeError:
                        continue
                    else:
                        list_of_vacancies.append(vacancy)
                else:
                    break
        return list_of_vacancies

    def delete_vacancy(self, vacancies):
        """
           Функция удаления из файла.
           :param vacancies: Список объектов класса Vacancy
           :return: None
           """
        with open(self.filename, 'r', encoding='utf-8') as f:
            file_data = f.read()
            data = json.loads(file_data)
        for vacancy in data:
            if vacancy in vacancies:
                data.remove(vacancy)
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))
