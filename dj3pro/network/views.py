from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from easysnmp import Session
import pandas as pd
import os
from .utils import sp
from django.conf import settings

SNMP_COMM_RO = settings.SNMP_COMM_RO

module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, '/home/ms77grz/.devreg/gpon_hosts.csv')


def network(request):
    return render(request, 'network/network.html')


@login_required
def olt_list(request):
    title = 'GPON Проекты'

    df = pd.read_csv(file_path, names=(
        'id', 'address', 'ip', 'model', 's_cap', 'b_cap', 'xnum', 'xplata', 'boards', 'inst_date', 'lat', 'lon', 'area', 'desc'))
    df1 = df[['ip', 'address', 'model', 'desc']]
    df1.sort_values('desc', inplace=True)
    olts = df1.to_dict('records')

    return render(request, 'network/gpon/olt_list.html', {'title': title, 'olts': olts})


@login_required
def olt_detail(request, ip, model):
    title = 'Список абонентов'
    if model not in ['LTP-4X', 'LTP-8X']:
        try:
            session = Session(hostname=ip, community=SNMP_COMM_RO, version=2)
            subscribers = session.walk('.1.3.6.1.4.1.2011.6.128.1.1.2.43.1.9')
            states = session.walk('.1.3.6.1.4.1.2011.6.128.1.1.2.46.1.15')
            zipped_context = zip(subscribers, states)
        except Exception:
            messages.error(request, f'Не удалось установить связь с {ip}')
            return redirect('olt_list')
    else:
        # try:
        #     session = Session(hostname=ip, community=SNMP_COMM_RO, version=2)
        #     subscribers = session.walk(
        #         '.1.3.6.1.4.1.35265.1.22.3.4.1.8')
        #     states = session.walk('.1.3.6.1.4.1.35265.1.22.3.2.1.5')
        #     zipped_context = zip(subscribers, states)
        # except Exception:
        #     messages.error(request, f'Не удалось установить связь с {ip}')
        #     return redirect('olt_list')
        messages.error(request, f'Функционал для ELTEX не работает. Попробуйте подключиться по telnet {ip}')
        return redirect('olt_list')
    return render(request, 'network/gpon/olt_detail.html', {'title': title, 'zipped_context': zipped_context, 'ip': ip, 'model': model})


@login_required
def ont_detail(request, ip, model, oid):
    title = 'Свойства ONT'
    if model not in ['LTP-4X', 'LTP-8X']:
        ont_id = oid.split('.')[-1]  # 0-15
        oid_id = '.'.join(oid.split('.')[-2:])  # 4194304000.0
        port_id = oid.split('.')[-2]  # 4194304000
        slot_port = sp(port_id)
        try:
            session = Session(hostname=ip, community='gpon_vtk_95',
                              version=2, use_sprint_value=True)
            sn = session.get(f'iso.3.6.1.4.1.2011.6.128.1.1.2.43.1.3.{oid_id}').value.replace(
                ' ', '').replace('"', '')
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
        'ip': ip,
        'lineprofile': lineprofile,
        'sn': sn,
        'ont_id': ont_id,
        'slot_port': slot_port,
        'optical_power': optical_power
    })
