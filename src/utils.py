from src.api import HeadHunterApi, SuperJobApi
from src.data import JsonFileManager


def choose_platform():
    """
    Функция для выбора пользователем платформы для поиска вакансии.
    """
    print('Выберите платформу для поиска вакансии\n'
          '1 - HeadHunter\n'
          '2 - SuperJob\n'
          '3 - на всех платформах')


def choose_vacancy():
    """
    Функция для ввода пользователем названия вакансии для запроса.
    """
    return input('Введите вакансию для поиска ')


def get_vacancies(api_manager: list):
    """Функция для вывода списка вакансий по запросу с API"""
    vacancies = []
    for api in api_manager:
        vacancies.extend(api.format_data())
    return vacancies


def get_top_vacancies(file_manager, user_input_count):
    """
    Функция для получения вакансий, отсортированных по зарплате.
    """
    vacancy_list = file_manager.get_list_vacancies()
    try:
        sorted_vacancies = sorted(vacancy_list, key=lambda elem: elem['salary_from'], reverse=True)[:user_input_count]
    except TypeError:
        print('Часть вакансий указана без з/ты, выберите другой критерий поиска из предложенных вариантов')
    else:
        return sorted_vacancies


def actions_for_vacancies(file_manager):
    print('Выберете действие:\n'
          '1 - получить топ-N вакансий по зарплате\n'
          '2 - выборка вакансии по минимальному уровню заработной платы\n'
          '3 - удалить вакансию по указанному критерию\n'
          '0 - выйти'
          )
    while True:
        user_request = input()
        if user_request in ('1', '2', '3', '0'):
            if user_request == '1':
                user_input_count = int(input('Введите количество вакансий для вывода '))
                top_n = get_top_vacancies(file_manager, user_input_count)
                try:
                    for vac in top_n:
                        print(vac)
                except TypeError:
                    continue
                break
            elif user_request == '2':
                salary_input = int(input('Введите минимальную з/п '))
                min_salary = file_manager.get_vacancies_by_keyword({'salary_input': salary_input})
                for vac in min_salary:
                    print(vac)
                break
            elif user_request == '3':
                low_salary_input = int(input('Введите уровень з/п, ниже которой можно удалить вакансии из списка: '))
                file_manager.delete_vacancy(file_manager.get_vacancies_by_keyword({'salary_input': low_salary_input}))
                print(f'Вакансии удалены из файла по критерию {low_salary_input}')
                break
            elif user_request == '0':
                break
        else:
            print('Некорректный запрос, выберите другой')


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    keyword = choose_vacancy()
    choose_platform()
    while True:
        user_request = input()
        api_list = []
        if user_request in ('1', '2', '3'):
            if user_request == '1':
                hh = HeadHunterApi(keyword)
                api_list.append(hh)
                break
            elif user_request == '2':
                sj = SuperJobApi(keyword)
                api_list.append(sj)
                break
            elif user_request == '3':
                hh = HeadHunterApi(keyword)
                sj = SuperJobApi(keyword)
                api_list.append(hh)
                api_list.append(sj)
                break
        else:
            print('Некорректный запрос, выберите другой')


    file_manager = JsonFileManager('js_file_vacancies.json')
    file_manager.write_file(get_vacancies(api_list))
    actions_for_vacancies(file_manager)
