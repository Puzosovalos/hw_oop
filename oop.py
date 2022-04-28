class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __gt__(self, other):
        '''Тут будет сравнение по оценке.'''
        try:
            result = self.get_avg_grades()[0]
            result_other = other.get_avg_grades()[0]
        except ValueError:
            return 'Невозможно получить среднюю оценку'
        return result > result_other

    def get_avg_grades(self):
        avg_dict = {}
        for k, v in self.grades.items():
            avg_dict[k] = float(sum(v)) // float(len(v))
        result = [float(elem) for elem in list(avg_dict.values())]
        return result

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (f'Имя: {self.name} \nФамилия: {self.surname} '
                f'\nКурсы в процессе изучения: {", ".join(self.courses_in_progress)}'
                f'\nСредняя оценка за домашние задания: {self.get_avg_grades()[0]}'
                f'\nЗавершенные курсы: {", ".join(self.finished_courses)}')


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def attach_course(self, course):
        self.courses_attached += course

    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname}'


class Lecturer(Mentor):
    def __init__(self, name, surname):
        self.grades = {}
        super().__init__(name, surname)

    def __gt__(self, other):
        '''Тут будет сравнение по оценке.'''
        try:
            result = self.get_avg_grades()[0]
            result_other = other.get_avg_grades()[0]
        except ValueError:
            return 'Невозможно получить среднюю оценку'
        return result > result_other

    def attach_course(self, course):
        return super().attach_course(course)

    def get_avg_grades(self):
        avgDict = {}
        for k, v in self.grades.items():
            avgDict[k] = sum(v) // float(len(v))
        result = [str(elem) for elem in list(avgDict.values())]
        return ', '.join(result)

    def __str__(self):
        return (f'Имя: {self.name} \nФамилия: {self.surname}'
                f'\nСредняя оценка за лекции: {self.get_avg_grades()}')


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print('Ошибка')

    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname}'


def get_all_avg_students(students, courses):
    grades = []
    for student in students:
        for course in courses:
            grades.extend(student.grades[course])
    avg = round(sum(grades) / len(grades))
    return avg


def get_all_avg_lectures(lectures, courses):
    grades = []
    for lecturer in lectures:
        for course in courses:
            grades.extend(lecturer.grades[course])
    avg = round(sum(grades) / len(grades))
    return avg


if __name__ == '__main__':
    student1 = Student('Ivan', 'Student', 'Male')
    student1.courses_in_progress += ['Python', 'Git']
    student2 = Student('Maria', 'student2', 'Female')
    student2.courses_in_progress += ['Python', 'Git']
    reviewer1 = Reviewer('Artem', 'Reviewer1')
    reviewer1.courses_attached += ['Python', 'Git']
    reviewer2 = Reviewer('Anton', 'Reviewer2')
    reviewer2.courses_attached += ['Python', 'Git']
    lecturer1 = Lecturer('Carl', 'Lecturer1')
    lecturer1.courses_attached += ['Python', 'Git']
    lecturer2 = Lecturer('Oleg', 'Lecturer2')
    lecturer2.courses_attached += ['Python', 'Git']
    student1.rate_lecturer(lecturer1, 'Python', 7)
    student2.rate_lecturer(lecturer1, 'Python', 5)
    student1.rate_lecturer(lecturer2, 'Python', 10)
    student2.rate_lecturer(lecturer2, 'Python', 6)
    reviewer1.rate_hw(student1, 'Python', 10)
    reviewer1.rate_hw(student1, 'Python', 7)
    reviewer2.rate_hw(student1, 'Python', 4)
    reviewer1.rate_hw(student2, 'Python', 3)
    reviewer1.rate_hw(student2, 'Python', 6)
    reviewer2.rate_hw(student2, 'Python', 5)
    print(student1)
    print(student2)
    print(lecturer1)
    print(lecturer2)
    list_students = [student1, student2]
    list_courses = ['Python']
    list_lectures = [lecturer1, lecturer2]
    list_courses = ['Python']
    print(get_all_avg_students(list_students, list_courses))
    print(get_all_avg_lectures(list_lectures, list_courses))