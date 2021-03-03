from django import template

register = template.Library()


@register.inclusion_tag('cloud_manager/menu.html')
def show_menu():
    return {'arg_list': ['upload', 'download', 'delete']}
