from django import template

from ...creme_core.core.loading import get_class

get_nodes = get_class('creme_config.menu', 'get_nodes')
register = template.Library()


@register.simple_tag
def dashboard_navigation(user):
    return get_nodes(user)
