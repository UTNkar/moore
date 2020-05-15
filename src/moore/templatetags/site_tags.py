from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the bootstrap menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag('tags/menu.html', takes_context=True)
def menu_items(context, parent, sidenav=False, top_level=False):
    menuitems = parent.get_children().live().in_menu()
    menuitems = [m.specific for m in menuitems]
    for menuitem in menuitems:
        menuitem.has_children = has_menu_children(menuitem)
        menuitem.active = context['request'].path.startswith(menuitem.url)
        menuitem.title = (
            menuitem.translated_title
            if menuitem.translated_title else menuitem.title
        )

    return {
        'parent': parent,
        'top_level': top_level,
        'menuitems': menuitems,
        'sidenav': sidenav,
        'request': context['request'],
    }


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('tags/menu_children.html', takes_context=True)
def menu_children(context, parent, sidenav=False):
    children = parent.get_children().live().in_menu()
    children = [c.specific for c in children]
    return {
        'parent': parent,
        'children': children,
        'sidenav': sidenav,
        'request': context['request'],
    }
