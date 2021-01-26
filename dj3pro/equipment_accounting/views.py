from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SearchSubscriber
from subprocess import Popen, PIPE, STDOUT
from django.conf import settings
from easysnmp import Session

DEVCONS = settings.DEVCONS
SNMP_COMM_RO_FTTX = settings.SNMP_COMM_RO_FTTX


def home(request):
    return render(request, 'equipment_accounting/home.html')


@login_required
def search(request):
    if request.method == 'POST':
        form = SearchSubscriber(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data.get('account_number')
            
            try:
                account_number = int(account_number)
            except Exception:
                messages.error(request, f'Введите номер лицевого счета')
                return redirect('equipment_accounting_search')

            command = ["ag", "-B 1", "--hidden", "--nonumbers",
                       f"{account_number}", DEVCONS]
            process = Popen(command, stdout=PIPE, stderr=STDOUT)
            output = process.stdout.read().decode()
            output = ''.join(output)
            output = output.replace(
                DEVCONS, '')
            output = output.split('\n')
            if len(output) <= 1:
                output = None
            form = SearchSubscriber()
            context = context = {
                'form': form,
                'output': output,
            }
            if output:
                model = output[0].split('_')[0]
                ip = output[0].split('_')[1].split('.cfg:')[0]
                port = output[0].split('_')[1].split('.cfg:')[1]
                # example ls 1102288921 with name in description line
                description = ' '.join(output[1].split('_')[1:]).split('.cfg:')[1].strip()
                if 'description' in description:
                    description = description.split('description')[1].replace('=', '').strip()
                if 'name' in description:
                    description = description.split('name')[1].replace('=', '').strip()
                if 'desc' in description:
                    description = description.split('desc')[1].replace('=', '').replace('"', '').strip()
                    print(description)
                # CHECK IF HOST IS REACHABLE
                try:
                    session = Session(hostname=ip, community='vtk', version=2, timeout=1, retries=1)
                    is_online = session.get('sysName.0')
                except Exception:
                    is_online = False
                
                context['model'] = model
                context['ip'] = ip
                context['port'] = port
                context['description'] = description
                context['is_online'] = is_online
            return render(request, 'equipment_accounting/search.html', context)
    else:
        form = SearchSubscriber()
    return render(request, 'equipment_accounting/search.html', {'form': form})


def about(request):
    return render(request, 'equipment_accounting/about.html', {'title': 'About'})
