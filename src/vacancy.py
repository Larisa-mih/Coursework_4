class Vacancy:
    def __init__(self, name_vacancy, url, requirements, employer, city, salary_from, salary_to):
        self.name_vacancy = name_vacancy
        self.url = url
        self.requirements = requirements
        self.employer = employer
        self.city = city
        self.salary_from = salary_from
        self.salary_to = salary_to

    def __str__(self):
        return f'{self.name_vacancy}\n{self.employer}'

    def __ge__(self, other):
        return self.salary_from >= other.salary_from

    def __le__(self, other):
        return self.salary_from <= other.salary_from

    def validate_data(self):
        """Функция для валидации данных"""
        if self.name_vacancy is None:
            self.name_vacancy = ' '
        elif self.url is None:
            self.url = ' '
        elif self.requirements is None:
            self.requirements = ' '
        elif self.employer is None:
            self.employer = ' '
        elif self.city is None:
            self.city = ' '
        elif self.salary_from is None or self.salary_from == 'null':
            self.salary_from = 0
        elif self.salary_to is None or self.salary_from == 'null':
            self.salary_to = 0
