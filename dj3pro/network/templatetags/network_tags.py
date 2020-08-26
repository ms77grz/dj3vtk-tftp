from django import template
from easysnmp import Session

register = template.Library()


@register.filter
def clear_value(text):
    return text.replace('_', ' ').replace('=', '')


@register.filter
def ont_status(value):
    if value == '1':
        return 'online'
    return 'offline'


# @register.filter
# def olt_status(ip):
#     try:
#         session = Session(hostname=ip, community='gpon_vtk_95', version=2)
#         session.walk('1.3.6.1.2.1.1.3')
#         return 'online'
#     except Exception:
#         return 'offline'
