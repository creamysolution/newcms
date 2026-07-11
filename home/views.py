from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import EventForm
from .models import Event, Bookings
from django.contrib.auth.decorators import login_required
# Create your views here.
# home,create_event,event_detail, join_event, cancel_seat 


def home(request):
    context = {'events': Event.objects.filter(dnt__gte=timezone.now()).order_by('dnt')}
    return render(request, 'home.html',context)

@login_required
def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.organizer = request.user
            obj.save()
            messages.success(request, f"Event '{obj.name}' created successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'event_form.html', {'form': form})
    context = {'form': form}
    return render(request, 'event_form.html', context)

# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Event, Bookings


def event_list(request):
    """Homepage — upcoming events only."""
    events = Event.objects.filter(dnt__gte=timezone.now()).order_by('dnt')
    return render(request, 'home.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    # All bookings for this event, oldest first — used for both the
    # attendee table and figuring out which seat box is "yours".
    bookings = event.bookings.select_related('participant').order_by('booked_at')

    user_has_joined = False
    my_seat_index = -1

    if request.user.is_authenticated:
        for index, booking in enumerate(bookings):
            if booking.participant == request.user:
                user_has_joined = True
                my_seat_index = index
                break

    context = {
        'event': event,
        'user_has_joined': user_has_joined,
        'my_seat_index': my_seat_index,
        'seat_range': range(event.total_seats),
        'attendees': bookings,
    }
    return render(request, 'event_detail.html', context)


@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method != 'POST':
        return redirect('event_detail', event_id=event_id)

    already_joined = Bookings.objects.filter(
        event=event, participant=request.user
    ).exists()

    if already_joined:
        messages.warning(request, "You've already joined this event.")
    elif event.seats <= 0:
        messages.error(request, "Sorry, this event is full.")
    else:
        Bookings.objects.create(event=event, participant=request.user)
        messages.success(request, f"You're in! Seat reserved for {event.name}.")

        if request.user.email:
            send_mail(
                subject=f"Booking confirmed: {event.name}",
                message=(
                    f"Hi {request.user.username},\n\n"
                    f"Your seat for '{event.name}' on "
                    f"{event.dnt.strftime('%b %d, %Y %I:%M %p')} at {event.venue} "
                    f"is confirmed.\n\nSee you there!"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True,
            )

    return redirect('event_detail', event_id=event.id)


@login_required
def cancel_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method != 'POST':
        return redirect('event_detail', event_id=event.id)


    if event.organizer == request.user:
        event.delete()
        messages.success(request, f"Your event '{event.name}' has been cancelled.")
    else:
        messages.warning(request, "You don't have permission to cancel this event.")

    return redirect('event_detail', event_id=event.id)

def cancel_seat(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    booking = Bookings.objects.filter(event=event, participant=request.user).first()

    if booking:
        booking.delete()
        messages.success(request, f"Your seat for {event.name} has been cancelled.")
    else:
        messages.warning(request, "You don't have a booking for this event.")

    return redirect('event_detail', event_id=event.id)

def my_bookings(request):
    bookings = Bookings.objects.filter(participant=request.user)
    context = {'bookings': bookings}
    return render(request, 'my_bookings.html', context)


def my_events(request):
    events = Event.objects.filter(organizer=request.user)
    context = {'events': events}
    return render(request, 'my_events.html', context)