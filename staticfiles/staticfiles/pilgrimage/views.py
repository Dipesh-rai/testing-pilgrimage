from django.shortcuts import render,redirect
from service.models import Service
from home.models import Home,Commitment,Short_description
from news.models import News
from blogg.models import Blogpages, Blog
from aboutpage.models import About,Ourmission,Whytravel
from sacredsite.models import Sacredsite,Sacredpage, TourBooking, Itinerary, Faq, Discounts,Gallery
from sacredsite.forms import TourBookingForm
from category.models import Category,Category_page
from contactpage.models import Contact
from contactpage.form import ContactForm
from logo_footer.models import Footer, Logo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render,redirect
from subscription.forms import SubsciptionForm
from subscription.models import Subscriber
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, get_object_or_404 
from django.core.mail import EmailMultiAlternatives

@csrf_exempt
def check_email(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        email = json.loads(request.body).get('email', '')
        exists = Subscriber.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def homepage(request):
    category=request.GET.get('category')
    if category==None:
        sacredData = Sacredsite.objects.filter(is_published=True).order_by('-id')[:6]
    else:
        sacredData = Sacredsite.objects.filter(Category__sacred_slug=category)
    homedata=Home.objects.all()
    logo=Logo.objects.all()
    sacredpage=Sacredpage.objects.all()
    newsData=News.objects.all()
    servicesData=Service.objects.all().order_by('-id')[:4]
    categories=Category.objects.all()
    commitment=Commitment.objects.all()
    shortdes=Short_description.objects.all()
    footer=Footer.objects.all()
    contactpage=Contact.objects.all()
    blog=Blog.objects.all().order_by('-id')[:3]
    blogpage=Blogpages.objects.all()
    category_page=Category_page.objects.all()
    # for a in servicesData:
    #     print(a.service_icon)
    # print(servicesData)
    # Handle AJAX requests
    form=SubsciptionForm()
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Email check request
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                if 'email' in data:
                    exists = Subscriber.objects.filter(email=data['email']).exists()
                    return JsonResponse({'exists': exists})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Subscription request
        form = SubsciptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'exists', 'message': 'This email is already subscribed.'})
            
            subscriber = form.save()
            
            try:
                # Email sending with HTML and text versions
                html_content = render_to_string('emails/subscription_confirmation.html', {'email': email})
                text_content = render_to_string('emails/subscription_confirmation.txt', {'email': email})
                
                msg = EmailMultiAlternatives(
                    subject="Thanks for Subscribing",
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                    bcc=["nirvanajourney1832@gmail.com"]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log the error
                return JsonResponse({'status': 'error', 'message': 'Subscription saved, but email failed to send.'})
        else:
            return JsonResponse({'status': 'invalid', 'message': 'Please enter a valid email.'}, status=400)
    
    data={
        'servicesData':servicesData,
        'newsData':newsData,
        'logo':logo,
        'categories':categories,
        'sacredData':sacredData,
        'homedata':homedata,
        'sacredpage':sacredpage,
        'commitment':commitment,
        'shortdes':shortdes,
        'blog':blog,
        'blogpage':blogpage,
        'category_page':category_page,
        'footer':footer,
        'contactpage':contactpage,
        'form':form,
    }
    return render(request,"index.html",data)

def sacredsite(request):
    category=request.GET.get('category')
    if category==None:
        sacredData = Sacredsite.objects.order_by('-id').filter(is_published=True)
    else:
        sacredData = Sacredsite.objects.filter(Category__sacred_slug=category)
    paginator=Paginator(sacredData,6)
    page_number=request.GET.get('page')
    try:
        sacredDatafinal=paginator.page(page_number)
    except PageNotAnInteger:
        sacredDatafinal=paginator.page(1)
    except EmptyPage:
        sacredDatafinal=paginator.page(paginator.num_pages)
    logo=Logo.objects.all()
    categories=Category.objects.all()
    contactpage=Contact.objects.all()
    footer=Footer.objects.all()

    form=SubsciptionForm()
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Email check request
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                if 'email' in data:
                    exists = Subscriber.objects.filter(email=data['email']).exists()
                    return JsonResponse({'exists': exists})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Subscription request
        form = SubsciptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'exists', 'message': 'This email is already subscribed.'})
            
            subscriber = form.save()
            
            try:
                # Email sending with HTML and text versions
                html_content = render_to_string('emails/subscription_confirmation.html', {'email': email})
                text_content = render_to_string('emails/subscription_confirmation.txt', {'email': email})
                
                msg = EmailMultiAlternatives(
                    subject="Thanks for Subscribing",
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                    bcc=["nirvanajourney1832@gmail.com"]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log the error
                return JsonResponse({'status': 'error', 'message': 'Subscription saved, but email failed to send.'})
        else:
            return JsonResponse({'status': 'invalid', 'message': 'Please enter a valid email.'}, status=400)
    data={
        'sacredData':sacredDatafinal,
        'categories':categories,
        'current_category':category,
        'contactpage':contactpage,
        'logo':logo,
        'form':form,
        'footer':footer,
    }
    return render(request,"sacredsite.html",data)

def blog(request):
    category=request.GET.get('category')
    if category==None:
        sacredData = Sacredsite.objects.order_by('-id').filter(is_published=True)
    else:
        sacredData = Sacredsite.objects.filter(Category__sacred_slug=category)
    blogpage=Blogpages.objects.all()
    blog=Blog.objects.all()
    logo=Logo.objects.all()
    categories=Category.objects.all()
    contactpage=Contact.objects.all()
    paginator=Paginator(blog,6)
    page_number=request.GET.get('page')
    try:
        blogfinal=paginator.page(page_number)
    except PageNotAnInteger:
        blogfinal=paginator.page(1)
    except EmptyPage:
        blogfinal=paginator.page(paginator.num_pages)
    categories=Category.objects.all()
    contactpage=Contact.objects.all()
    form=SubsciptionForm()
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Email check request
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                if 'email' in data:
                    exists = Subscriber.objects.filter(email=data['email']).exists()
                    return JsonResponse({'exists': exists})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Subscription request
        form = SubsciptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'exists', 'message': 'This email is already subscribed.'})
            
            subscriber = form.save()
            
            try:
                # Email sending with HTML and text versions
                html_content = render_to_string('emails/subscription_confirmation.html', {'email': email})
                text_content = render_to_string('emails/subscription_confirmation.txt', {'email': email})
                
                msg = EmailMultiAlternatives(
                    subject="Thanks for Subscribing",
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                    bcc=["nirvanajourney1832@gmail.com"]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log the error
                return JsonResponse({'status': 'error', 'message': 'Subscription saved, but email failed to send.'})
        else:
            return JsonResponse({'status': 'invalid', 'message': 'Please enter a valid email.'}, status=400)
    footer=Footer.objects.all()
    data={
        'sacredData':sacredData,
        'categories':categories,
        'blogpage':blogpage,
        'blog':blogfinal,
        'contactpage':contactpage,
        'logo':logo,
        'form':form,
        'footer':footer,
    }
    return render(request,"blog.html",data)

def blogpages(request,slug):
    category=request.GET.get('category')
    if category==None:
        sacredData = Sacredsite.objects.order_by('-id').filter(is_published=True)
    else:
        sacredData = Sacredsite.objects.filter(Category__sacred_slug=category)
    categories=Category.objects.all()
    blogDetails=Blog.objects.get(blog_slug=slug)
    logo=Logo.objects.all()
    blog=Blog.objects.all()
    contactpage=Contact.objects.all()
    form=SubsciptionForm()
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Email check request
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                if 'email' in data:
                    exists = Subscriber.objects.filter(email=data['email']).exists()
                    return JsonResponse({'exists': exists})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Subscription request
        form = SubsciptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'exists', 'message': 'This email is already subscribed.'})
            
            subscriber = form.save()
            
            try:
                # Email sending with HTML and text versions
                html_content = render_to_string('emails/subscription_confirmation.html', {'email': email})
                text_content = render_to_string('emails/subscription_confirmation.txt', {'email': email})
                
                msg = EmailMultiAlternatives(
                    subject="Thanks for Subscribing",
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                    bcc=["nirvanajourney1832@gmail.com"]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log the error
                return JsonResponse({'status': 'error', 'message': 'Subscription saved, but email failed to send.'})
        else:
            return JsonResponse({'status': 'invalid', 'message': 'Please enter a valid email.'}, status=400)
    footer=Footer.objects.all()
    related_blog=blogDetails.get_related_blog()[:3]
    data={
        'categories':categories,
        'blogDetails':blogDetails,
        'logo':logo,
        'sacredData':sacredData,
        'blog':blog,
        'contactpage':contactpage,
        'form':form,
        'footer':footer,
        'related_blog':related_blog
    }
    return render(request,"blogpages.html",data)

def newsDetails(request,slug):
    category=request.GET.get('category')
    if category==None:
        sacredData = Sacredsite.objects.order_by('-id').filter(is_published=True)
    else:
        sacredData = Sacredsite.objects.filter(Category__sacred_slug=category)
    logo=Logo.objects.all()
    newsDetails=News.objects.get(news_slug=slug)
    categories=Category.objects.all()
    contactpage=Contact.objects.all()
    form=SubsciptionForm()
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Email check request
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                if 'email' in data:
                    exists = Subscriber.objects.filter(email=data['email']).exists()
                    return JsonResponse({'exists': exists})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Subscription request
        form = SubsciptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'exists', 'message': 'This email is already subscribed.'})
            
            subscriber = form.save()
            
            try:
                # Email sending with HTML and text versions
                html_content = render_to_string('emails/subscription_confirmation.html', {'email': email})
                text_content = render_to_string('emails/subscription_confirmation.txt', {'email': email})
                
                msg = EmailMultiAlternatives(
                    subject="Thanks for Subscribing",
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                    bcc=["nirvanajourney1832@gmail.com"]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log the error
                return JsonResponse({'status': 'error', 'message': 'Subscription saved, but email failed to send.'})
        else:
            return JsonResponse({'status': 'invalid', 'message': 'Please enter a valid email.'}, status=400)
    footer=Footer.objects.all()
    data={
        'newsDetails':newsDetails,
        'categories':categories,
        'sacredData':sacredData,
        'contactpage':contactpage,
        'logo':logo,
        'form':form,
        'footer':footer,
    }
    return render(request,"newsdetails.html",data)

def journeyDetails(request, slug):
    # Get the sacred site details
    journey_details = get_object_or_404(Sacredsite, sacred_slug=slug)
    
    # Get related data
    itineraries = journey_details.itineraries.all()
    faq = journey_details.faqs.all()
    logo=Logo.objects.all()
    discounts = journey_details.discounts.all()
    discount=journey_details.discount.all()
    gallery=journey_details.gallery.all()
    categories = Category.objects.all()
    contactpage = Contact.objects.all()
    footer = Footer.objects.all()
    related_sites = journey_details.get_related_sites()[:3]
    # Handle category filtering
    category = request.GET.get('category')
    sacredData = Sacredsite.objects.filter(is_published=True)
    if category:
        sacredData = sacredData.filter(Category__sacred_slug=category)
    
    # Initialize forms
    booking_form = TourBookingForm(initial={'package': journey_details.id})
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Check if it's a booking submission (has package field)
        if 'package' in request.POST:
            booking_form = TourBookingForm(request.POST)
            if booking_form.is_valid():
                booking = booking_form.save()
                try:
                    send_booking_confirmation(booking, journey_details)
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Inquiry confirmed! Check your email for details.'
                    })
                except Exception as e:
                    print(f"Booking email failed: {e}")
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Inquiry saved but confirmation email failed.'
                    })
            else:
                return JsonResponse({
                    'status': 'invalid',
                    'message': 'Please correct the errors',
                    'errors': booking_form.errors
                })

    form=SubsciptionForm()
    if request.method == "POST" and 'booking_form' in request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Email check request
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                if 'email' in data:
                    exists = Subscriber.objects.filter(email=data['email']).exists()
                    return JsonResponse({'exists': exists})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Subscription request
        form = SubsciptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'exists', 'message': 'This email is already subscribed.'})
            
            subscriber = form.save()
            
            try:
                # Email sending with HTML and text versions
                html_content = render_to_string('emails/subscription_confirmation.html', {'email': email})
                text_content = render_to_string('emails/subscription_confirmation.txt', {'email': email})
                
                msg = EmailMultiAlternatives(
                    subject="Thanks for Subscribing",
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                    bcc=["nirvanajourney1832@gmail.com"]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log the error
                return JsonResponse({'status': 'error', 'message': 'Subscription saved, but email failed to send.'})
        else:
            return JsonResponse({'status': 'invalid', 'message': 'Please enter a valid email.'}, status=400)
    
    # Handle separate AJAX subscription requests
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'email' in request.POST:
        subscription_form = SubsciptionForm(request.POST)
        if subscription_form.is_valid():
            email = subscription_form.cleaned_data['email']
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({
                    'status': 'exists',
                    'message': 'This email is already subscribed.'
                })
            subscription_form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'You are successfully subscribed!'
            })
        return JsonResponse({
            'status': 'invalid',
            'message': 'Please enter a valid email.'
        })
    
    context = {
        'journeyDetails': journey_details,
        'logo':logo,
        'itineraries': itineraries,
        'faq': faq,
        'discounts': discounts,
        'gallery':gallery,
        'categories': categories,
        'sacredData': sacredData,
        'contactpage': contactpage,
        'footer': footer,
        'booking_form': booking_form,
        'form': form,
        'discount':discount,
        'related_sites':related_sites,
    }
    return render(request, "viewjourney.html", context)

def send_booking_confirmation(booking, package):
    context = {
        'booking': booking,
        'package': package,
        'itineraries': package.itineraries.all(),
        'faqs': package.faqs.all(),
    }
    
    msg_html = render_to_string('emails/booking_confirmation.html', context)
    msg_plain = render_to_string('emails/booking_confirmation.txt', context)
    
    send_mail(
        f'Booking Confirmation: {package.sacred_name}',
        msg_plain,
        settings.DEFAULT_FROM_EMAIL,
        [booking.email,'nirvanajourney1832@gmail.com'],
        html_message=msg_html,
        fail_silently=False,
    )

def categorypages(request):
    category=request.GET.get('category')
    if category==None:
        sacredData = Sacredsite.objects.order_by('-id').filter(is_published=True)
    else:
        sacredData = Sacredsite.objects.filter(Category__sacred_slug=category)
   
    categorypage=Category_page.objects.all()
    logo=Logo.objects.all()
    categories=Category.objects.all()
    contactpage=Contact.objects.all()
    paginator=Paginator(categories,6)
    page_number=request.GET.get('page')
    try:
        categoriesfinal=paginator.page(page_number)
    except PageNotAnInteger:
        categoriesfinal=paginator.page(1)
    except EmptyPage:
        categoriesfinal=paginator.page(paginator.num_pages)

    form=SubsciptionForm()
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Email check request
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                if 'email' in data:
                    exists = Subscriber.objects.filter(email=data['email']).exists()
                    return JsonResponse({'exists': exists})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Subscription request
        form = SubsciptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'exists', 'message': 'This email is already subscribed.'})
            
            subscriber = form.save()
            
            try:
                # Email sending with HTML and text versions
                html_content = render_to_string('emails/subscription_confirmation.html', {'email': email})
                text_content = render_to_string('emails/subscription_confirmation.txt', {'email': email})
                
                msg = EmailMultiAlternatives(
                    subject="Thanks for Subscribing",
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                    bcc=["nirvanajourney1832@gmail.com"]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log the error
                return JsonResponse({'status': 'error', 'message': 'Subscription saved, but email failed to send.'})
        else:
            return JsonResponse({'status': 'invalid', 'message': 'Please enter a valid email.'}, status=400)
    footer=Footer.objects.all()
    data={
        'categorypage':categorypage,
        'logo':logo,
        'categories':categoriesfinal,
        'sacredData':sacredData,
        'contactpage':contactpage,
        'form':form,
        'footer':footer,
    }
    return render(request,"categories.html",data)


def contact(request):
    category=request.GET.get('category')
    if category==None:
        sacredData = Sacredsite.objects.order_by('-id').filter(is_published=True)
    else:
        sacredData = Sacredsite.objects.filter(Category__sacred_slug=category)
    contactpage=Contact.objects.all()
    categories=Category.objects.all()
    logo=Logo.objects.all()
    forms=ContactForm
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        forms=ContactForm(request.POST)
        if forms.is_valid():
            name=forms.cleaned_data['name']
            email=forms.cleaned_data['email']
            content=forms.cleaned_data['content']
            try:
                html_content=render_to_string('emails/contact.html',{
                    'name':name,
                    'email':email,
                    'content':content,
                })
                text_content = f"""
                    Name:{name}
                    Email:{email}
                    Message:{content}
                """
                send_mail(
                    subject=f"New Contact Form Submission from {name}",
                    message=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['nirvanajourney1832@gmail.com'],
                    html_message=html_content,
                    fail_silently=False,
                    )
                 # 2. NEW: Confirmation email to CLIENT
                client_html = render_to_string('emails/contact_confirmation.html', {
                   'name': name,
                    'email':email,
                    'content':content,
                })
        
                send_mail(
                    subject="Thank you for contacting us",
                    message="We've received your message and will respond soon",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],  # Client's email from form
                    html_message=client_html,
                )
                return JsonResponse({
                    'success':True,
                    'message':'Thank you! Your message has been sent successfully.'
                })
            except Exception as e:
                print(f"Email sending failed: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'Message saved but email failed to send.',
                'error': str(e)
            }, status=500)
        else:
            return JsonResponse({
                'success':False,
                'errors':forms.errors
            })

# subscribtion
    form=SubsciptionForm()
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Email check request
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                if 'email' in data:
                    exists = Subscriber.objects.filter(email=data['email']).exists()
                    return JsonResponse({'exists': exists})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Subscription request
        form = SubsciptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'exists', 'message': 'This email is already subscribed.'})
            
            subscriber = form.save()
            
            try:
                # Email sending with HTML and text versions
                html_content = render_to_string('emails/subscription_confirmation.html', {'email': email})
                text_content = render_to_string('emails/subscription_confirmation.txt', {'email': email})
                
                msg = EmailMultiAlternatives(
                    subject="Thanks for Subscribing",
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                    bcc=["nirvanajourney1832@gmail.com"]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log the error
                return JsonResponse({'status': 'error', 'message': 'Subscription saved, but email failed to send.'})
        else:
            return JsonResponse({'status': 'invalid', 'message': 'Please enter a valid email.'}, status=400)
    footer=Footer.objects.all()

    data={
        'categories':categories,
        'sacredData':sacredData,
        'logo':logo,
        'contactpage':contactpage,
        'form':form,
        'forms':forms,
        'footer':footer,
    }
    return render(request,"contact.html",data)

def saveenquiry(request):
    category=request.GET.get('category')
    logo=Logo.objects.all()
    if category==None:
        sacredData = Sacredsite.objects.order_by('-id').filter(is_published=True)
    else:
        sacredData = Sacredsite.objects.filter(Category__sacred_slug=category)
   
    categories=Category.objects.all()
    data={
        'categories':categories,
        'sacredData':sacredData,
        'logo':logo,
    }
    return render(request,"contact.html",data)

# 
def about(request):
    category=request.GET.get('category')
    if category==None:
        sacredData = Sacredsite.objects.order_by('-id').filter(is_published=True)
    else:
        sacredData = Sacredsite.objects.filter(Category__sacred_slug=category)
    categories=Category.objects.all()
    logo=Logo.objects.all()
    about=About.objects.all()
    contactpage=Contact.objects.all()
    form=SubsciptionForm()
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Email check request
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                if 'email' in data:
                    exists = Subscriber.objects.filter(email=data['email']).exists()
                    return JsonResponse({'exists': exists})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Subscription request
        form = SubsciptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'exists', 'message': 'This email is already subscribed.'})
            
            subscriber = form.save()
            
            try:
                # Email sending with HTML and text versions
                html_content = render_to_string('emails/subscription_confirmation.html', {'email': email})
                text_content = render_to_string('emails/subscription_confirmation.txt', {'email': email})
                
                msg = EmailMultiAlternatives(
                    subject="Thanks for Subscribing",
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                    bcc=["nirvanajourney1832@gmail.com"]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log the error
                return JsonResponse({'status': 'error', 'message': 'Subscription saved, but email failed to send.'})
        else:
            return JsonResponse({'status': 'invalid', 'message': 'Please enter a valid email.'}, status=400)
    footer=Footer.objects.all()
    data={
        'categories':categories,
        'sacredData':sacredData,
        'about':about,
        'logo':logo,
        'contactpage':contactpage,
        'form':form,
        'footer':footer,
    }
    return render(request,"about.html",data)

def activities(request,exception):
    category=request.GET.get('category')
    if category==None:
        sacredData = Sacredsite.objects.order_by('-id').filter(is_published=True)
    else:
        sacredData = Sacredsite.objects.filter(Category__sacred_slug=category)
    categories=Category.objects.all()
    about=About.objects.all()
    contactpage=Contact.objects.all()
    logo=Logo.objects.all()
    form= SubsciptionForm()
    if request.method == "POST":
        form = SubsciptionForm(request.POST)
        if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = SubsciptionForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                if Subscriber.objects.filter(email=email).exists():
                    return JsonResponse({'status': 'exists', 'message': 'This email is already subscribed.'})
                else:
                    form.save()
                    return JsonResponse({'status': 'success', 'message': 'You are successfully subscribed!'})
            else:
                return JsonResponse({'status': 'invalid', 'message': 'Please enter a valid email.'})
    footer=Footer.objects.all()
    data={
        'categories':categories,
        'sacredData':sacredData,
        'about':about,
        'logo':logo,
        'contactpage':contactpage,
        'form':form,
        'footer':footer,
    }
    return render(request,"activities.html",data)

def ourmission(request):
    category=request.GET.get('category')
    if category==None:
        sacredData = Sacredsite.objects.order_by('-id').filter(is_published=True)
    else:
        sacredData = Sacredsite.objects.filter(Category__sacred_slug=category)
    categories=Category.objects.all()
    ourmissiondetails=Ourmission.objects.all()
    contactpage=Contact.objects.all()
    logo=Logo.objects.all()
    form=SubsciptionForm()
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Email check request
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                if 'email' in data:
                    exists = Subscriber.objects.filter(email=data['email']).exists()
                    return JsonResponse({'exists': exists})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Subscription request
        form = SubsciptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'exists', 'message': 'This email is already subscribed.'})
            
            subscriber = form.save()
            
            try:
                # Email sending with HTML and text versions
                html_content = render_to_string('emails/subscription_confirmation.html', {'email': email})
                text_content = render_to_string('emails/subscription_confirmation.txt', {'email': email})
                
                msg = EmailMultiAlternatives(
                    subject="Thanks for Subscribing",
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                    bcc=["nirvanajourney1832@gmail.com"]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log the error
                return JsonResponse({'status': 'error', 'message': 'Subscription saved, but email failed to send.'})
        else:
            return JsonResponse({'status': 'invalid', 'message': 'Please enter a valid email.'}, status=400)
    footer=Footer.objects.all()
    data={
        'categories':categories,
        'sacredData':sacredData,
        'logo':logo,
        'ourmissiondetails':ourmissiondetails,
        'contactpage':contactpage,
        'form':form,
        'footer':footer,
    }
    return render(request,"ourmission.html",data)
# 


def whytravel(request):
    category=request.GET.get('category')
    if category==None:
        sacredData = Sacredsite.objects.order_by('-id').filter(is_published=True)
    else:
        sacredData = Sacredsite.objects.filter(Category__sacred_slug=category)
    categories=Category.objects.all()
    logo=Logo.objects.all()
    ourmission=Whytravel.objects.all()
    contactpage=Contact.objects.all()
    form=SubsciptionForm()
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Email check request
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                if 'email' in data:
                    exists = Subscriber.objects.filter(email=data['email']).exists()
                    return JsonResponse({'exists': exists})
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Subscription request
        form = SubsciptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'exists', 'message': 'This email is already subscribed.'})
            
            subscriber = form.save()
            
            try:
                # Email sending with HTML and text versions
                html_content = render_to_string('emails/subscription_confirmation.html', {'email': email})
                text_content = render_to_string('emails/subscription_confirmation.txt', {'email': email})
                
                msg = EmailMultiAlternatives(
                    subject="Thanks for Subscribing",
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})
            except Exception as e:
                print(f"Email sending failed: {e}")  # Log the error
                return JsonResponse({'status': 'error', 'message': 'Subscription saved, but email failed to send.'})
        else:
            return JsonResponse({'status': 'invalid', 'message': 'Please enter a valid email.'}, status=400)
    footer=Footer.objects.all()
    data={
        'categories':categories,
        'sacredData':sacredData,
        'logo':logo,
        'ourmission':ourmission,
        'contactpage':contactpage,
        'form':form,
        'footer':footer,
    }
    return render(request,"whytravelwithus.html",data)