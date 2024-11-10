# Accounting Tests Documentation

## 1. Overview
The accounting tests verify the functionality of KoalixCRM's accounting module, focusing on account management, bookings, and accounting period calculations. The tests use Django's TestCase framework for database-driven testing.

## 2. Test Structure

### 2.1 Files
- `__init__.py`: Package initialization file
- `test_accountingModelTest.py`: Main test suite for accounting models

### 2.2 Test Coverage
The test suite covers:
- Account balance calculations
- Accounting period operations
- Booking transactions
- XML serialization for reporting

## 3. Test Setup and Data Model

### 3.1 Class Structure
```plantuml
@startuml
class AccountingModelTest {
  + setUp()
  + test_sumOfAllBookings()
  + test_sumOfAllBookingsBeforeAccountPeriod()
  + test_sumOfAllBookingsWithinAccountgPeriod()
  + test_overall_liabilities()
  + test_overall_assets()
  + test_overall_earnings()
  + test_overall_spendings()
  + test_serialize_to_xml()
}

class TestData {
  + User
  + Accounts
  + AccountingPeriods
  + Bookings
}

AccountingModelTest --> TestData: creates
@enduml
```

### 3.2 Data Model
```plantuml
@startuml
class Account {
  + account_number: String
  + title: String
  + account_type: String
  + description: String
  + is_open_interest_account: Boolean
  + is_open_reliabilities_account: Boolean
  + is_product_inventory_activa: Boolean
  + is_a_customer_payment_account: Boolean
}

class AccountingPeriod {
  + title: String
  + begin: Date
  + end: Date
}

class Booking {
  + from_account: Account
  + to_account: Account
  + amount: Decimal
  + description: String
  + booking_date: DateTime
  + accounting_period: AccountingPeriod
  + staff: User
  + last_modified_by: User
}

Booking --> Account: from_account
Booking --> Account: to_account
Booking --> AccountingPeriod
@enduml
```

### 3.3 Test Flow
```plantuml
@startuml
title Booking Test Flow

participant TestCase
participant Account
participant Booking
participant AccountingPeriod

TestCase -> Account: create accounts\n(cash, bank, etc.)
TestCase -> AccountingPeriod: create periods\n(2024-2026)
TestCase -> Booking: create test bookings

group Test Balance Calculation
    TestCase -> Account: sum_of_all_bookings()
    Account --> TestCase: return total balance
    TestCase -> Account: verify balance matches\nexpected amount
end

group Test Period Calculations
    TestCase -> AccountingPeriod: overall_assets()
    AccountingPeriod -> Account: get all asset accounts
    Account --> AccountingPeriod: return accounts
    AccountingPeriod -> Booking: get relevant bookings
    Booking --> AccountingPeriod: return bookings
    AccountingPeriod --> TestCase: return calculated total
    TestCase -> TestCase: verify amount
end

group Test XML Export
    TestCase -> AccountingPeriod: serialize_to_xml()
    AccountingPeriod -> Account: get account data
    Account --> AccountingPeriod: return data
    AccountingPeriod -> Booking: get booking data
    Booking --> AccountingPeriod: return data
    AccountingPeriod --> TestCase: return XML
    TestCase -> TestCase: verify XML structure
end
@enduml
```

## 4. Test Cases

### 4.1 Account Balance Tests
- `test_sumOfAllBookings`: Verifies correct calculation of total account balances
- `test_sumOfAllBookingsBeforeAccountPeriod`: Tests balance calculations before specific accounting periods
- `test_sumOfAllBookingsWithinAccountgPeriod`: Validates balance calculations within accounting periods

### 4.2 Accounting Period Tests
- `test_overall_liabilities`: Validates total liabilities calculation
- `test_overall_assets`: Verifies total assets calculation
- `test_overall_earnings`: Tests earnings calculation
- `test_overall_spendings`: Validates spending calculations

### 4.3 Data Export Tests
- `test_serialize_to_xml`: Ensures correct XML serialization of accounting data

## 5. Test Data Setup

### 5.1 Accounts
- Cash (1000): Asset account for cash transactions
- Bank Account (1300): Asset account for bank transactions
- Bank Loan (2000): Liability account for short-term loans
- Investment Capital (2900): Liability account for long-term investment
- Spendings (3000): Spending account for purchases
- Earnings (4000): Earnings account for sales

### 5.2 Accounting Periods
- Fiscal year 2024: January 1, 2024 - December 31, 2024
- Fiscal year 2025: January 1, 2025 - December 31, 2025
- Fiscal year 2026: January 1, 2026 - December 31, 2026

### 5.3 Test Data Relationships
- Each booking connects two accounts (from_account and to_account)
- Bookings are assigned to specific accounting periods
- User records are maintained for staff and modification tracking
- Account types determine their role in financial calculations

## 6. Running Tests
```bash
python manage.py test koalixcrm.accounting.tests
```

## 7. Writing New Tests
1. Follow the existing pattern in `test_accountingModelTest.py`
2. Add test data in the `setUp` method if needed
3. Ensure proper cleanup in `tearDown` if necessary
4. Use descriptive test names that reflect the functionality being tested
5. Include assertions that verify both positive and negative cases

## 8. Test Dependencies

### 8.1 Required Models
- Django User model
- Account model
- AccountingPeriod model
- Booking model
- PDFExport utility

### 8.2 External Dependencies
- Django TestCase framework
- datetime module
- make_date_utc utility function

### 8.3 Database Requirements
- Test database with transaction support
- Proper migration setup
- Configured Django settings

## 9. Performance Considerations

1. **Test Data Volume**
   - Current test suite uses minimal test data
   - Consider adding volume tests for performance validation
   - Monitor database query count
## 10. Test Isolation

### 10.1 Database Isolation
- Uses Django's TestCase which provides automatic transaction rollback
- Each test method runs in its own transaction
- Database is reset to a clean state between tests
- Test data is isolated through Django's test database creation

### 10.2 Fixture Management
- Test data is created in setUp() method for each test run
- Uses direct object creation instead of fixtures for better control
- Consistent initial state for all test methods
- Hierarchical data setup (User -> Accounts -> Periods -> Bookings)

### 10.3 Test Data Separation
```plantuml
@startuml
title Test Data Isolation Pattern

participant TestCase
database TestDB
participant Transaction

TestCase -> TestDB: Begin Test
activate Transaction

group Setup Phase
    TestCase -> TestDB: Create User
    TestCase -> TestDB: Create Accounts
    TestCase -> TestDB: Create Periods
    TestCase -> TestDB: Create Bookings
end

group Test Execution
    TestCase -> TestDB: Run Test Method
    TestCase -> TestDB: Verify Results
end

TestCase -> Transaction: Rollback
deactivate Transaction

TestCase -> TestDB: Next Test
@enduml
```

### 10.4 Resource Management
1. **Database Connections**
   - Managed by Django's test framework
   - Automatic cleanup after each test
   - Separate test database per test run

2. **Test Data Lifecycle**
   ```plantuml
   @startuml
   title Test Data Lifecycle
   
   state "Test Start" as Start
   state "Setup Data" as Setup
   state "Execute Test" as Execute
   state "Verify Results" as Verify
   state "Cleanup" as Cleanup
   
   Start --> Setup
   Setup --> Execute
   Execute --> Verify
   Verify --> Cleanup
   Cleanup --> [*]
   @enduml
   ```

### 10.5 Common Issues and Solutions
1. **Data Leakage Prevention**
   - Use unique identifiers for test data
   - Avoid global state modifications
   - Maintain data independence between tests

2. **Resource Contention**
   - Each test uses isolated database transactions
   - No shared state between test methods
   - Clean setup/teardown cycle

3. **Test Independence**
   - Each test method is self-contained
   - No dependencies between test methods
   - Explicit test data creation

### 10.6 Best Practices
1. **Setting Up Test Environment**
   - Use setUp() for common test data
   - Create only necessary test data
   - Maintain data consistency

2. **Managing Dependencies**
   - Explicit dependency creation in setUp
   - Clear separation of test scenarios
   - Avoid cross-test dependencies

3. **Data Cleanup**
   - Automatic transaction rollback
   - No manual cleanup needed
   - Consistent database state

4. **Parallel Execution**
   - Tests designed for parallel execution
   - No shared resource conflicts
   - Independent test methods

### 10.7 Debugging Isolation Issues
1. **Common Problems**
   - Data bleeding between tests
   - Inconsistent test results
   - Resource cleanup failures

2. **Solutions**
   - Verify setUp method completeness
   - Check for shared state
   - Monitor database transactions
   - Use proper test case inheritance

### 10.8 Test Isolation Patterns
```plantuml
@startuml
title Test Isolation Patterns

package "Test Environment" {
    [Test Database] as DB
    [Transaction Manager] as TM
    [Test Runner] as TR
}

cloud "Isolated Resources" {
    [Test Case 1] as TC1
    [Test Case 2] as TC2
}

DB -- TM
TM -- TR
TR -- TC1
TR -- TC2

note right of TC1: Independent\nTransaction
note right of TC2: Independent\nTransaction
note bottom of TM: Manages Rollbacks
@enduml
```
