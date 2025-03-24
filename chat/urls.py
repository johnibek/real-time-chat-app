from django.urls import path
from . import views


urlpatterns = [
    path("", views.chat_view, name='home'),
    path("chat/<str:username>", views.get_or_create_chatroom, name="start-chat"),
    path("chat/room/<str:chatroom_name>", views.chat_view, name='chatroom'),
    path("chat/new_groupchat/", views.create_groupchat, name='new-groupchat'),
    path("chat/edit/<str:chatroom_name>", views.chatroom_edit_view, name="edit-chatroom"),
    path("chat/delete/<str:chatroom_name>", views.chatroom_delete_view, name='delete-chatroom'),
    path("chat/leave/<str:chatroom_name>", views.chatroom_leave_view, name='leave-chatroom'),
    path("chat/fileupload/<str:chatroom_name>", views.chat_file_upload, name='chat-file-upload'),
]