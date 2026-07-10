from django.shortcuts import redirect, render,reverse
from .forms import EventForm
from .models import Event, Bookings
# Create your views here.
# home,create_event,event_detail, join_event, cancel_seat 


def home(request):
    return render(request, 'home.html')


def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'event_form.html', context)

def event_detail(request, event_id):
    # Fetch the event based on the provided event_id
    event = Event.objects.get(id=event_id)
    context = {'event': event}
    return render(request, 'event_detail.html', context)


def join_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if event.seats > 0:
        # Create a booking for the user
        Bookings.objects.create(user=request.user, event=event)
        # Decrease the available seats
        event.save()
        next_url = request.GET.get('next', reverse('event_detail', args=[event_id]))
    return redirect(next_url)

def cancel_seat(request, event_id):
    event = Event.objects.get(id=event_id)
    booking = Bookings.objects.filter(user=request.user, event=event).first()
    if booking:
        booking.delete()
        event.save()
    next_url = request.GET.get('next', reverse('event_detail', args=[event_id]))
    return redirect(next_url)


def my_bookings(request):
    bookings = Bookings.objects.filter(participant=request.user)
    context = {'bookings': bookings}
    return render(request, 'my_bookings.html', context)


def my_events(request):
    events = Event.objects.filter(organizer=request.user)
    context = {'events': events}
    return render(request, 'my_events.html', context)