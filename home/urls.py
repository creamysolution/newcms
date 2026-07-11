from django.urls import path
from .views import home,create_event,event_detail, join_event, cancel_seat,my_bookings,my_events,cancel_event
urlpatterns= [
    path('',home, name="home"),
    path('create_event/',create_event, name="create_event"),
    path('event/<int:event_id>/', event_detail, name='event_detail'),
    path('event/<int:event_id>/join/', join_event, name='join_event'),
    path('event/<int:event_id>/cancel/', cancel_event, name='cancel_event'),

    path('event/<int:event_id>/seat/cancel/', cancel_seat, name='cancel_seat'),
    path('my/bookings/', my_bookings, name='my_bookings'),
    path('my/events/', my_events, name='my_events'),

    
]