from django.urls import path
from .views import getAllJobs, getJob, createJob, updateJob, deleteJob, getTopics
urlpatterns = [
    path('jobs/', getAllJobs, name='jobs'),
    path('jobs/<int:id>/', getJob, name='job'),
    path('create_job/',createJob, name='new_job'),
    path('update_job/<int:id>/',updateJob, name='update_job'),
    path('delete_job/<int:id>/',deleteJob, name='delete_job'),
    path('get_topics/<str:topics>/', getTopics, name='get_topics'),

]