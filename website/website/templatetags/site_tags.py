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
def menu_items(context, parent, calling_page=None, sidenav=False):
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        # TODO: There has to be a better alternative!
        if hasattr(menuitem, 'googleformindex'):
            menuitem.translated_title = menuitem.googleformindex\
                .translated_title
        elif hasattr(menuitem, 'googleformpage'):
            menuitem.translated_title = menuitem.googleformpage\
                .translated_title
        elif hasattr(menuitem, 'homepage'):
            menuitem.translated_title = menuitem.homepage.translated_title
        elif hasattr(menuitem, 'recruitmentpage'):
            menuitem.translated_title = menuitem.recruitmentpage\
                .translated_title
        elif hasattr(menuitem, 'newsindexpage'):
            menuitem.translated_title = menuitem.newsindexpage.translated_title
        elif hasattr(menuitem, 'newspage'):
            menuitem.translated_title = menuitem.newspage.translated_title
        elif hasattr(menuitem, 'webpage'):
            menuitem.translated_title = menuitem.webpage.translated_title
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = (calling_page.url.startswith(menuitem.url)
                           if calling_page else False)
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        'sidenav': sidenav,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('tags/menu_children.html', takes_context=True)
def menu_children(context, parent, sidenav=False):
    children = parent.get_children()
    children = children.live().in_menu()
    return {
        'parent': parent,
        'children': children,
        'sidenav': sidenav,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }
