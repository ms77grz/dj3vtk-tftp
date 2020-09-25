from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SearchSubscriber
from subprocess import Popen, PIPE, STDOUT
from dj3pro.settings import DEVCONS


def home(request):
    return render(request, 'equipment_accounting/home.html')


@login_required
def search(request):
    if request.method == 'POST':
        form = SearchSubscriber(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data.get('account_number')
            command = ["ag", "-B 1", "--hidden", "--nonumbers",
                       f"{account_number}", DEVCONS]
            process = Popen(command, stdout=PIPE, stderr=STDOUT)
            output = process.stdout.read().decode()
            output = ''.join(output)
            output = output.replace(
                DEVCONS, '')
            output = output.split('\n')
            if len(output) < 1:
                output = None
            form = SearchSubscriber()
            return render(request, 'equipment_accounting/search.html', {'form': form, 'output': output})
    else:
        form = SearchSubscriber()
    return render(request, 'equipment_accounting/search.html', {'form': form})


def about(request):
    return render(request, 'equipment_accounting/about.html', {'title': 'About'})
