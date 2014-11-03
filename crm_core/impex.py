from import_export import resources
from .models import Product, Contract, Customer, CustomerBillingCycle, \
    CustomerGroup, PurchaseOrder, Quote, Invoice, Supplier, TaxRate, Unit


class ProductResource(resources.ModelResource):
    
    class Meta():
        model = Product
        

class ContractResource(resources.ModelResource):
    
    class Meta():
        model = Contract

        
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

        
class SupplierResource(resources.ModelResource):
    
    class Meta():
        model = Supplier
        
        
class TaxRateResource(resources.ModelResource):
    
    class Meta():
        model = TaxRate
        
        
class UnitResource(resources.ModelResource):
    
    class Meta():
        model = Unit