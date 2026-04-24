"""Per-app REST API routes for koalixcrm Core (currencies/taxes/units/pdf).

Mounted at ``/koalixcrm_core/api/v1/<workspace_id>/`` from
``projectsettings/urls.py`` once CR-R2 of CR-002 lands. Until then this
module is inert — importing it has no effect on the running URL conf.
"""
from rest_framework.routers import DefaultRouter

from koalixcrm.core_api_py.core_api import (
    CurrencyViewSet,
    TaxViewSet,
    UnitViewSet,
    CurrencyTransformViewSet,
    UnitTransformViewSet,
)
from koalixcrm.core_api_py.pdf_export_process_view_set import PDFExportProcessViewSet
from koalixcrm.djangoUserExtension.views.document_template_view_set import (
    DocumentTemplateViewSet,
)

router = DefaultRouter()
router.register(r'currencies', CurrencyViewSet, basename='currency')
router.register(r'taxes', TaxViewSet, basename='tax')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'currency-transforms', CurrencyTransformViewSet, basename='currency-transform')
router.register(r'unit-transforms', UnitTransformViewSet, basename='unit-transform')
router.register(r'pdf-export-processes', PDFExportProcessViewSet, basename='pdf-export-process')
router.register(r'document-templates', DocumentTemplateViewSet, basename='document-template')

urlpatterns = router.urls
