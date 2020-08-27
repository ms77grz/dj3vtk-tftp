from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from easysnmp import Session
import pandas as pd
import os
from .utils import sp

module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, '/home/ms77grz/.devreg/gpon_hosts.csv')


def network(request):
    return render(request, 'network/network.html')


@login_required
def olt_list(request):
    title = 'GPON Проекты'

    df = pd.read_csv(file_path, names=(
        'id', 'address', 'ip', 'model', 's_cap', 'b_cap', 'xnum', 'xplata', 'boards', 'inst_date', 'lat', 'lon', 'area', 'desc'))
    df1 = df[['ip', 'address', 'model']]
    olts = df1.to_dict('records')

    return render(request, 'network/gpon/olt_list.html', {'title': title, 'olts': olts})


@login_required
def olt_detail(request, ip):
    title = 'Список абонентов'
    try:
        session = Session(hostname=ip, community='gpon_vtk_95', version=2)
        subscribers = session.walk('.1.3.6.1.4.1.2011.6.128.1.1.2.43.1.9')
        states = session.walk('.1.3.6.1.4.1.2011.6.128.1.1.2.46.1.15')
        zipped_context = zip(subscribers, states)
    except Exception:
        messages.error(request, f'Не удалось установить связь с {ip}')
        return redirect('olt_list')
    return render(request, 'network/gpon/olt_detail.html', {'title': title, 'zipped_context': zipped_context, 'ip': ip})


@login_required
def ont_detail(request, ip, oid, description):
    title = 'Свойства ONT'
    ont_id = oid.split('.')[-1]  # 0-15
    oid_id = '.'.join(oid.split('.')[-2:])  # 4194304000.0
    port_id = oid.split('.')[-2]  # 4194304000
    slot_port = sp(port_id)
    # Getting serial number and profile
    session = Session(hostname=ip, community='gpon_vtk_95',
                      version=2, use_sprint_value=True)
    sn = session.get(f'iso.3.6.1.4.1.2011.6.128.1.1.2.43.1.3.{oid_id}').value.replace(
        ' ', '').replace('"', '')
    lineprofile = session.get(
        f'.1.3.6.1.4.1.2011.6.128.1.1.2.43.1.7.{oid_id}').value.replace('"', '')
    optical_power = round(int(session.get(
        f'.1.3.6.1.4.1.2011.6.128.1.1.2.51.1.6.{oid_id}').value)/100-100, 2)
    return render(request, 'network/gpon/ont_detail.html', {
        'title': title,
        'ip': ip,
        'lineprofile': lineprofile,
        'description': description,
        'sn': sn,
        'ont_id': ont_id,
        'oid_id': oid_id,
        'slot_port': slot_port,
        'port_id': port_id,
        'optical_power': optical_power
    })
