from django.shortcuts import render, redirect, HttpResponse
from .forms import SignUpForm, ProfileForm, AuthKeyCollectForm, AuthKeyVerifyForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from passlib.hash import pbkdf2_sha256
from . models import AuthKeyModel
from . utility import encode_string, decode_string, CloudFlareWork
from hurry.filesize import size, alternative
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
# Create your views here.


def homepage(request):
    return render(request, 'dashboard/homepage.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            password = form.cleaned_data.get('password1')
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')

    else:
        form = SignUpForm()
        profile_form = ProfileForm()

    return render(request, 'dashboard/signup.html', {'form': form, 'profile_form': profile_form})


def login_request(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}!')
            return redirect('home')

    else:
        form = AuthenticationForm()
    front = {'form': form}
    return render(request, 'dashboard/login.html', front)


def logout_request(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        logout(request)
        return render(request, 'dashboard/logout.html')


def collect_auth_key(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthKeyCollectForm(request.POST)
        if form.is_valid():
            auth_key = request.POST.get('auth_key')
            '''enc_auth_key = pbkdf2_sha256.encrypt(auth_key)'''
            enc_auth_key = encode_string(auth_key)
            if not AuthKeyModel.objects.filter(user=request.user):
                AuthKeyModel.objects.create(
                    user=request.user, auth_key=enc_auth_key)
                messages.success(request, 'API key stored successfully')
                return redirect('home')

            else:

                messages.info(
                    request, "You already have an API key please head to cloudflare if you have forgotten what it was.")
                return redirect('auth_key_collect')
        else:
            messages.error(request, 'PLease enter a valid input')
            return redirect('auth_key_collect')
    else:
        form = AuthKeyCollectForm()
    front = {
        'form': form
    }
    return render(request, 'dashboard/auth_key_collect.html', front)


def waf_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
        messages.info(request, 'You need to login first')
    if AuthKeyModel.objects.filter(user=request.user):
        auth_user = AuthKeyModel.objects.get(user=request.user)
        enc_api_key = auth_user.auth_key
        dec_api_key = decode_string(enc_api_key)
        cf = CloudFlareWork(dec_api_key, request.user.email)
        data = cf.zone_list()
        if len(data) == 0:
            messages.info(
                request, 'looks like you do not have any domains registered with us')
        front = {
            'zone_list': data
        }
        return render(request, 'dashboard/waf_home.html', front)
    else:
        messages.info(
            request, 'You have not provided any API key for this account')
        return redirect('auth_key_collect')


def get_auth_id_helper(request):
    auth_user = AuthKeyModel.objects.get(user=request.user)
    enc_api_key = auth_user.auth_key
    dec_api_key = decode_string(enc_api_key)
    return dec_api_key


def zone_details(request, zone_name):
    api_key = get_auth_id_helper(request)

    # passing in the details of the zone
    cf = CloudFlareWork(api_key, request.user.email)

    # passing the total data to the template
    data = cf.get_zone_analytics_24_hrs(zone_name)
    data_served_int = data.get('bandwidth').get('all')
    data_served = size(data_served_int, system=alternative)
    percent_cached_float = (data.get('bandwidth').get(
        'cached')/data.get('bandwidth').get('all'))*100
    percent_cached = float("{:.2f}".format(percent_cached_float))
    data_cached_int = data.get('bandwidth').get('cached')
    data_cached = size(data_cached_int, system=alternative)

    # getting data for graph

    since_until, unique_list = cf.get_zone_analytics_timeseries_visitors(
        zone_name)
    _, requests_list = cf.get_zone_analytics_timeseries_requests(
        zone_name)

    data_served_graph = cf.get_zone_analytics_timeseries_data_served(zone_name)
    percent_cached_graph = cf.get_zone_analytics_timeseries_percent_cached(
        zone_name)

    data_cached_graph = cf.get_zone_analytics_timeseries_data_cached(zone_name)

    front = {
        'data': data,
        'data_served': data_served,
        'percent_cached': percent_cached,
        'data_cached': data_cached,
        'requests_list': requests_list,
        'since_until': since_until,
        'unique_list': unique_list,
        'data_served_graph': data_served_graph,
        'percent_cached_graph': percent_cached_graph,
        'data_cached_graph': data_cached_graph
    }
    return render(request, 'dashboard/waf_detail.html', front)
