# -*- coding: utf-8 -*-
"""KoalixCRM Contacts API Client"""
from typing import Dict, List, Any, Optional

from koalixcrm.shared.api_client import BaseAPIClient
from koalixcrm.crm_api_py.dto.customer import Customer
from koalixcrm.crm_api_py.dto.supplier import Supplier
from koalixcrm.crm_api_py.dto.person import Person
from koalixcrm.crm_api_py.dto.contact import Contact
from koalixcrm.crm_api_py.dto.customer_group import CustomerGroup
from koalixcrm.crm_api_py.dto.customer_billing_cycle import CustomerBillingCycle
from koalixcrm.crm_api_py.dto.postal_address import PostalAddress
from koalixcrm.crm_api_py.dto.email_address import EmailAddress
from koalixcrm.crm_api_py.dto.phone_address import PhoneAddress


class KoalixCRMContactsAPIClient(BaseAPIClient):
    api_path_env_var = 'KOALIXCRM_CRM_API_PATH'
    api_path_default = ''

    def __init__(self, api_url=None, username=None, password=None):
        super().__init__(api_url=api_url, username=username, password=password)

    # ------------------------------------------------------------------
    # Customer (endpoint: /customers)
    # ------------------------------------------------------------------

    def get_customer(self, object_id: int) -> Optional[Customer]:
        return self._get_object(Customer, "/customers", object_id)

    def get_customer_list(self) -> List[Customer]:
        return self._get_object_list(Customer, "/customers/")

    def create_customer(self, data: Dict[str, Any]) -> Optional[Customer]:
        response_data = self._make_request("/customers/", method="POST", data=data)
        if response_data:
            obj = Customer(response_data, self)
            self._cache.set(Customer, obj.id, obj)
            return obj
        return None

    def update_customer(self, object_id: int, data: Dict[str, Any]) -> Optional[Customer]:
        return self._put_full_update(Customer, "/customers", object_id, data)

    # ------------------------------------------------------------------
    # Supplier (endpoint: /suppliers)
    # ------------------------------------------------------------------

    def get_supplier(self, object_id: int) -> Optional[Supplier]:
        return self._get_object(Supplier, "/suppliers", object_id)

    def get_supplier_list(self) -> List[Supplier]:
        return self._get_object_list(Supplier, "/suppliers/")

    def create_supplier(self, data: Dict[str, Any]) -> Optional[Supplier]:
        response_data = self._make_request("/suppliers/", method="POST", data=data)
        if response_data:
            obj = Supplier(response_data, self)
            self._cache.set(Supplier, obj.id, obj)
            return obj
        return None

    def update_supplier(self, object_id: int, data: Dict[str, Any]) -> Optional[Supplier]:
        return self._put_full_update(Supplier, "/suppliers", object_id, data)

    # ------------------------------------------------------------------
    # Person (endpoint: /persons)
    # ------------------------------------------------------------------

    def get_person(self, object_id: int) -> Optional[Person]:
        return self._get_object(Person, "/persons", object_id)

    def get_person_list(self) -> List[Person]:
        return self._get_object_list(Person, "/persons/")

    def create_person(self, data: Dict[str, Any]) -> Optional[Person]:
        response_data = self._make_request("/persons/", method="POST", data=data)
        if response_data:
            obj = Person(response_data, self)
            self._cache.set(Person, obj.id, obj)
            return obj
        return None

    def update_person(self, object_id: int, data: Dict[str, Any]) -> Optional[Person]:
        return self._put_full_update(Person, "/persons", object_id, data)

    # ------------------------------------------------------------------
    # Contact (endpoint: /contacts)
    # ------------------------------------------------------------------

    def get_contact(self, object_id: int) -> Optional[Contact]:
        return self._get_object(Contact, "/contacts", object_id)

    def get_contact_list(self) -> List[Contact]:
        return self._get_object_list(Contact, "/contacts/")

    def create_contact(self, data: Dict[str, Any]) -> Optional[Contact]:
        response_data = self._make_request("/contacts/", method="POST", data=data)
        if response_data:
            obj = Contact(response_data, self)
            self._cache.set(Contact, obj.id, obj)
            return obj
        return None

    def update_contact(self, object_id: int, data: Dict[str, Any]) -> Optional[Contact]:
        return self._put_full_update(Contact, "/contacts", object_id, data)

    # ------------------------------------------------------------------
    # CustomerGroup (endpoint: /customer_groups)
    # ------------------------------------------------------------------

    def get_customer_group(self, object_id: int) -> Optional[CustomerGroup]:
        return self._get_object(CustomerGroup, "/customer_groups", object_id)

    def get_customer_group_list(self) -> List[CustomerGroup]:
        return self._get_object_list(CustomerGroup, "/customer_groups/")

    def create_customer_group(self, data: Dict[str, Any]) -> Optional[CustomerGroup]:
        response_data = self._make_request("/customer_groups/", method="POST", data=data)
        if response_data:
            obj = CustomerGroup(response_data, self)
            self._cache.set(CustomerGroup, obj.id, obj)
            return obj
        return None

    def update_customer_group(self, object_id: int, data: Dict[str, Any]) -> Optional[CustomerGroup]:
        return self._put_full_update(CustomerGroup, "/customer_groups", object_id, data)

    # ------------------------------------------------------------------
    # CustomerBillingCycle (endpoint: /customer_billing_cycles)
    # ------------------------------------------------------------------

    def get_customer_billing_cycle(self, object_id: int) -> Optional[CustomerBillingCycle]:
        return self._get_object(CustomerBillingCycle, "/customer_billing_cycles", object_id)

    def get_customer_billing_cycle_list(self) -> List[CustomerBillingCycle]:
        return self._get_object_list(CustomerBillingCycle, "/customer_billing_cycles/")

    def create_customer_billing_cycle(self, data: Dict[str, Any]) -> Optional[CustomerBillingCycle]:
        response_data = self._make_request("/customer_billing_cycles/", method="POST", data=data)
        if response_data:
            obj = CustomerBillingCycle(response_data, self)
            self._cache.set(CustomerBillingCycle, obj.id, obj)
            return obj
        return None

    def update_customer_billing_cycle(self, object_id: int, data: Dict[str, Any]) -> Optional[CustomerBillingCycle]:
        return self._put_full_update(CustomerBillingCycle, "/customer_billing_cycles", object_id, data)

    # ------------------------------------------------------------------
    # ContactPostalAddress (endpoint: /contact_postal_addresses)
    # ------------------------------------------------------------------

    def get_contact_postal_address(self, object_id: int) -> Optional[PostalAddress]:
        return self._get_object(PostalAddress, "/contact_postal_addresses", object_id)

    def get_contact_postal_address_list(self) -> List[PostalAddress]:
        return self._get_object_list(PostalAddress, "/contact_postal_addresses/")

    def create_contact_postal_address(self, data: Dict[str, Any]) -> Optional[PostalAddress]:
        response_data = self._make_request("/contact_postal_addresses/", method="POST", data=data)
        if response_data:
            obj = PostalAddress(response_data, self)
            self._cache.set(PostalAddress, obj.id, obj)
            return obj
        return None

    def update_contact_postal_address(self, object_id: int, data: Dict[str, Any]) -> Optional[PostalAddress]:
        return self._put_full_update(PostalAddress, "/contact_postal_addresses", object_id, data)

    # ------------------------------------------------------------------
    # ContactEmailAddress (endpoint: /contact_email_addresses)
    # ------------------------------------------------------------------

    def get_contact_email_address(self, object_id: int) -> Optional[EmailAddress]:
        return self._get_object(EmailAddress, "/contact_email_addresses", object_id)

    def get_contact_email_address_list(self) -> List[EmailAddress]:
        return self._get_object_list(EmailAddress, "/contact_email_addresses/")

    def create_contact_email_address(self, data: Dict[str, Any]) -> Optional[EmailAddress]:
        response_data = self._make_request("/contact_email_addresses/", method="POST", data=data)
        if response_data:
            obj = EmailAddress(response_data, self)
            self._cache.set(EmailAddress, obj.id, obj)
            return obj
        return None

    def update_contact_email_address(self, object_id: int, data: Dict[str, Any]) -> Optional[EmailAddress]:
        return self._put_full_update(EmailAddress, "/contact_email_addresses", object_id, data)

    # ------------------------------------------------------------------
    # ContactPhoneAddress (endpoint: /contact_phone_numbers)
    # ------------------------------------------------------------------

    def get_contact_phone_address(self, object_id: int) -> Optional[PhoneAddress]:
        return self._get_object(PhoneAddress, "/contact_phone_numbers", object_id)

    def get_contact_phone_address_list(self) -> List[PhoneAddress]:
        return self._get_object_list(PhoneAddress, "/contact_phone_numbers/")

    def create_contact_phone_address(self, data: Dict[str, Any]) -> Optional[PhoneAddress]:
        response_data = self._make_request("/contact_phone_numbers/", method="POST", data=data)
        if response_data:
            obj = PhoneAddress(response_data, self)
            self._cache.set(PhoneAddress, obj.id, obj)
            return obj
        return None

    def update_contact_phone_address(self, object_id: int, data: Dict[str, Any]) -> Optional[PhoneAddress]:
        return self._put_full_update(PhoneAddress, "/contact_phone_numbers", object_id, data)
