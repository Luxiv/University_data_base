import random
import string

'''
to do:

doc strings

'''


def handle_type_error(funktion):
    def wrapper(self, *arg):
        try:
            res = funktion(self, *arg)
        except TypeError:
            raise ValueError('Value must be Integer! Please input correct data!')
        return res

    return wrapper


class Group_Gen:
    @handle_type_error
    def group_gene8or(self, number_of_groups: int):
        list_of_groups = [f'{random.choice(string.ascii_uppercase)}'
                          f'{random.choice(string.ascii_uppercase)}'
                          f'-{random.randint(0, 9)}{random.randint(0, 9)}'
                          for i in range(0, number_of_groups)]

        return list_of_groups


class Student_Gen:
    @handle_type_error
    def student_gene8or(self, number_of_students: int):
        first_name_list = ['Dominick', 'Santiago', 'Quentrell', 'Kamden', 'Branson', 'Trenton', 'Arthur', 'Cayden',
                           'Keaton', 'Tobias', 'Yesenia', 'Desiree', 'Kara', 'Melody', 'Xylina', 'Lola', 'Emilia',
                           'Uma', 'Joanna', 'Queena']
        last_name_list = ['Brown', 'Nelson', 'Bailey', 'Hernandez', 'Smith', 'Coleman', 'Torres', 'Roberts', 'Collins',
                          'Sanchez', 'Washington', 'Green', 'Morris', 'Price', 'Baker', 'James', 'Campbell', 'Stewart',
                          'Howard', 'Johnson']
        list_of_names = [f'{random.choice(first_name_list)} {random.choice(last_name_list)}'
                         for i in range(0, number_of_students)]
        return list_of_names


class Course_Gen:

    def courses_list(self):
        courses = ['math', 'biology', 'physics', 'chemistry', 'astronomy', 'computer science',
                   'programming', 'history', 'modeling', 'languages']
        return courses

