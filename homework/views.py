# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        data = [
            {
                'id': 'id_1',
                'name': 'Ivanov Ivan Ivanovich',
                'course': 1,
                'group': '2D93',
                'Chemistry': 5,
                'Physics': 5,
                'Math': 5,
                'Philosophy': 5,
                'ComputerScience': 5,
            },

            {
                'id': 'id_2',
                'name': 'Petrov Fedor Petrovich',
                'course': 1,
                'group': '2D93',
                'Chemistry': 5,
                'Physics': 5,
                'Math': 5,
                'Philosophy': 2,
                'ComputerScience': 5,
            },

            {
                'id': 'id_3',
                'name': 'Semionov Petr Sergeevich',
                'course': 1,
                'group': '2D91',
                'Chemistry': 5,
                'Physics': 4,
                'Math': 4,
                'Philosophy': 3,
                'ComputerScience': 4,
            },

            {
                'id': 'id_4',
                'name': 'Popov Pavel Semionovich',
                'course': 1,
                'group': '2D91',
                'Chemistry': 5,
                'Physics': 2,
                'Math': 3,
                'Philosophy': 3,
                'ComputerScience': 2,
            },

            {
                'id': 'id_5',
                'name': 'Titova Svetlana Nikolaevna',
                'course': 2,
                'group': '2D81',
                'Chemistry': 5,
                'Physics': 5,
                'Math': 5,
                'Philosophy': 5,
                'ComputerScience': 5,
            },

            {
                'id': 'id_6',
                'name': 'Krylova Irina Petrovna',
                'course': 2,
                'group': '2D81',
                'Chemistry': 5,
                'Physics': 4,
                'Math': 4,
                'Philosophy': 3,
                'ComputerScience': 5,
            },

            {
                'id': 'id_7',
                'name': 'Popova Marya Sergeevna',
                'course': 2,
                'group': '2D81',
                'Chemistry': 5,
                'Physics': 4,
                'Math': 3,
                'Philosophy': 5,
                'ComputerScience': 4,
            },
        ]
        subjects_list = ['Chemistry', 'Physics', 'Math', 'Philosophy', 'ComputerScience']

        creator = Creator(data, subjects_list)
        students = creator.create_students()
        subjects = creator.create_subjects()
        statistic = Statistics()

        context.update(
            {
                'students_statistics': statistic.show_data(creator, students),
                'excellent_students': statistic.get_excelent_students(students),
                'bad_students': statistic.to_deduction(students),
                'difficult_subjects': statistic.get_difficult_subjects(subjects),
                'easy_subjects': statistic.get_easy_subjects(subjects),
            }
        )
        return context


class Student:
    def __init__(self, name, group, scores):
        self.name = name
        self.group = group
        self.scores = scores

    def show_name(self):
        return self.name

    def show_group(self):
        return self.group

    def show_scores(self):
        return self.scores

    def __repr__(self):
        return self.name


class Subject:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores

    def __repr__(self):
        return self.name


class Creator:
    def __init__(self, data, subjects):
        self.data = data
        self.subjects = subjects
        data_len = len(self.data)

        self.student_id_list = [self.data[i]['id'] for i in range(data_len)]
        self.student_name_list = [self.data[i]['name'] for i in range(data_len)]
        self.group_list = [self.data[i]['group'] for i in range(data_len)]
        
        self.student_score_list = [({subject: self.data[i][subject]
                                     for subject in self.subjects}) for i in range(data_len)]

        self.subject_score_map = {subject: [self.data[i][subject]
                                            for i in range(data_len)] for subject in self.subjects}

    def create_students(self):
        student_map = {student_id: Student(name, group, scores) for student_id, name, group, scores
                       in zip(self.student_id_list, self.student_name_list, self.group_list, self.student_score_list)}

        return student_map

    def create_subjects(self):
        scores_generator = (self.subject_score_map[name] for name in self.subjects)

        subject_map = {name: Subject(name, scores) for name, scores in
                       zip(self.subjects, scores_generator)}

        return subject_map


class Statistics:
    @staticmethod
    def get_student_average_score(student: Student):
        scores = student.scores.values()
        average_score = sum(scores) / len(scores)

        return average_score

    @staticmethod
    def get_excelent_students(students: dict):
        students_average = {student.show_name(): Statistics.get_student_average_score(student)
                            for student in students.values()}

        excelent_students = [student for student in students_average if students_average[student] == 5]

        return ', '.join(excelent_students)

    @staticmethod
    def to_deduction(students: dict):
        students_scores = {student.show_name(): student.show_scores()
                           for student in students.values()}

        bed_students = [student for student in students_scores if 2 in students_scores[student].values()]

        return ', '.join(bed_students)

    @staticmethod
    def show_data(creator: Creator, students):
        students_data = creator.data

        for item, student in zip(students_data, students.values()):
            item['AverageScore'] = Statistics.get_student_average_score(student)

        return students_data

    @staticmethod
    def get_subjects_average_score(subject: Subject):
        scores = subject.scores
        average_score = sum(scores) / len(scores)

        return average_score

    @staticmethod
    def get_difficult_subjects(subjects: dict):
        subject_average = {subject.name: Statistics.get_subjects_average_score(subject)
                           for subject in subjects.values()}

        difficult_subjects = [subject for subject in subject_average if subject_average[subject] < 4]

        return ', '.join(difficult_subjects)

    @staticmethod
    def get_easy_subjects(subjects: dict):
        subject_average = {subject.name: Statistics.get_subjects_average_score(subject)
                           for subject in subjects.values()}

        easy_subjects = [subject for subject in subject_average if subject_average[subject] > 4.5]

        return ', '.join(easy_subjects)
