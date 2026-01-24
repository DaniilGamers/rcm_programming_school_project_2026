from django.db import models


class OrderQuerySet(models.QuerySet):
    def by_name(self, name):
        return self.filter(name=name)

    def by_surname(self, surname):
        return self.filter(surname=surname)

    def by_email(self, email):
        return self.filter(email=email)

    def by_phone(self, phone):
        return self.filter(phone=phone)

    def by_age(self, age):
        return self.filter(age=age)

    def by_course(self, course):
        return self.filter(course=course)

    def by_course_format(self, course_format):
        return self.filter(course_format=course_format)

    def by_course_type(self, course_type):
        return self.filter(course_type=course_type)

    def by_status(self, status):
        return self.filter(status=status)

    def by_group(self, group):
        return self.filter(group=group)

    def by_date_startswith(self, date_startswith):
        return self.filter(date_startswith=date_startswith)

    def by_date_endswith(self, date_endswith):
        return self.filter(date_endswith=date_endswith)

    def by_manager(self, manager):
        return self.filter(manager=manager)


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model)

    def by_name(self, name):
        return self.get_queryset().by_name(name)

    def by_surname(self, surname):
        return self.get_queryset().by_surname(surname)

    def by_email(self, email):
        return self.get_queryset().by_email(email)

    def by_phone(self, phone):
        return self.get_queryset().by_phone(phone)

    def by_age(self, age):
        return self.get_queryset().by_age(age)

    def by_course(self, course):
        return self.get_queryset().by_course(course)

    def by_course_format(self, course_format):
        return self.get_queryset().by_course_format(course_format)

    def by_course_type(self, course_type):
        return self.get_queryset().by_course_type(course_type)

    def by_status(self, status):
        return self.get_queryset().by_status(status)

    def by_group(self, group):
        return self.get_queryset().by_group(group)

    def by_date_startswith(self, date_startswith):
        return self.get_queryset().by_date_startswith(date_startswith)

    def by_date_endswith(self, date_endswith):
        return self.get_queryset().by_date_endswith(date_endswith)

    def by_manager(self, manager):
        return self.get_queryset().by_manager(manager)
