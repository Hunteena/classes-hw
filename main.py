def dict_average(some_dict):
    '''
    Считает среднюю оценку по словарю с оценками по курсам.
    Для этого сначала считает среднюю оценку по каждому курсу, а потом среднюю от них.
    '''
    average = 0
    if some_dict:
        for grades in some_dict.values():
            average += sum(grades) / len(grades)
        average /= len(some_dict)
    return average


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        return '\n'.join([f'Имя: {self.name}',
                          f'Фамилия: {self.surname}',
                          f'Средняя оценка за домашние задания: {dict_average(self.grades)}',
                          f'Курсы  в процессе изучения: {", ".join(self.courses_in_progress)}',
                          f'Завершённые курсы: {", ".join(self.finished_courses)}'])

    def __lt__(self, other):
        return  dict_average(self.grades) < dict_average(other.grades)

    def rate_lecturer(self, lecturer, course, rating):
        if isinstance(lecturer, Lecturer) \
                and course in (self.finished_courses + self.courses_in_progress) \
                and course in lecturer.courses_attached:
            if course in lecturer.ratings:
                lecturer.ratings[course].append(rating)
            else:
                lecturer.ratings[course] = [rating]
        else:
            print(f'Ошибка. {self.name} {self.surname} не может оценивать лекции {lecturer.name} {lecturer.surname} по курсу {course}')


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print(f'Ошибка. {self.name} {self.surname} не может оценивать домашние задания {student.name} {student.surname} по курсу {course}')


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.ratings = {}

    def __str__(self):
        return '\n'.join([f'Имя: {self.name}',
                          f'Фамилия: {self.surname}',
                          f'Средняя оценка за лекции: {dict_average(self.ratings)}'])
    def __lt__(self, other):
        return dict_average(self.ratings) < dict_average(other.ratings)

    def rate_hw(self, student, course, grade):
        print('Лектор не оценивает домашние задания!')


class Reviewer(Mentor):
    def __str__(self):
        return '\n'.join([f'Имя: {self.name}',
                          f'Фамилия: {self.surname}'])


def average_course_grade(students, course):
    '''
    Считает среднюю оценку за курс по всем студентам из списка
    '''
    average = 0
    counter = 0
    if students:
        for student in students:
            grade_list = student.grades.get(course)
            if grade_list:
                average += sum(grade_list) / len(grade_list)
                counter += 1
        if counter:
            average /= counter
    return average

def average_course_rate(lecturers, course):
    '''
    Считает среднюю оценку зв курс по всем лекторам из списка
    '''
    average = 0
    counter = 0
    if lecturers:
        for lecturer in lecturers:
            rating_list = lecturer.ratings.get(course)
            if rating_list:
                average += sum(rating_list) / len(rating_list)
                counter += 1
        if counter:
            average /= counter
    return average


def main():        
    student1 = Student('Pavel', 'Chekov', 'male')
    student1.finished_courses = ['Astronavigation']
    student1.courses_in_progress = ['Engineering', 'Communications']
    student2 = Student('Nyota', 'Uhura', 'female')
    student2.courses_in_progress = ['Xenolinguistics', 'Communications']


    lecturer1 = Lecturer('Christopher', 'Pike',)
    lecturer1.courses_attached = ['Astronavigation', 'Communications']
    lecturer2 = Lecturer('Sarek', 'Vulcan')
    lecturer2.courses_attached = ['Xenolinguistics', 'Engineering']

    reviewer1 = Reviewer('Spock', 'Vulcan')
    reviewer1.courses_attached = ['Xenolinguistics']
    reviewer2 = Reviewer('James', 'Kirk')
    reviewer2.courses_attached = ['Engineering', 'Communications']

    student1.rate_lecturer(lecturer1, 'Astronavigation', 7)
    student1.rate_lecturer(lecturer1, 'Communications', 8)
    student2.rate_lecturer(lecturer2, 'Xenolinguistics', 9)
    student2.rate_lecturer(lecturer1, 'Communications', 7)

    reviewer1.rate_hw(student2, 'Xenolinguistics', 10)
    reviewer1.rate_hw(student2, 'Xenolinguistics', 8)
    reviewer2.rate_hw(student1, 'Engineering', 8)
    reviewer2.rate_hw(student2, 'Communications', 9)

    print(student1, student2, lecturer1, lecturer2, reviewer1, reviewer2, sep='\n\n')

    print()
    print(f'{student1.name} {student1.surname} < {student2.name} {student2.surname} = {student1 < student2}')
    print(f'{lecturer1.name} {lecturer1.surname} < {lecturer2.name} {lecturer2.surname} = {lecturer1 < lecturer2}')

    print()
    course = 'Communications'
    print(f'Средняя оценка студентов за курс {course}: {average_course_grade([student1, student2], course)}')
    print(f'Средняя оценка лекторов за курс {course}: {average_course_rate([lecturer1, lecturer2], course)}')
    
main()

