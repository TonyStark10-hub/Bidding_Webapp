from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing',views.create_listing,name='create_listing'),
    path('active_listing',views.active_listing,name='active_listing'),
    path('viewlisting/<int:item_id>',views.viewlisting,name='viewlisting'),
    path('addtowatchlist/<int:item_id>',views.addtowatchlist,name='addtowatchlist'),
    path('addcomment/<int:item_id>',views.addcomment,name='addcomment'),
    path('watchlist',views.watchlist_view,name='watchlist'),
    path('catagory/<str:cat>',views.catagory,name='catagory'),
    path('catagories',views.catagories,name='catagories'),
    path('closebid/<int:item_id>',views.closebid,name='closebid'),
    path('closedbidslist',views.closedbidslist,name='closedbidslist'),
    path('winnings',views.winnings,name='winnings')

]
