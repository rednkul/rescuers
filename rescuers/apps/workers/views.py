import re
from django.http import FileResponse
from django.db.models import Q, Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, UpdateView, CreateView

from .forms import WorkerForm
from .models import Worker, Post, Division, PostState, Service







class State:
    """Общее по штату"""

    def get_state_workers_number(self):
        return sum(PostState.objects.all().values_list('standard_size', flat=True).order_by())

    def get_workers_number(self):
        return Worker.objects.exclude(name='Вакансия').count()

    def get_vacancies_number(self):
        return Worker.objects.filter(name='Вакансия').count()

    def get_overstaffing(self):
        if self.get_workers_number() > self.get_state_workers_number():
            return self.get_workers_number() - self.get_state_workers_number()
        else:
            return 0

    def get_staffing_percent(self):
        if self.get_state_workers_number() > 0:
            return round(self.get_workers_number() * 100 / self.get_state_workers_number(), 2)
        else:
            return 0

    """По оперативному составу"""

    def get_state_operative_number(self):
        return sum(PostState.objects.filter(post__operative=True).values_list('standard_size', flat=True).order_by())

    def get_operative_number(self):
        return Worker.objects.filter(post__operative=True).exclude(name='Вакансия').count()

    def get_operative_vacancies_number(self):
        return Worker.objects.filter(post__operative=True, name='Вакансия').count()

    def get_operative_overstaffing_number(self):
        if self.get_operative_number() > self.get_state_operative_number():
            return self.get_operative_number() - self.get_state_operative_number()
        else:
            return 0

    def get_operative_staffing_percent(self):
        if self.get_state_operative_number() > 0:
            return round(self.get_operative_number() * 100 / self.get_state_operative_number())
        else:
            return 0

    """По респираторному составу"""

    def get_resperator_state(self):
        return sum(PostState.objects.filter(post__rescuer=True).values_list('standard_size', flat=True).order_by())

    def get_resperator_number(self):
        return  Worker.objects.filter(post__rescuer=True).exclude(name='Вакансия').count()

    """По административно-техническому составу"""

    def get_state_admin_number(self):
        return sum(PostState.objects.filter(post__operative=False).values_list('standard_size', flat=True).order_by())

    def get_admin_number(self):
        return Worker.objects.filter(post__operative=False).exclude(name='Вакансия').count()

    def get_admin_vacancies_number(self):
        return Worker.objects.filter(post__operative=False, name='Вакансия').count()

    def get_admin_overstaffing_number(self):
        if self.get_admin_number() > self.get_state_admin_number():
            return self.get_admin_number() - self.get_state_admin_number()
        else:
            return 0

    def get_admin_staffing_percent(self):
        if self.get_state_admin_number() > 0:
            return round(self.get_admin_number() * 100 / self.get_state_admin_number())
        else:
            return 0

class FilterSearchFields:

    def get_divisions(self):
        return Division.objects.all().annotate(cnt=Count('division_workers')).order_by('-cnt')

    def get_posts(self):
        return Post.objects.all()

    def get_operatives(self):
        return Post.objects.values_list('operative', flat=True).distinct()

    def get_rescuers(self):
        return Post.objects.values_list('rescuer', flat=True).distinct()

    def get_sexes(self):
        return sorted(Worker.objects.values_list("sex", flat=True).distinct())

    def get_state(self):
        sum_state = PostState.objects.aggregate(Sum('standard_size'))
        return sum_state['standard_size__sum']

    def get_workers_number(self):
        return Worker.objects.exclude(name='Вакансия').count()

    def get_vacancies_number(self):
        return Worker.objects.filter(name='Вакансия').count()

    def get_service_priorities(self):
        """
        Кортеж значений приоритета должностей, для которых выводится ({имя_службы}. cл.)
        """
        return (2, 3, 6)



class WorkersView(ListView, FilterSearchFields):
    queryset = Worker.objects.all()
    template_name = 'workers/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(self.get_divisions())
        context['division_list'] = self.get_divisions()
        context['filter'] = True

        return context



class Search(ListView, FilterSearchFields):
    """Поиск по ФИО"""
    template_name = 'workers/index.html'

    def get_workers(self):
        search = [i.capitalize() for i in self.request.GET.get('q').split()]

        if len(search) == 1:
            workers = Worker.objects.filter(
                                            Q(surname__iregex=search[0]) |
                                            Q(name__iregex=search[0]) |
                                            Q(lastname__iregex=search[0])
                                            )
        else:
            workers = Worker.objects.filter(
                                            Q(surname__in=search) |
                                            Q(name__in=search) |
                                            Q(lastname__in=search)
                                            )
        print(f'Workers----------------{workers}-----------------')
        return workers
    def get_queryset(self):

        return Division.objects.filter(division_workers__in=self.get_workers()).distinct().annotate(cnt=Count('division_workers')).order_by('-cnt')

    # Q(title__contains=self.request.GET.get('q').upper()) |
    # Q(title__contains=self.request.GET.get('q').lower()))

    def get_context_data(self, *args, **kwargs):
        search = self.request.GET.get('q')
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f"q={search}&"
        context['worker_list'] = self.get_workers()
        return context


class WorkerFilterView(FilterSearchFields, ListView):
    """Фильтрация продуктов по категории/поставщику/производителю"""
    template_name = 'workers/index.html'


    def get_workers(self):
        get_divisions = self.request.GET.getlist("division")
        get_posts = self.request.GET.getlist("post")
        get_operatives = self.request.GET.getlist("operative")
        get_rescuers = self.request.GET.getlist("rescuer")
        get_sexes = self.request.GET.getlist("sex")
        get_vacancy = self.request.GET.get("vacancy")
        print(get_vacancy)

        print(f'ВАк фильтр--------------------{get_vacancy}-----------------')


        division_filter = get_divisions if get_divisions else self.get_divisions()
        post_filter = get_posts if get_posts else self.get_posts()
        operative_filter = get_operatives if get_operatives else self.get_operatives()
        rescuer_filter = get_rescuers if get_rescuers else self.get_rescuers()
        sex_filter = get_sexes if get_sexes else self.get_sexes()
        print(f'Пол-------------{sex_filter}')

        if get_vacancy == '1':
            vacancy_filter = 'Вакансия'

            workers = Worker.objects.filter(division__in=division_filter,
                                            post__in=post_filter,
                                            post__operative__in=operative_filter,
                                            post__rescuer__in=rescuer_filter,
                                            sex__in=sex_filter,
                                            name=vacancy_filter,
                                            )
        elif get_vacancy == '2':

            workers = Worker.objects.filter(division__in=division_filter,
                                            post__in=post_filter,
                                            post__operative__in=operative_filter,
                                            post__rescuer__in=rescuer_filter,
                                            sex__in=sex_filter,
                                            ).exclude(name='Вакансия')
        else:
            workers = Worker.objects.filter(division__in=division_filter,
                                            post__in=post_filter,
                                            post__operative__in=operative_filter,
                                            post__rescuer__in=rescuer_filter,
                                            sex__in=sex_filter,
                                            )
        print(f'-------------------{workers}')
        return workers

    def get_queryset(self):

        return Division.objects.filter(division_workers__in=self.get_workers()).annotate(cnt=Count('division_workers')).order_by('-cnt')


    def get_context_data(self, *args, **kwargs):
        get_divisions = self.request.GET.getlist("division")
        get_posts = self.request.GET.getlist("post")
        get_operatives = self.request.GET.getlist("operative")
        get_rescuers = self.request.GET.getlist("rescuer")
        get_sexes = self.request.GET.getlist("sex")
        get_vacancy = self.request.GET.get("vacancy")

        context = super().get_context_data(*args, **kwargs)
        context['worker_list'] = self.get_workers()
        context['division'] = ''.join([f"division={x}&" for x in get_divisions])
        context['post'] = ''.join([f"post={x}&" for x in get_posts])
        context['operative'] = ''.join([f"operative={x}&" for x in get_operatives])
        context['rescuer'] = ''.join([f"rescuer={x}&" for x in get_rescuers])
        context['sex'] = ''.join([f"sex={x}&" for x in get_sexes])
        context['vacancy'] = f"vacancy={get_vacancy}&"
        # Определяю, есть ли фильтрация по должности/оеративности/аттестованности
        # Если есть, то убираю вывод штатного и фактического размера подразделения

        context['filter'] = not any((get_posts, get_operatives, get_rescuers, get_sexes, get_vacancy))
        return context


class WorkerDetailView(DetailView):
    model = Worker
    slug_field = 'id'



class NewWorkerView(CreateView):
    model = Worker
    template_name = 'workers/new_worker.html'
    fields = ['surname', 'name', 'lastname', 'sex', 'post', 'division', 'photo']
    success_url = reverse_lazy('workers:home_page')

class EditWorkerView(UpdateView):
    model = Worker
    template_name = 'workers/edit_worker.html'
    fields = ['surname', 'name', 'lastname', 'sex', 'post', 'division', 'attestated','date_beginning', 'date_attestation', 'photo']

class NewPostView(CreateView):
    model = Post
    template_name = 'workers/new_post.html'
    fields = ['name', 'service', 'operative', 'rescuer', 'attestation_period']
    success_url = reverse_lazy('workers:home_page')

class EditPostView(UpdateView):
    model = Post
    template_name = 'workers/edit_post.html'
    fields = ['name', 'service', 'operative', 'rescuer', 'attestation_period']
    success_url = reverse_lazy('workers:home_page')

class NewDivisionView(CreateView):
    model = Division
    template_name = 'workers/new_division.html'
    fields = ['name', 'standard_size']
    success_url = reverse_lazy('workers:home_page')

class EditDivisionView(UpdateView):
    model = Division
    template_name = 'workers/edit_division.html'
    fields = ['name', 'standard_size']
    success_url = reverse_lazy('workers:home_page')

class DivisionListView(ListView):
    queryset = Division.objects.all().annotate(cnt=Count('division_workers')).order_by('-cnt')
    template_name = 'workers/divisions/division_list.html'

class DivisionDetailView(DetailView, FilterSearchFields):
    model = Division
    slug_field = 'id'
    template_name = 'workers/divisions/division_detail.html'

    def get_division(self):
        url = self.request.path



        division_id =  re.search('\d{1,}', url).group(0)

        division = Division.objects.get(id=division_id)
        print(f'--------------------------------------{division}--------------------')
        return division

    def get_posts(self):
        division = self.get_division()
        workers = Worker.objects.filter(division=division)
        print(Post.objects.filter(post_workers__in=workers))
        return Post.objects.filter(post_workers__in=workers).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.get_posts()
        context['worker_list'] = Worker.objects.filter(division=self.get_division())
        context['filter'] = True
        return context


class DivisionFilter(ListView, FilterSearchFields):
    model = Division
    template_name = 'workers/divisions/division_detail.html'


    def get_posts(self):
        division = self.get_division()
        workers = Worker.objects.filter(division=division)
        return Post.objects.filter(post_workers__in=workers).distinct()



    def get_division(self):

        division_id = self.request.GET.get('division')

        return Division.objects.get(id=division_id)

    def get_workers(self):
        division = self.get_division()

        get_posts = self.request.GET.getlist("post")
        get_operatives = self.request.GET.getlist("operative")
        get_rescuers = self.request.GET.getlist("rescuer")
        get_sexes = self.request.GET.getlist("sex")
        get_vacancy = self.request.GET.get("vacancy")

        post_filter = get_posts if get_posts else self.get_posts()
        operative_filter = get_operatives if get_operatives else self.get_operatives()
        rescuer_filter = get_rescuers if get_rescuers else self.get_rescuers()
        sex_filter = get_sexes if get_sexes else self.get_sexes()



        if get_vacancy == '1':


            workers = Worker.objects.filter(division=division,
                                            post__in=post_filter,
                                            post__operative__in=operative_filter,
                                            post__rescuer__in=rescuer_filter,
                                            sex__in=sex_filter,
                                            name='Вакансия',
                                            )
        elif get_vacancy == '2':

            workers = Worker.objects.filter(division=division,
                                            post__in=post_filter,
                                            post__operative__in=operative_filter,
                                            post__rescuer__in=rescuer_filter,
                                            sex__in=sex_filter,
                                            ).exclude(name='Вакансия')
        else:
            workers = Worker.objects.filter(division=division,
                                            post__in=post_filter,
                                            post__operative__in=operative_filter,
                                            post__rescuer__in=rescuer_filter,
                                            sex__in=sex_filter,
                                            )

        return workers


    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args, **kwargs)

        get_posts = self.request.GET.getlist("post")
        get_operatives = self.request.GET.getlist("operative")
        get_rescuers = self.request.GET.getlist("rescuer")
        get_sexes = self.request.GET.getlist("sex")
        get_vacancy = self.request.GET.get("vacancy")

        worker_list = self.get_workers()
        if worker_list:
            context['worker_list'] = worker_list
        context['posts'] = self.get_posts()
        context['division'] = self.get_division()


        context['post'] = ''.join([f"post={x}&" for x in get_posts])
        context['operative'] = ''.join([f"operative={x}&" for x in get_operatives])
        context['rescuer'] = ''.join([f"rescuer={x}&" for x in get_rescuers])
        context['sex'] = ''.join([f"sex={x}&" for x in get_sexes])
        context['vacancy'] = f"vacancy={get_vacancy}&"

        context['filter'] = not any((get_posts, get_operatives, get_rescuers, get_sexes, get_vacancy))
        return context


class DivisionSearch(ListView, FilterSearchFields):
    template_name = 'workers/divisions/division_detail.html'
    model = Division
    def get_posts(self):
        division = self.get_division()
        workers = Worker.objects.filter(division=division)
        return Post.objects.filter(post_workers__in=workers)




    def get_division(self):
        url = self.request.path

        division_id = re.search('\d{1,}', url).group(0)

        division = Division.objects.get(id=division_id)
        print(f'--------------------------------------{division}--------------------')
        return division




    def get_workers(self):
        search = [i.capitalize() for i in self.request.GET.get('q').split()]
        division = self.get_division()
        if len(search) == 1:
            workers = Worker.objects.filter(division=division).filter(
                Q(surname__iregex=search[0]) |
                Q(name__iregex=search[0]) |
                Q(lastname__iregex=search[0])
            )
            print(f'Workers1----------------{workers}-----------------')
        else:
            workers = Worker.objects.filter(division=division).filter(
                Q(surname__in=search) |
                Q(name__in=search) |
                Q(lastname__in=search)
            )
            print(f'Workers2----------------{workers}-----------------')
        return workers



    # Q(title__contains=self.request.GET.get('q').upper()) |
    # Q(title__contains=self.request.GET.get('q').lower()))

    def get_context_data(self, *args, **kwargs):
        search = self.request.GET.get('q')
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f"q={search}&"

        worker_list = self.get_workers()
        if worker_list:
            context['worker_list'] = worker_list

        context['division'] = self.get_division()
        return context



class NewPostStateView(CreateView):
    model = PostState
    template_name = 'workers/new_post_state.html'
    fields = ['division', 'post', 'standard_size']
    success_url = reverse_lazy('workers:home_page')

class StaffingView(ListView, FilterSearchFields, State):
    model = Service
    template_name = 'workers/staffing.html'




    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        """Общий штат"""
        context['state_number'] = self.get_state_workers_number()
        context['workers_number'] = self.get_workers_number()
        context['vacancies_number'] = self.get_vacancies_number()
        context['overstaffing'] = self.get_overstaffing()
        context['staffing_percent'] = self.get_staffing_percent()

        """Оперативный состав"""
        context['operative_state'] = self.get_state_operative_number()
        context['operative_number'] = self.get_operative_number()
        context['operative_vacancies'] = self.get_operative_vacancies_number()
        context['operative_overstaffing'] = self.get_operative_overstaffing_number()
        context['operative_staffing_percent'] = self.get_operative_staffing_percent()

        """Административно-технический состав"""
        context['admin_state'] = self.get_state_admin_number()
        context['admin_number'] = self.get_admin_number()
        context['admin_vacancies'] = self.get_admin_vacancies_number()
        context['admin_overstaffing'] = self.get_admin_overstaffing_number()
        context['admin_staffing_percent'] = self.get_admin_staffing_percent()


        return context