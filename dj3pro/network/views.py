from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from easysnmp import Session
import pandas as pd
import os
from .utils import sp
from django.conf import settings
from collections import OrderedDict
from operator import getitem


SNMP_COMM_RO_GPON = settings.SNMP_COMM_RO_GPON

module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, '/home/ms77grz/.devreg/gpon_hosts.csv')


def network(request):
    return render(request, 'network/network.html')


@login_required
def olt_list(request):
    title = 'Список Проектов'

    df = pd.read_csv(file_path, names=(
        'id', 'address', 'ip', 'model', 's_cap', 'b_cap', 'xnum', 'xplata', 'boards', 'inst_date', 'lat', 'lon', 'area', 'desc'))
    df1 = df[['ip', 'address', 'model', 'desc']]
    df1.sort_values('desc', inplace=True)
    olts = df1.to_dict('records')

    return render(request, 'network/gpon/olt_list.html', {'title': title, 'olts': olts})


@login_required
def olt_detail(request, ip, model):
    title = 'Список абонентов'
    if model in ['MA5608T', 'MA5683T']:
        try:
            # GET SNMP DATA FROM OLT
            session = Session(hostname=ip, community=SNMP_COMM_RO_GPON, version=2)
            subscribers = session.walk('.1.3.6.1.4.1.2011.6.128.1.1.2.43.1.9')
            states = session.walk('.1.3.6.1.4.1.2011.6.128.1.1.2.46.1.15')
            zipped_context = zip(subscribers, states)

            # CREATE A DICT WITH KEY VALUE PAIRS / REPORT DICT FOR SPLITTERS
            data = {}
            report = {}
            for subscriber, state in zipped_context:
                key = subscriber.oid
                description = ' '.join(subscriber.value.replace('_', ' ').replace(
                    '=', ' ').replace('(', ' ').replace(')', ' ').split()[:-1])
                status = state.value
                splitter = ''.join(subscriber.value.replace('_', ' ').replace(
                    '=', ' ').replace('(', ' ').replace(')', ' ').split()[-1])
                data[key] = {'description': description,
                            'status': status, 'splitter': splitter}

                count = report.get(splitter, 0)
                report[splitter] = count + 1

            # SORT DATA VIA SPLITTERS AS A KEY
            sorted_data = OrderedDict(sorted(data.items(), key=lambda x: getitem(x[1], 'splitter')))
                        
            # COLLECT SPLITTERS FROM REPORT TO A SORTED SPLITTERS LIST
            splitters = sorted(report.items(), key=lambda item: item[0])

            sorted_splitters = []
            for line in splitters:
                sorted_splitters.append(f'splitter {line[0]}: {line[1]}')
            

            # EVALUATE TOTAL SPLITTERS
            total_spliters = len(report.keys())

            # EVALUATE TOTAL SUBSCRIBERS
            total_subscribers = len(sorted_data)

        except Exception:
            messages.error(request, f'Не удалось установить связь с {ip}')
            return redirect('olt_list')
    else:
        messages.error(request, f'Функционал для ELTEX не работает. Попробуйте подключиться по telnet {ip}')
        return redirect('olt_list')
    
    return render(request, 'network/gpon/olt_detail.html',
                  {'title': title,
                   'ip': ip,
                   'model': model,
                   'sorted_data': sorted_data,
                   'sorted_splitters': sorted_splitters,
                   'total_spliters': total_spliters,
                   'total_subscribers': total_subscribers,
                   })


@login_required
def ont_detail(request, ip, model, oid):
    title = 'Свойства ONT'
    if model in ['MA5608T', 'MA5683T']:
        ont_id = oid.split('.')[-1]  # 0-15
        oid_id = '.'.join(oid.split('.')[-2:])  # 4194304000.0
        port_id = oid.split('.')[-2]  # 4194304000
        slot_port = sp(port_id)
        try:
            session = Session(hostname=ip, community=SNMP_COMM_RO_GPON,
                              version=2, use_sprint_value=True)
            subscriber = session.get(f'.1.3.6.1.4.1.2011.6.128.1.1.2.43.1.9.{oid_id}')
            subscriber = ' '.join(subscriber.value.replace('_', ' ').replace('=', ' ').replace('(', ' ').replace(')', ' ').replace('"', '').split())
            print(subscriber)
            sn = session.get(f'iso.3.6.1.4.1.2011.6.128.1.1.2.43.1.3.{oid_id}').value.replace(' ', '').replace('"', '')
            lineprofile = session.get(
                f'.1.3.6.1.4.1.2011.6.128.1.1.2.43.1.7.{oid_id}').value.replace('"', '')
            optical_power = round(int(session.get(
                f'.1.3.6.1.4.1.2011.6.128.1.1.2.51.1.6.{oid_id}').value)/100-100, 2)
        except Exception:
            messages.error(request, f'Не удалось установить связь с {ip}')
            return redirect('olt_list')
    else:
        ont_id = None
        oid_id = '.'.join(oid.split('.')[-3:])  # 4.30.212
        lineprofile = None
        slot_port = None

        try:
            session = Session(hostname=ip, community='gpon_vtk_95',
                              version=2, use_sprint_value=True)
            sn = session.get(
                f'1.3.6.1.4.1.35265.1.22.3.4.1.2.1.8.69.76.84.88.98.{oid_id}').value.replace(
                ' ', '').replace('"', '')
            optical_power = round(int(session.get(
                f'1.3.6.1.4.1.35265.1.22.3.1.1.11.1.8.69.76.84.88.98.{oid_id}').value)*0.1, 2)
        except Exception:
            messages.error(request, f'Не удалось установить связь с {ip}')
            return redirect('olt_list')

    return render(request, 'network/gpon/ont_detail.html', {
        'title': title,
        'subscriber': subscriber,
        'ip': ip,
        'lineprofile': lineprofile,
        'sn': sn,
        'ont_id': ont_id,
        'slot_port': slot_port,
        'optical_power': optical_power
    })


@login_required
def show_map(request):
    coords = [
        [43.301575,45.710273],
        [43.300861,45.708599],
        [43.301524,45.710261],
        [43.306353,45.70355],
        [43.301982,45.709973],
        [43.304581,45.705236],
        [43.30726,45.702498],
        [43.301221,45.710557],
        [43.305417,45.704428],
    ]
    return render(request, 'network/gpon/olt_map.html',{'title': 'Карта Проекта', 'coords':coords})