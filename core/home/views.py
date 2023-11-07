from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from django.contrib import messages, auth
from django.contrib.auth.models import User
from .models import *
from django.core.mail import send_mail

# Create your views here.

def index(request):

  listings = Listing.objects.order_by('-list_date').filter(is_published=True)

  context = {
    
    'listings': listings
  }
  return render(request, 'index.html' , context)

def services(request):

  return render(request, 'services.html')

    

def contactus(request):
    return render(request, 'contactus.html')

def realtors(request):
    # Get all realtors
    realtors = Realtor.objects.order_by('-hire_date')

    # Get MVP
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }
    return render(request, 'realtor.html', context)

def listings(request):
  listings = Listing.objects.order_by('-list_date').filter(is_published=True)

  context = {
    'listings': listings
  }

  return render(request, 'properties.html', context)

def dashboard(request):
  current_user = request.user
  user_listings = mylistings.objects.filter(username=current_user)
  listing_ids = [my__listing.contact_object.listing_id for my__listing in user_listings]
  my_listingss = Listing.objects.filter(id__in=listing_ids)
 
  context = {
    'listings': my_listingss
  }

  return render(request, 'dashboard.html', context)

def property_single(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)

  context = {
    'listing': listing
  }

  return render(request, 'property-single.html', context)


def about(request):
    

    return render(request, 'about.html')

def realtorregistration(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    description = request.POST.get('description')
    is_mvp = request.POST.get('is_mvp')
    if is_mvp == "True":
      is_mvp = True
    else:
      is_mvp = False
    realtor_image = request.FILES.get('photo')
    Realtor.objects.create(name=name,email=email,description=description,is_mvp=is_mvp,photo=realtor_image)

    return redirect('home')
  else:
    return render(request,'realtorregistration.html')


def contact(request):
  if request.method == 'POST':
    listing_id = request.POST['listing_id']
    listing = request.POST['listing']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    message = request.POST['message']
    user_id = request.POST['user_id']
    realtor_email = request.POST['realtor_email']

    #  Check if user has made inquiry already
    if request.user.is_authenticated:
      user_id = request.user.id
      has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
      if has_contacted:
        messages.error(request, 'You have already made an inquiry for this listing')
        return redirect('/property-single/'+listing_id)

    contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id )

    contact.save()

    mylistings.objects.create(
      contact_object = contact,
      username = request.user
    )

    # Send email
    # send_mail(
    #   'Property Listing Inquiry',
    #   'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
    #   'iprabhatdev@gmail.com',
    #   [realtor_email, 'random@gmail.com'],
    #   fail_silently=False
    # )

    messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
    return redirect('/property-single/'+listing_id)
  

def register(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is being used')
          return redirect('register')
        else:
          # Looks good
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
          # Login after register
          # auth.login(request, user)
          # messages.success(request, 'You are now logged in')
          # return redirect('index')
          user.save()
          messages.success(request, 'You are now registered and can log in')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('register')
  else:
    return render(request, 'register.html')
  



def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'You are now logged in')
      return redirect('home')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
  else:
    return render(request, 'login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('home')
  else:
    return redirect('home')

# def dashboard(request):
#   user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

#   context = {
#     'contacts': user_contacts
#   }
#   return render(request, 'dashboard.html', context)

# views.py

# def search_listings(request):
#     if request.method == 'GET':
#         form = request.GET['search_query']
#         search_query = form.cleaned_data.get('search_query', '')

#         # Perform the search using the search_query
#         listings = Listing.objects.filter(description__icontains=search_query, is_published=True)

#         context = {
#             'listings': listings,
#         }

#         return render(request, 'search.html', context)
    

def search_listings(request):
  queryset_list = Listing.objects.order_by('-list_date')

  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  # City
  if 'city' in request.GET:
    city = request.GET['city']
    if city:
      queryset_list = queryset_list.filter(city__iexact=city)

  # State
  if 'state' in request.GET:
    state = request.GET['state']
    if state:
      queryset_list = queryset_list.filter(state__iexact=state)

  # # Bedrooms
  # if 'bedrooms' in request.GET:
  #   bedrooms = request.GET['bedrooms']
  #   if bedrooms:
  #     queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

  # # Price
  # if 'price' in request.GET:
  #   price = request.GET['price']
  #   if price:
  #     queryset_list = queryset_list.filter(price__lte=price)

  context = {
    # 'state_choices': state_choices,
    # 'bedroom_choices': bedroom_choices,
    # 'price_choices': price_choices,
    'listings': queryset_list,
    'values': request.GET
  }

  return render(request, 'search.html', context)
    
    