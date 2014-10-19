from import_export import resources
from .models import Product, Contract, Currency, Customer, CustomerBillingCycle, \
    CustomerGroup, PurchaseOrder, Quote, Invoice, SalesContract, Supplier, Tax, Unit


class ProductResource(resources.ModelResource):
    
    class Meta():
        model = Product
        

class ContractResource(resources.ModelResource):
    
    class Meta():
        model = Contract
        

class CurrencyResource(resources.ModelResource):
    
    class Meta():
        model = Currency
        
        
class CustomerResource(resources.ModelResource):
    
    class Meta():
        model = Customer
        
        
class CustomerBillingCycleResource(resources.ModelResource):
    
    class Meta():
        model = CustomerBillingCycle
        
        
class CustomerGroupResource(resources.ModelResource):
    
    class Meta():
        model = CustomerGroup
        
        
class PurchaseOrderResource(resources.ModelResource):
    
    class Meta():
        model = PurchaseOrder
        
        
class QuoteResource(resources.ModelResource):
    
    class Meta():
        model = Quote
        
        
class InvoiceResource(resources.ModelResource):
    
    class Meta():
        model = Invoice
        
        
class SalesContractResource(resources.ModelResource):
    
    class Meta():
        model = SalesContract
        
        
class SupplierResource(resources.ModelResource):
    
    class Meta():
        model = Supplier
        
        
class TaxResource(resources.ModelResource):
    
    class Meta():
        model = Tax
        
        
class UnitResource(resources.ModelResource):
    
    class Meta():
        model = Unit