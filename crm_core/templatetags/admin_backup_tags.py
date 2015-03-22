from __future__ import unicode_literals
from mezzanine import template


register = template.Library()


@register.inclusion_tag("admin/includes/backup.html")
def admin_backup():
    """
    Dashboard widget for displaying a backup button.
    """
    pass