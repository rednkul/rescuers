from django.urls import path
from .views import WorkersView, Search, WorkerFilterView, WorkerDetailView, NewWorkerView, EditWorkerView, \
    EditWorkerView, \
    NewPostView, EditPostView, EditDivisionView, NewDivisionView, DivisionListView, DivisionDetailView, DivisionFilter, \
    DivisionSearch, NewPostStateView, StaffingView

app_name = 'workers'

urlpatterns = [
    #Страницы сотрудников
    path('', WorkersView.as_view(), name='home_page'),
    path('search/', Search.as_view(), name='search'),
    path('worker_filter/', WorkerFilterView.as_view(), name='worker_filter'),
    path('worker/<int:pk>/', WorkerDetailView.as_view(), name='worker_detail'),
    path('new_worker/', NewWorkerView.as_view(), name='new_worker'),
    path('edit_worker/<int:pk>/', EditWorkerView.as_view(), name='edit_worker'),

    # Страницы должностей
    path('new_post/', NewPostView.as_view(), name='new_post'),
    path('edit_post/<int:pk>/', EditPostView.as_view(), name='edit_post'),
    path('new_post_state/', NewPostStateView.as_view(), name='new_post_state'),

    # Страницы подразделений
    path('new_division/', NewDivisionView.as_view(), name='new_division'),
    path('edit_division/<int:pk>/', EditDivisionView.as_view(), name='edit_division'),
    path('divisions/', DivisionListView.as_view(), name='divisions'),
    path('divisions/division_detail/<int:pk>/', DivisionDetailView.as_view(), name='division_detail'),
    path('division/division_detail/<int:pk>/filter/', DivisionFilter.as_view(), name='division_filter'),
    path('division/division_detail/<int:pk>/search/', DivisionSearch.as_view(), name='division_search'),

    # Укомплектованность
    path('staffing/', StaffingView.as_view(), name='staffing'),



]