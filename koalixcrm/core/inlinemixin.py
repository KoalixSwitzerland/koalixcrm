class LimitedAdminInlineMixin(object):
    """
    InlineAdmin mixin limiting the selection of related items according to
    criteria which can depend on the current parent object being edited.

    A typical use case would be selecting a subset of related items from
    other inlines, ie. images, to have some relation to other inlines.

    Use as follows::

        class MyInline(LimitedAdminInlineMixin, admin.TabularInline):
            def get_filters(self, request, obj):
                return (('<field_name>', dict(<filters>)),)

    Here, <field_name> is the name of the FK field to be filtered and <filters>
    is a dict of parameters as you would normally specify them in the filter()
    method of QuerySets.

    Modified from:
    https://stackoverflow.com/a/5008984
    https://gist.github.com/dokterbob/828117
    """

    @staticmethod
    def limit_inline_choices(formset, field, empty=False, **filters):
        """
        This function fetches the queryset with available choices for a given
        `field` and filters it based on the criteria specified in filters,
        unless `empty=True`. In this case, no choices will be made available.
        """
        assert field in formset.form.base_fields
        qs = formset.form.base_fields[field].queryset
        if empty:
            formset.form.base_fields[field].queryset = qs.none()
        else:
            qs = qs.filter(**filters)
            formset.form.base_fields[field].queryset = qs

    def get_formset(self, request, obj=None, **kwargs):
        """
        Make sure we can only select variations that relate to the current
        item.
        """
        formset = super(LimitedAdminInlineMixin, self).get_formset(request,
                                                                   obj,
                                                                   **kwargs)
        inline_filters = self.get_filters(request, obj)
        if inline_filters:
            for (field, filters,) in inline_filters:
                self.limit_inline_choices(formset, field, **filters)
        return formset