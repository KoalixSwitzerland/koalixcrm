from django.views.generic import UpdateView, CreateView
from extra_views import UpdateWithInlinesView, CreateWithInlinesView


# ################
# ##   Mixins   ##
# ################

class UpdateWithModifiedByMixin(UpdateView):

    def post(self, request, *args, **kwargs):
        res = super(UpdateWithModifiedByMixin, self).post(request, *args, **kwargs)
        self.object.lastmodifiedby = request.user
        self.object.save()
        return res


class CreateWithModifieByMixin(CreateView):

    def post(self, request, *args, **kwargs):
        res = super(CreateWithModifieByMixin, self).post(request, *args, **kwargs)
        self.object.lastmodifiedby = request.user
        self.object.save()
        return res


class UpdateWithInlinesAndModifiedByMixin(UpdateWithInlinesView):

    def post(self, request, *args, **kwargs):
        res = super(UpdateWithInlinesAndModifiedByMixin, self).post(request, *args, **kwargs)
        self.object.lastmodifiedby = request.user
        self.object.save()
        return res


class CreateWithInlinesAndModifiedByMixin(CreateWithInlinesView):

    def post(self, request, *args, **kwargs):
        res = super(CreateWithInlinesAndModifiedByMixin, self).post(request, *args, **kwargs)
        self.object.lastmodifiedby = request.user
        self.object.save()
        return res
