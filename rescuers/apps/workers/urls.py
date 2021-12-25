from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import WorkersView, Search, WorkerFilterView, WorkerDetailView, NewWorkerView, EditWorkerView, \
    EditWorkerView, \
    NewPostView, EditPostView, EditDivisionView, NewDivisionView, DivisionListView, DivisionDetailView, DivisionFilter, \
    DivisionSearch, NewPostStateView, StaffingView, NewVacancyView, WorkerDeleteView, DivisionDeleteView, \
    ServiceEditView, PostDetailView, PostStateDetailView, PostStateEditView, NewServiceView, DeletePostView

app_name = 'workers'





urlpatterns = [
    #Страницы сотрудников
    path('', login_required(WorkersView.as_view()), name='home_page'),
    path('search/', login_required(Search.as_view()), name='search'),
    path('worker_filter/', login_required(WorkerFilterView.as_view()), name='worker_filter'),
    path('worker/<int:pk>/', login_required(WorkerDetailView.as_view()), name='worker_detail'),
    path('new_worker/', login_required(NewWorkerView.as_view()), name='new_worker'),
    path('edit_worker/<int:pk>/', login_required(EditWorkerView.as_view()), name='edit_worker'),
    path('worker/<int:pk>/delete_worker', login_required(WorkerDeleteView.as_view()), name='delete_worker'),
    path('new_vacancy/', login_required(NewVacancyView.as_view()), name='new_vacancy'),

    # Страницы должностей
    path('new_post/', login_required(NewPostView.as_view()), name='new_post'),
    path('edit_post/<int:pk>/', login_required(EditPostView.as_view()), name='edit_post'),
    path('post/<int:pk>/delete_post/', login_required(DeletePostView.as_view()), name='delete_post'),
    path('new_post_state/', login_required(NewPostStateView.as_view()), name='new_post_state'),
    path('post_state/<int:pk_div>_<int:pk_post>/', login_required(PostStateDetailView.as_view()), name='post_state_detail'),
    path('post/<int:pk>/', login_required(PostDetailView.as_view()), name='post_detail'),
    path('edit_post_state/<slug:slug>/', login_required(PostStateEditView.as_view()),
                                        name='edit_post_state'),

    # Страницы подразделений
    path('new_division/', login_required(NewDivisionView.as_view()), name='new_division'),
    path('edit_division/<int:pk>/', login_required(EditDivisionView.as_view()), name='edit_division'),
    path('divisions/', login_required(DivisionListView.as_view()), name='divisions'),
    path('divisions/<int:pk>/delete_division/', login_required(DivisionDeleteView.as_view()), name='delete_division'),
    path('divisions/division_detail/<int:pk>/', login_required(DivisionDetailView.as_view()), name='division_detail'),
    path('division/division_detail/<int:pk>/filter/', login_required(DivisionFilter.as_view()), name='division_filter'),
    path('division/division_detail/<int:pk>/search/', login_required(DivisionSearch.as_view()), name='division_search'),

    # Укомплектованность
    path('staffing/', login_required(StaffingView.as_view()), name='staffing'),

    # Службы
    path('new_service/', login_required(NewServiceView.as_view()), name='new_service'),
    path('service_edit/<int:pk>/', login_required(ServiceEditView.as_view()), name='edit_service'),
    path('services/<int:pk>/delete_service/', login_required(DivisionDeleteView.as_view()), name='delete_service'),

]