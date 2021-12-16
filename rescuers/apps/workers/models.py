from django.db import models


# Create your models here.
from django.urls import reverse


class Service(models.Model):
    """Службы"""
    name = models.CharField('Наименование', max_length=50)

    def get_abbreviation(self):
        abbreviation = ''
        first_letters = [s[0].capitalize() for s in self.name.split()]
        for i in first_letters:
            abbreviation += i
        return abbreviation

    def get_service_state(self):
        return sum(PostState.objects.filter(post__service=self).values_list('standard_size', flat=True))

    def get_service_workers_number(self):
        return Worker.objects.filter(post__in=self.service_posts.all()).exclude(name='Вакансия').count()

    def get_service_vacancies_number(self):
        return Worker.objects.filter(post__in=self.service_posts.all(), name='Вакансия').count()

    def get_service_overstaffing(self):
        if self.get_service_workers_number() > self.get_service_state():
            return self.get_service_workers_number() - self.get_service_state()
        else:
            return 0

    def get_service_staffing_percent(self):
        if self.get_service_state() > 0:
            return round(self.get_service_workers_number() * 100 / self.get_service_state(), 2)
        else:
            return 0
    def __str__(self):
        if len(self.get_abbreviation()) > 2:
            return f'{self.name} ({self.get_abbreviation()})'
        else:
            return f'{self.name}'

    class Meta:
        verbose_name = "Служба"
        verbose_name_plural = "Службы"

class Post(models.Model):
    """Должность"""
    name = models.CharField('Наименование', max_length=100)
    operative = models.BooleanField('Принадлежность к оперативному составу')
    rescuer = models.BooleanField('Принадлежность к аттестованным спасателям')
    attestation_period = models.CharField('Время между аттестациями для должности(если необходимо)', max_length=20)
    SERVICE_CHOICES = (
                       ('мед', 'мед'),
                       ('проф', 'проф'),
                       ('опер', 'опер'),
                       )
    service_in_name = models.CharField('Служба (для вывода в названии должности)',help_text='Добавить при необходимости', choices=SERVICE_CHOICES, max_length=12, blank=True, default='')
    priority = models.PositiveSmallIntegerField('Приоритет вывода в списке', blank=True, default=9,
                                                help_text="Для командира отряда- 1; "
                                                          "Для зам.ком. отряда - 2; "
                                                          "Для пом.ком. отряда - 3; "
                                                          "Для ком. взвода     - 4; "
                                                          "Для зам.ком.взвода  - 5; "
                                                          "Для пом.ком. взвода - 6; "
                                                          "Для ком.отдел.      - 7; "
                                                          "Для респираторщика  - 8; "
                                                          "Для остальных по умолчанию - 9.")

    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True,
                                blank=True, default=None, related_name='service_posts')
    def __str__(self):
        if self.service_in_name:
            return f"{self.name} ({self.service_in_name}.сл)"
        else:
            return f"{self.name}"

    def get_post_state(self):
        return sum(self.post_state.values_list('standard_size', flat=True))

    def get_post_workers_number(self):
        return Worker.objects.filter(post=self).exclude(name='Вакансия').count()

    def get_post_vacancies_number(self):
        return Worker.objects.filter(post=self, name='Вакансия').count()

    def get_overstaffing(self):
        if self.get_post_workers_number() > self.get_post_state():
            return self.get_post_workers_number() - self.get_post_state()


    def get_staffing_percent(self):
        if self.get_post_state() > 0:
            return round(self.get_post_workers_number() * 100 / self.get_post_state(), 2)


    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class Division(models.Model):
    """Подразделеение"""
    name = models.CharField('Наименование', max_length=100)
    standard_size = models.PositiveSmallIntegerField('Штатный размер')

    def get_state(self):
        return sum(self.division_state.values_list('standard_size', flat=True))

    def get_vacancies(self):
        return len(self.division_workers.filter(name='Вакансия'))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"



class Worker(models.Model):
    """Сотрудник"""
    surname = models.CharField('Фамилия', max_length=30, blank=True)
    name = models.CharField('Имя', max_length=30)
    lastname = models.CharField('Отчество', max_length=30, blank=True)
    SEX_CHOICES = (('МУЖ', 'МУЖ'),
                   ('ЖЕН', 'ЖЕН'))
    sex = models.CharField('Пол', max_length=6, choices=SEX_CHOICES, default='МУЖ', blank=True)
    post = models.ForeignKey(Post, verbose_name='Должность', on_delete=models.SET_NULL,
                             blank=True, null=True, related_name='post_workers')
    division = models.ForeignKey(Division, verbose_name='Подразделение', on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name='division_workers')
    date_beginning = models.DateField('Время начала службы')
    date_attestation = models.DateField('Дата последней аттестации', blank=True, default=None, null=True)
    on_duty = models.BooleanField('Фактическое нахождение на службе', blank=True, default=True, null=True)
    photo = models.ImageField('Фото', blank=True, default='', upload_to='workers/')
    attestated = models.BooleanField('Аттестован', blank=True, default=False, null=True)
    #vacancy = models.BooleanField('Вакансия', default='False', help_text='Выберите, если создаете вакансию')

    def get_full_name(self):
        return f'{self.surname} {self.name} {self.lastname}'

    def get_initials(self):
        return f"{self.name[0]}.{self.lastname[0]}. {self.surname} "

    def get_absolute_url(self):
        return reverse('workers:worker_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.surname} {self.name} {self.lastname}'

    class Meta:

        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class PostState(models.Model):
    """Штатный размер должности в подразделении"""
    division = models.ForeignKey(Division, verbose_name='Подразделение',
                                 on_delete=models.CASCADE, blank=True, related_name='division_state')

    post = models.ForeignKey(Post, verbose_name='Должность', on_delete=models.CASCADE,
                             blank=True, related_name='post_state')

    standard_size = models.PositiveSmallIntegerField('Штатный размер должности в подразделении', default=0)



    def __str__(self):
        return f'{self.division.name} - {self.post.name} : {self.standard_size}'

    class Meta:
        verbose_name = 'Штатный размер должности'
        verbose_name_plural = 'Штатные размеры должностей'
        unique_together = ['division', 'post']

