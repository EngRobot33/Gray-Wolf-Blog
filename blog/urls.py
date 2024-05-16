from django.urls import path

from .views import PostList, PostDetail, CategoryList, AuthorList, PostPreview

app_name = "blog"

urlpatterns = [
    path('', PostList.as_view(), name="home"),
    path('page/<int:page>', PostList.as_view(), name="home"),
    path('post/<slug:slug>', PostDetail.as_view(), name="detail"),
    path('preview/<int:pk>', PostPreview.as_view(), name="preview"),
    path('category/<slug:slug>', CategoryList.as_view(), name="category"),
    path('category/<slug:slug>/page/<int:page>', CategoryList.as_view(), name="category"),
    path('author/<slug:username>', AuthorList.as_view(), name="author"),
    path('author/<slug:username>/page/<int:page>', AuthorList.as_view(), name="author"),
]
