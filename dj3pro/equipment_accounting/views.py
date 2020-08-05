from django.shortcuts import render

devices = [
    {
        'hostname': 'GRZ32-121-Alpha-A28F',
        'ip': '10.25.32.121',
        'address': 'г. Грозный ул. 4 переулок Петрапавловское б/н',
        'model': 'Alpha-A28F',
        'type_of_service': 'fiber aggregation switch',
        'area': 'grz_area',
        'latitude': 43.343118,
        'longitude': 45.705417,
        'site': 'БC-LTE-88',
        'comment': 'старый IP'
    },
    {
        'hostname': 'GRZ32-134-Alpha-A28F',
        'ip': '10.25.32.134',
        'address': 'г. Грозный ул. Ворожева/Лермонтова 55/65',
        'model': 'Alpha-A28F',
        'type_of_service': 'fiber aggregation switch',
        'area': 'grz_area',
        'latitude': 43.350286,
        'longitude': 45.729852,
        'site': 'БС LTE-90 доп ком',
        'comment': 'старый IP'
    },
    {
        'hostname': 'GRZ1-088-S2940',
        'ip': '10.25.0.223',
        'address': 'г. Грозный ул. Мира 64',
        'model': 'SNR-S2940-8G',
        'type_of_service': 'copper access switch',
        'area': 'grz_area',
        'latitude': 43.343118,
        'longitude': 45.705417,
        'site': 'РОВД',
        'comment': 'старый IP'
    }
]


def home(request):
    return render(request, 'equipment_accounting/home.html', {'devices': devices})


def about(request):
    return render(request, 'equipment_accounting/about.html', {'title': 'About'})
