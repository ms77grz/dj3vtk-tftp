from django.urls import path
# from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = 'blog'

urlpatterns = [
    # path('', views.post_list, name='post_list'),
    path('', PostListView.as_view(), name='post_list'),
    # path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
