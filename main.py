class Note:
    """Создание класса для инициализации и вывода записей телефонного справочника"""

    def __init__(self,
                 surname=None,
                 name=None,
                 patronymic=None,
                 organization=None,
                 office_number=None,
                 personal_number=None):
        """Инициализатор объекта класса Note, создаваемого на основе этого класса"""

        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.organization = organization
        self.office_number = office_number
        self.personal_number = personal_number

    def add(self):
        """Метод класса Note для определения значений атрибутов объекта класса"""

        all_parametrs = ''
        self.surname = input("Введите фамилию: ")
        all_parametrs += self.surname
        self.name = input("Введите имя: ")
        all_parametrs += self.name
        self.patronymic = input("Введите отчество: ")
        all_parametrs += self.patronymic
        self.organization = input("Введите название организации: ")
        all_parametrs += self.organization
        self.office_number = input("Введите рабочий телефон: ")
        all_parametrs += self.office_number
        self.personal_number = input("Введите личный телефон (сотовый): ")
        all_parametrs += self.personal_number
        if len(all_parametrs) == 0:  # Условие, исключающее создание пустой записи
            return 0

    def __str__(self):
        """Переопределение встроенного метода для возвращения строкового представления объекта класса"""

        return f'{self.surname}, ' \
               f'{self.name}, ' \
               f'{self.patronymic}, ' \
               f'{self.organization}, ' \
               f'{self.office_number}, ' \
               f'{self.personal_number}'


class Phonebook:
    """Создание класса для взаимодействия с телефонным справочником,
    наполненным объектами класса Note в строковом представлении"""

    def find_note(self, query: str):
        """Метод класса для поиска записей"""

        with open('Phonebook.txt', encoding='utf-8') as file:
            output_notes = []  # создание пустого списка для добавление всех записей, считанных из файла
            for line in file.readlines():
                # Создание объекта класса Note на основе его строкового представления
                note = Note(*line.strip("\n").split(', '))
                for i in query.split(','):
                    # Проверка на вхождение элемента запроса в значения атрибутов объекта класса Note
                    if i in note.__dict__.values():
                        output_notes.append(note)
            if len(output_notes) == 0:
                return ['\nПо вашему запросу записи не найдены!\n']
            return output_notes

    def show_pages(self):
        """Метод класса для постраничного отображения записей"""

        def options_for_show_pages():
            """Функция для пользовательского ввода значения выбора в диапазоне 1-3.
            Используется только в данном методе класса"""

            switch_options = None
            while switch_options not in [1, 2, 3]:
                try:
                    switch_options = int(input("\nВведите число для выбора действия ['1' - Следующая страница, "
                                               "'2' - Предыдущая страница, '3' - Выход в главное меню]: "))
                except ValueError:
                    print('', end='')
            return switch_options

        notes = []  # Создание пустого списка записей для добавления в него объектов класса Note
        with open('Phonebook.txt', encoding='utf-8') as file:
            for line in file.readlines():
                # Создание объекта класса Note на основе его строкового представления и его добавление к списку записей
                note = Note(*line.strip("\n").split(', '))
                notes.append(note)
            # Сортировка записей в лексикографическом порядке
            notes = sorted([str(note) for note in notes])
            notes = [Note(*str(note).split(', ')) for note in notes]
            # Создание вложенного списка страниц с первым элементом, представляющим собой список,
            # содержащий строковое отображение меню перелистывания страниц
            pages_notes = [[f"В телефонном справочнике {len(notes)} записи(ей).\n"
                            f"На одной странице отображается 10 записей.\n"
                            f"Для перелистывания вперёд введите '1'\n"
                            f"Для перелистывания назад введите '2'\n"
                            f"Для выхода в главное меню введите '3'"]]
            # Добавление к списку страниц списков из объектов класса Note, разбитых по 10 записей
            for i in range(0, len(notes), 10):
                pages_notes.append(notes[i: i + 10])
            counter = 0  # Счётчик для перемещения по вложенным спискам
            # Вывод на печать первого элемента списка страниц (меню перелистывания страниц)
            for i in pages_notes[counter]:
                print(i)
            print(f'Страница {counter + 1}')
            # Запуск цикла для перемещения по списку страниц
            # в зависимости от значения, переданного функцией options_for_show_pages
            while True:
                switch = options_for_show_pages()

                if switch == 1:
                    if counter == (len(pages_notes) - 1):  # Обработка граничных условий
                        print('\nВы находитесь на последней странице телефонного справочника!')
                    else:
                        counter += 1
                        for i in pages_notes[counter]:
                            print(i)
                        print(f'Страница {counter + 1}')

                if switch == 2:
                    if counter == 0:  # Обработка граничных условий
                        print('\nВы находитесь на первой странице телефонного справочника!')
                    else:
                        counter -= 1
                        for i in pages_notes[counter]:
                            print(i)
                        print(f'Страница {counter + 1}')

                if switch == 3:
                    return  # Выход в главное меню телефонного справочника

    def add_note(self):
        """Метод класса для добавления записи в телефонный справочник"""

        note = Note()  # Создание объекта класса Note со значениями атрибутов None
        # Определение значений атрибутов объекта и проверка на отсутствие пустых значений
        if note.add() == 0:
            return print('\nНе введён ни один из параметров для добавления нового контакта!\n')
        # Проверка на отсутствие добавляемой записи в телефонном справочнике
        # (уникальным критерием считать атрибут 'телефон личный(сотовый)')
        # и последующая запись в конец файла, в случае успешной проверки
        if Phonebook.find_note(note.personal_number) == ['\nПо вашему запросу записи не найдены!\n']:
            with open('Phonebook.txt', 'a', encoding='utf-8') as file:
                file.write(f'{note.surname}, '
                           f'{note.name}, '
                           f'{note.patronymic}, '
                           f'{note.organization}, '
                           f'{note.office_number}, '
                           f'{note.personal_number}\n')
                print('\nЗапись успешно дабавлена в телефонный справочник!\n')
        else:
            print('\nЗапись с таким личным телефоном (сотовым) уже существует!\n')

    def delete_note(self, query: str):
        """Метод класса для удаления записи(ей) из телефонного справочника"""

        with open('Phonebook.txt', 'r', encoding='utf-8') as file:
            output_notes = []  # создание пустого списка для добавление всех записей, считанных из файла
            delete_notes = []  # создание пустого списка для добавление удаляемых записей, соответствующих запросу
            for line in file.readlines():
                # Создание объекта класса Note на основе его строкового представления
                note = Note(*line.strip("\n").split(', '))
                output_notes.append(note)
                for i in query.split(','):
                    # Проверка на вхождение элемента запроса в значения атрибутов объекта класса Note
                    if i.strip() in note.__dict__.values():
                        delete_notes.append(note)
            # формирование нового списка (все записи минус удаляемые записи)
            new_notes = list(set(output_notes).difference(set(delete_notes)))
        if len(delete_notes) == 0:
            return f'\nПо вашему запросу записи не найдены\n'
        with open('Phonebook.txt', 'w', encoding='utf-8') as file:
            # Сортировка записей в лексикографическом порядке для последующей записи в файл
            new_notes = sorted([str(note) for note in new_notes])
            new_notes = [Note(*str(note).split(', ')) for note in new_notes]
            for note in new_notes:
                file.write(f'{note.surname}, '
                           f'{note.name}, '
                           f'{note.patronymic}, '
                           f'{note.organization}, '
                           f'{note.office_number}, '
                           f'{note.personal_number}\n')
            return f'\nУдалено(а/ы) {len(delete_notes)} запись(и/ей), соответствующих вашему запросу!\n'

    def change_note(self, query: str):
        """Метод класса для редактирования записи телефонного справочника"""

        notes = []  # Создание пустого списка записей для добавления в него объектов класса Note
        with open('Phonebook.txt', encoding='utf-8') as file:
            for line in file.readlines():
                # Создание объекта класса Note на основе его строкового представления и его добавление к списку записей
                note = Note(*line.strip("\n").split(', '))
                notes.append(note)

        note_change = Note()  # Создание объекта класса Note для редактируемой записи со значениями атрибутов None
        # Поиск редактируемой записи и её переприсваивание
        for i in Phonebook.find_note(query):
            if str(i).split(', ')[-1].strip() == str(query):
                print()
                note_change = i
            else:
                return f'\nЗапись с таким личным телефоном (сотовым) не найдена!\n'
        del_note = Note(*str(note_change).split(', '))  # Создание объекта класса Note для записи до редактирования
        print(f'Редактируемая запись: {note_change}')
        if note_change.add() == 0:
            return f'\nНе введён ни один параметр для редактирования!\n'
        notes.append(note_change)  # Добавление к списку записей редактируемой записи
        # Определение индекса записи до редактирования и её удаление из списка записей
        for i, note in enumerate(notes):
            if str(del_note) == str(note):
                notes.pop(i)
        with open('Phonebook.txt', 'w', encoding='utf-8') as file:
            # Сортировка записей в лексикографическом порядке для последующей записи в файл
            notes = sorted([str(note) for note in notes])
            notes = [Note(*str(note).split(', ')) for note in notes]
            for note in notes:
                file.write(f'{note.surname}, '
                           f'{note.name}, '
                           f'{note.patronymic}, '
                           f'{note.organization}, '
                           f'{note.office_number}, '
                           f'{note.personal_number}\n')
        return f'\nЗапись изменена!\n'


def options():
    """Функция для пользовательского ввода значения выбора в диапазоне 1-6"""

    switch = None
    while switch not in [1, 2, 3, 4, 5, 6]:
        try:
            switch = int(input("Вы находитесь в главном меню телефонного справочника.\n"
                               "Для вывода постранично записей из телефонного справочника введите '1'\n"
                               "Для добавления новой записи введите '2'\n"
                               "Для редактирования записи введите '3'\n"
                               "Для удаления записи(ей) введите '4'\n"
                               "Для поиска записи(ей) введите '5'\n"
                               "Для выхода введите '6'\n"
                               "Введите число, соответствующее выбранному действию [1-6]: "))
        except ValueError:
            print('\nДоступны только команды, значения которых находятся в диапазоне 1-6!\n')
    return switch


Phonebook = Phonebook()  # Создание объекта класса Phonebook

# Запуск цикла для перемещения по главному меню телефонного справочника
# в зависимости от значения, переданного функцией options
while True:
    switch = options()
    if switch == 1:
        Phonebook.show_pages()
    if switch == 2:
        Phonebook.add_note()
    if switch == 3:
        query = input("Введите личный телефон (сотовый) изменяемой записи\n(Для уточнения личного телефона ("
                      "сотового) Вы можете воспользоваться функцией поиска записи в главном меню телефонного "
                      "справочника): ")
        print(Phonebook.change_note(query))
    if switch == 4:
        query = input("Введите параметры записи(ей) для удаления, используя в качестве разделителя символ ',': ")
        print(Phonebook.delete_note(query))
    if switch == 5:
        query = input("Введите параметры записи(ей) для поиска, используя в качестве разделителя символ ',': ")
        print()
        for i in Phonebook.find_note(query):
            print(i)
        print()
    if switch == 6:
        break
