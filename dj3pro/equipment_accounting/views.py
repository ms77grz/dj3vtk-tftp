from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SearchSubscriber
from subprocess import Popen, PIPE, STDOUT


@login_required
def home(request):
    if request.method == 'POST':
        form = SearchSubscriber(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data.get('account_number')
            command = ["ag", "-B 1", "--hidden", "--nonumbers", f"{account_number}", "/home/magax/webapps/networking/ftth/ftth_data"]
            process = Popen(command, stdout=PIPE, stderr=STDOUT)
            output = process.stdout.read().decode()
            output = ''.join(output)
            output = output.replace('/home/magax/webapps/networking/ftth/ftth_data/', '')
            output = output.split('\n')
            for p in output:
                messages.success(request, f"{p}")
            return redirect('equipment_accounting_home')
    else:
        form = SearchSubscriber()
    return render(request, 'equipment_accounting/home.html', {'form': form})


def about(request):
    return render(request, 'equipment_accounting/about.html', {'title': 'About'})
