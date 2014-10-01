"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'koalixcrm.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for koalixcrm
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Group: Administration & Applications'),
            column=1,
            collapsible=False,
            children = [
                modules.AppList(
                    _('Administration'),
                    column=1,
                    collapsible=True,
                    css_classes=('collapse closed',),
                    models=('django.contrib.*',),
                ),
                modules.AppList(
                    _('Applications'),
                    column=1,
                    collapsible=False,
                    exclude=('django.contrib.*',),
                )
            ]
        ))
        
       
        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('ModelList: Administration'),
            column=1,
            collapsible=False,
            models=('django.contrib.*',),
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Media Management'),
            column=2,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            column=2,
            children=[
                {
                    'title': _('koalixcrm documentation'),
                    'url': 'http://docs.koalix.org/',
                    'external': True,
                },
                {
                    'title': _('koalixcrm "koalixcrm-user" mailing list'),
                    'url': 'http://groups.google.com/group/koalixcrm-users',
                    'external': True,
                },
            ]
        ))
        
        # append a feed module
        self.children.append(modules.Feed(
            title=_('Latest koalixcrm News'),
            column=2,
            feed_url='http://www.koalix.org/projects/koalixcrm/news.atom',
            limit=5
        ))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))

