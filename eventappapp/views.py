from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . models import AddEvents,Register, CustomUser
from datetime import datetime
# Create your views here.

def register(request, pk):
    events=get_object_or_404(AddEvents, pk=pk) 
    return render(request,'register.html',{'obj':events})

def members(request):
    return render(request,'members.html')

def login_view(request):
    organisation = request.GET.get('organisation')  # Get organisation from URL

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email, organisation=organisation)  # ✅ Check organisation
        except CustomUser.DoesNotExist:
            user = None

        if user and user.password == password:  # ✅ Compare plain text password (no hashing)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # ✅ Store user ID instead of organisation name
            request.session['organisation_id'] = user.id  
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials', 'organisation': organisation})

    return render(request, 'login.html', {'organisation': organisation})

def user_logout(request):
    request.session.flush()
    return redirect('home')   

def home(request):
    events = AddEvents.objects.order_by('-event_date')  
    return render(request, 'home.html', {'events': events})

def eventdetails(request,pk):
    events=AddEvents.objects.get(pk=pk)
    return render(request,'eventdetails.html',{'obj':events})

def dashboard(request):
    organisation_id = request.session.get('organisation_id')  # Get organisation ID
    if not organisation_id:
        return redirect('login')

    organisation = CustomUser.objects.get(id=organisation_id)  # Get the logged-in organisation
    events = AddEvents.objects.filter(organisation=organisation)  #  Filter events by organisation instance

    return render(request, "dashboard.html", {"events": events, "organisation": organisation.organisation})




def organisedevents(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to view events.")
        return redirect('login')

    organisation = request.session.get('organisation')
    events = AddEvents.objects.filter(organisation=request.user)

    return render(request, 'organised-events.html', {'events': events})

def delete_event(request, pk):
    #event = get_object_or_404(AddEvents, id=event_id)
    event=get_object_or_404(AddEvents, pk=pk)
    event.delete()
    return redirect('organisedevents')
def addevent(request):
    if request.method == "POST":
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        start_time_12hr = request.POST.get('start_time')
        end_time_12hr = request.POST.get('end_time')
        event_venue = request.POST.get('event_venue')
        event_description = request.POST.get('event_description')
        registration_fee = request.POST.get('registration_fee')
        event_poster = request.FILES.get('event_poster')
        if start_time_12hr:
            start_time = datetime.strptime(start_time_12hr, "%I:%M %p").time()

        if end_time_12hr:
            end_time = datetime.strptime(end_time_12hr, "%I:%M %p").time()

        organisation_id = request.session.get('organisation_id')  # Retrieve user ID
        if not organisation_id:
            messages.error(request, "Organisation not found. Please log in again.")
            return redirect('login')

        organisation = CustomUser.objects.get(id=organisation_id)  # Fetch organisation by ID

        AddEvents.objects.create(
            event_name=event_name,
            event_date=event_date,
            start_time=start_time,
            end_time=end_time,
            event_venue=event_venue,
            event_description=event_description,
            registration_fee=registration_fee,
            event_poster=event_poster,
            organisation=organisation
        )

        messages.success(request, "Event added successfully!")
        return redirect('dashboard')

    return render(request, 'add-event.html')




def edit_event(request, pk):
    event = get_object_or_404(AddEvents, id=pk)  # Using get_object_or_404 for better error handling
    if request.method == 'POST':
        print(request.POST)
        event.event_name = request.POST.get('event_name')
        event.event_date = request.POST.get('event_date')
        start_time_12hr = request.POST.get('start_time')  # Example: "12:30 PM"
        end_time_12hr = request.POST.get('end_time') 
        event.event_venue = request.POST.get('event_venue')
        event.event_description = request.POST.get('event_description')
        event.registration_fee = request.POST.get('registration_fee')
        AddEvents.objects.update(event_name=event.event_name,event_date=event.event_date,event_venue=event.event_venue,event_description=event.event_description,registration_fee=event.registration_fee)

        if start_time_12hr:
            event.start_time = datetime.strptime(start_time_12hr, "%I:%M %p").time()

        if end_time_12hr:
            event.end_time = datetime.strptime(end_time_12hr, "%I:%M %p").time()
        # Only update the event_poster if a new one is provided
        if request.FILES.get('event_poster'):
            event.event_poster = request.FILES.get('event_poster')

        event.save()
        messages.success(request, 'Event updated successfully.')
        return redirect('organisedevents')
    

    return render(request, 'edit.html', {'obj': event})





def register(request, pk):
    event=get_object_or_404(AddEvents, id=pk)
    if request.method=='POST':
        participant_name=request.POST.get('participant_name')
        participant_email=request.POST.get('participant_email')
        participant_no=request.POST.get('participant_no')
        participant_clg=request.POST.get('participant_clg')
        participant_dept=request.POST.get('participant_dept')
        participant_sem=request.POST.get('participant_sem')
        
        Register.objects.create(event_id=event, participant_name=participant_name,participant_email=participant_email,participant_no=participant_no,participant_clg=participant_clg,participant_dept=participant_dept,participant_sem=participant_sem)
        #register.save()
        messages.success(request, 'Registered successfully.')
        return redirect('home')
        
        #return render(request, 'add-event.html', {'message': 'Event added successfully!'})
    return render(request,'register.html',{'event':event})





def reg_detail(request, event_id):
    event = get_object_or_404(AddEvents, id=event_id)  # Fetch all events
    participants = Register.objects.filter(event_id=event)
    return render(request,'reg_detail.html',{'event':event, "participants": participants})

  