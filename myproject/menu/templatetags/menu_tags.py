from django import template
from django.urls import resolve
from django.utils.safestring import mark_safe
from ..models import Menu, MenuItem

register = template.Library()

def get_active_items(menu_items, current_url):
    active_items = set()
    for item in menu_items:
        if item.get_url() == current_url:
            active_items.add(item.id)
            parent = item.parent
            while parent:
                active_items.add(parent.id)
                parent = parent.parent
    return active_items

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path

    try:
        menu = Menu.objects.prefetch_related(
            'items',
            'items__children',
            'items__children__children'
        ).get(slug=menu_name)
    except Menu.DoesNotExist:
        return ''

    menu_items = menu.items.filter(parent=None)
    active_items = get_active_items(menu.items.all(), current_url)

    def render_menu_item(item, level=0):
        is_active = item.id in active_items
        has_active_child = any(child.id in active_items for child in item.children.all())
        is_expanded = is_active or has_active_child

        html = f'<li class="menu-item level-{level} {"active" if is_active else ""}">'
        html += f'<a href="{item.get_url()}">{item.title}</a>'

        if item.children.exists() and (is_expanded or level == 0):
            html += '<ul class="submenu">'
            for child in item.children.all():
                html += render_menu_item(child, level + 1)
            html += '</ul>'

        html += '</li>'
        return html

    html = f'<ul class="menu {menu_name}">'
    for item in menu_items:
        html += render_menu_item(item)
    html += '</ul>'

    return mark_safe(html) 