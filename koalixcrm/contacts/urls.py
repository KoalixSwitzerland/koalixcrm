"""Per-app REST API routes for koalixcrm Contacts (Party data model).

Mounted at ``/koalixcrm_contacts/api/v1/<workspace_id>/`` from
``projectsettings/urls.py`` once CR-R2 of CR-002 lands. Until then this
module is inert — importing it has no effect on the running URL conf.
"""
from rest_framework.routers import DefaultRouter

from koalixcrm.contacts_api_py.contacts_api import (
    AddressAssignmentViewSet,
    AddressViewSet,
    CustomerBillingCycleViewSet,
    EmailAssignmentViewSet,
    OrganizationMembershipViewSet,
    OrganizationRelationshipViewSet,
    OrganizationViewSet,
    PartyContactViewSet,
    PartyEmailViewSet,
    PartyGroupMembershipViewSet,
    PartyGroupViewSet,
    PartyIdentificationViewSet,
    PartyRoleViewSet,
    PartyViewSet,
    PhoneAssignmentViewSet,
    PhoneNumberViewSet,
)

router = DefaultRouter()
router.register(r'customer-billing-cycles', CustomerBillingCycleViewSet, basename='customer-billing-cycle')
router.register(r'parties', PartyViewSet, basename='party')
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'party-contacts', PartyContactViewSet, basename='party-contact')
router.register(r'party-identifications', PartyIdentificationViewSet, basename='party-identification')
router.register(r'party-roles', PartyRoleViewSet, basename='party-role')
router.register(r'organization-memberships', OrganizationMembershipViewSet, basename='organization-membership')
router.register(r'organization-relationships', OrganizationRelationshipViewSet, basename='organization-relationship')
router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'address-assignments', AddressAssignmentViewSet, basename='address-assignment')
router.register(r'phone-numbers', PhoneNumberViewSet, basename='phone-number')
router.register(r'phone-assignments', PhoneAssignmentViewSet, basename='phone-assignment')
router.register(r'party-emails', PartyEmailViewSet, basename='party-email')
router.register(r'email-assignments', EmailAssignmentViewSet, basename='email-assignment')
router.register(r'party-groups', PartyGroupViewSet, basename='party-group')
router.register(r'party-group-memberships', PartyGroupMembershipViewSet, basename='party-group-membership')

urlpatterns = router.urls
