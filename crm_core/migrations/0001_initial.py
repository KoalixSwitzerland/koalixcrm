# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser_safe.fields
import django.utils.timezone
from django.conf import settings
import django_fsm
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0006_auto_20150811_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', django_fsm.FSMIntegerField(default=10, choices=[(10, 'open'), (20, 'payed'), (30, 'Invoice created'), (40, 'Invoice sent'), (50, 'Quote created'), (60, 'Quote sent'), (70, 'Purchaseorder created'), (90, 'Unpayed'), (100, 'Deleted')])),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('default_currency', models.CharField(blank=True, max_length=3, null=True, verbose_name='Default Currency', choices=[('USD', 'USD - United States Dollar'), ('EUR', 'EUR - Euro Members'), ('JPY', 'JPY - Japan Yen'), ('GBP', 'GBP - United Kingdom Pound'), ('CHF', 'CHF - Switzerland Franc'), ('AED', 'AED - United Arab Emirates Dirham'), ('AFN', 'AFN - Afghanistan Afghani'), ('ALL', 'ALL - Albania Lek'), ('AMD', 'AMD - Armenia Dram'), ('ANG', 'ANG - Netherlands Antilles Guilder'), ('AOA', 'AOA - Angola Kwanza'), ('ARS', 'ARS - Argentina Peso'), ('AUD', 'AUD - Australia Dollar'), ('AWG', 'AWG - Aruba Guilder'), ('AZN', 'AZN - Azerbaijan New Manat'), ('BAM', 'BAM - Bosnia and Herzegovina Convertible Marka'), ('BBD', 'BBD - Barbados Dollar'), ('BDT', 'BDT - Bangladesh Taka'), ('BGN', 'BGN - Bulgaria Lev'), ('BHD', 'BHD - Bahrain Dinar'), ('BIF', 'BIF - Burundi Franc'), ('BMD', 'BMD - Bermuda Dollar'), ('BND', 'BND - Brunei Darussalam Dollar'), ('BOB', 'BOB - Bolivia Boliviano'), ('BRL', 'BRL - Brazil Real'), ('BSD', 'BSD - Bahamas Dollar'), ('BTN', 'BTN - Bhutan Ngultrum'), ('BWP', 'BWP - Botswana Pula'), ('BYR', 'BYR - Belarus Ruble'), ('BZD', 'BZD - Belize Dollar'), ('CAD', 'CAD - Canada Dollar'), ('CDF', 'CDF - Congo/Kinshasa Franc'), ('CLP', 'CLP - Chile Peso'), ('CNY', 'CNY - China Yuan Renminbi'), ('COP', 'COP - Colombia Peso'), ('CRC', 'CRC - Costa Rica Colon'), ('CUC', 'CUC - Cuba Convertible Peso'), ('CUP', 'CUP - Cuba Peso'), ('CVE', 'CVE - Cape Verde Escudo'), ('CZK', 'CZK - Czech Republic Koruna'), ('DJF', 'DJF - Djibouti Franc'), ('DKK', 'DKK - Denmark Krone'), ('DOP', 'DOP - Dominican Republic Peso'), ('DZD', 'DZD - Algeria Dinar'), ('EGP', 'EGP - Egypt Pound'), ('ERN', 'ERN - Eritrea Nakfa'), ('ETB', 'ETB - Ethiopia Birr'), ('FJD', 'FJD - Fiji Dollar'), ('FKP', 'FKP - Falkland Islands (Malvinas) Pound'), ('GEL', 'GEL - Georgia Lari'), ('GGP', 'GGP - Guernsey Pound'), ('GHS', 'GHS - Ghana Cedi'), ('GIP', 'GIP - Gibraltar Pound'), ('GMD', 'GMD - Gambia Dalasi'), ('GNF', 'GNF - Guinea Franc'), ('GTQ', 'GTQ - Guatemala Quetzal'), ('GYD', 'GYD - Guyana Dollar'), ('HKD', 'HKD - Hong Kong Dollar'), ('HNL', 'HNL - Honduras Lempira'), ('HRK', 'HRK - Croatia Kuna'), ('HTG', 'HTG - Haiti Gourde'), ('HUF', 'HUF - Hungary Forint'), ('IDR', 'IDR - Indonesia Rupiah'), ('ILS', 'ILS - Israel Shekel'), ('IMP', 'IMP - Isle of Man Pound'), ('INR', 'INR - India Rupee'), ('IQD', 'IQD - Iraq Dinar'), ('IRR', 'IRR - Iran Rial'), ('ISK', 'ISK - Iceland Krona'), ('JEP', 'JEP - Jersey Pound'), ('JMD', 'JMD - Jamaica Dollar'), ('JOD', 'JOD - Jordan Dinar'), ('KES', 'KES - Kenya Shilling'), ('KGS', 'KGS - Kyrgyzstan Som'), ('KHR', 'KHR - Cambodia Riel'), ('KMF', 'KMF - Comoros Franc'), ('KPW', 'KPW - Korea (North) Won'), ('KRW', 'KRW - Korea (South) Won'), ('KWD', 'KWD - Kuwait Dinar'), ('KYD', 'KYD - Cayman Islands Dollar'), ('KZT', 'KZT - Kazakhstan Tenge'), ('LAK', 'LAK - Laos Kip'), ('LBP', 'LBP - Lebanon Pound'), ('LKR', 'LKR - Sri Lanka Rupee'), ('LRD', 'LRD - Liberia Dollar'), ('LSL', 'LSL - Lesotho Loti'), ('LTL', 'LTL - Lithuania Litas'), ('LVL', 'LVL - Latvia Lat'), ('LYD', 'LYD - Libya Dinar'), ('MAD', 'MAD - Morocco Dirham'), ('MDL', 'MDL - Moldova Le'), ('MGA', 'MGA - Madagascar Ariary'), ('MKD', 'MKD - Macedonia Denar'), ('MMK', 'MMK - Myanmar (Burma) Kyat'), ('MNT', 'MNT - Mongolia Tughrik'), ('MOP', 'MOP - Macau Pataca'), ('MRO', 'MRO - Mauritania Ouguiya'), ('MUR', 'MUR - Mauritius Rupee'), ('MVR', 'MVR - Maldives (Maldive Islands) Rufiyaa'), ('MWK', 'MWK - Malawi Kwacha'), ('MXN', 'MXN - Mexico Peso'), ('MYR', 'MYR - Malaysia Ringgit'), ('MZN', 'MZN - Mozambique Metical'), ('NAD', 'NAD - Namibia Dollar'), ('NGN', 'NGN - Nigeria Naira'), ('NIO', 'NIO - Nicaragua Cordoba'), ('NOK', 'NOK - Norway Krone'), ('NPR', 'NPR - Nepal Rupee'), ('NZD', 'NZD - New Zealand Dollar'), ('OMR', 'OMR - Oman Rial'), ('PAB', 'PAB - Panama Balboa'), ('PEN', 'PEN - Peru Nuevo Sol'), ('PGK', 'PGK - Papua New Guinea Kina'), ('PHP', 'PHP - Philippines Peso'), ('PKR', 'PKR - Pakistan Rupee'), ('PLN', 'PLN - Poland Zloty'), ('PYG', 'PYG - Paraguay Guarani'), ('QAR', 'QAR - Qatar Riyal'), ('RON', 'RON - Romania New Le'), ('RSD', 'RSD - Serbia Dinar'), ('RUB', 'RUB - Russia Ruble'), ('RWF', 'RWF - Rwanda Franc'), ('SAR', 'SAR - Saudi Arabia Riyal'), ('SBD', 'SBD - Solomon Islands Dollar'), ('SCR', 'SCR - Seychelles Rupee'), ('SDG', 'SDG - Sudan Pound'), ('SEK', 'SEK - Sweden Krona'), ('SGD', 'SGD - Singapore Dollar'), ('SHP', 'SHP - Saint Helena Pound'), ('SLL', 'SLL - Sierra Leone Leone'), ('SOS', 'SOS - Somalia Shilling'), ('SPL', 'SPL - Seborga Luigino'), ('SRD', 'SRD - Suriname Dollar'), ('STD', 'STD - S\xe3o Tom\xe9 and Pr\xedncipe Dobra'), ('SVC', 'SVC - El Salvador Colon'), ('SYP', 'SYP - Syria Pound'), ('SZL', 'SZL - Swaziland Lilangeni'), ('THB', 'THB - Thailand Baht'), ('TJS', 'TJS - Tajikistan Somoni'), ('TMT', 'TMT - Turkmenistan Manat'), ('TND', 'TND - Tunisia Dinar'), ('TOP', "TOP - Tonga Pa'anga"), ('TRY', 'TRY - Turkey Lira'), ('TTD', 'TTD - Trinidad and Tobago Dollar'), ('TVD', 'TVD - Tuvalu Dollar'), ('TWD', 'TWD - Taiwan New Dollar'), ('TZS', 'TZS - Tanzania Shilling'), ('UAH', 'UAH - Ukraine Hryvna'), ('UGX', 'UGX - Uganda Shilling'), ('UYU', 'UYU - Uruguay Peso'), ('UZS', 'UZS - Uzbekistan Som'), ('VEF', 'VEF - Venezuela Bolivar'), ('VND', 'VND - Viet Nam Dong'), ('VUV', 'VUV - Vanuatu Vat'), ('WST', 'WST - Samoa Tala'), ('XAF', 'XAF - Communaut\xe9 Financi\xe8re Africaine (BEAC) CFA Franc BEAC'), ('XCD', 'XCD - East Caribbean Dollar'), ('XDR', 'XDR - International Monetary Fund (IMF) Special Drawing Rights'), ('XOF', 'XOF - Communaut\xe9 Financi\xe8re Africaine (BCEAO) Franc'), ('XPF', 'XPF - Comptoirs Fran\xe7ais du Pacifique (CFP) Franc'), ('YER', 'YER - Yemen Rial'), ('ZAR', 'ZAR - South Africa Rand'), ('ZMK', 'ZMK - Zambia Kwacha'), ('ZWD', 'ZWD - Zimbabwe Dollar')])),
                ('dateofcreation', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='Created at', editable=False, blank=True)),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='Last modified', editable=False, blank=True)),
            ],
            options={
                'get_latest_by': 'lastmodification',
                'verbose_name': 'Contract',
                'verbose_name_plural': 'Contracts',
                'permissions': (('view_contract', 'Can view contracts'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prefix', models.CharField(blank=True, max_length=1, null=True, verbose_name='Title', choices=[(b'F', 'Company'), (b'H', 'Mr'), (b'W', 'Mrs'), (b'G', 'Ms')])),
                ('name', models.CharField(max_length=300, verbose_name='Name')),
                ('dateofcreation', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='Created at', editable=False, blank=True)),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='Last modified', editable=False, blank=True)),
                ('default_currency', models.CharField(blank=True, max_length=3, null=True, choices=[('USD', 'USD - United States Dollar'), ('EUR', 'EUR - Euro Members'), ('JPY', 'JPY - Japan Yen'), ('GBP', 'GBP - United Kingdom Pound'), ('CHF', 'CHF - Switzerland Franc'), ('AED', 'AED - United Arab Emirates Dirham'), ('AFN', 'AFN - Afghanistan Afghani'), ('ALL', 'ALL - Albania Lek'), ('AMD', 'AMD - Armenia Dram'), ('ANG', 'ANG - Netherlands Antilles Guilder'), ('AOA', 'AOA - Angola Kwanza'), ('ARS', 'ARS - Argentina Peso'), ('AUD', 'AUD - Australia Dollar'), ('AWG', 'AWG - Aruba Guilder'), ('AZN', 'AZN - Azerbaijan New Manat'), ('BAM', 'BAM - Bosnia and Herzegovina Convertible Marka'), ('BBD', 'BBD - Barbados Dollar'), ('BDT', 'BDT - Bangladesh Taka'), ('BGN', 'BGN - Bulgaria Lev'), ('BHD', 'BHD - Bahrain Dinar'), ('BIF', 'BIF - Burundi Franc'), ('BMD', 'BMD - Bermuda Dollar'), ('BND', 'BND - Brunei Darussalam Dollar'), ('BOB', 'BOB - Bolivia Boliviano'), ('BRL', 'BRL - Brazil Real'), ('BSD', 'BSD - Bahamas Dollar'), ('BTN', 'BTN - Bhutan Ngultrum'), ('BWP', 'BWP - Botswana Pula'), ('BYR', 'BYR - Belarus Ruble'), ('BZD', 'BZD - Belize Dollar'), ('CAD', 'CAD - Canada Dollar'), ('CDF', 'CDF - Congo/Kinshasa Franc'), ('CLP', 'CLP - Chile Peso'), ('CNY', 'CNY - China Yuan Renminbi'), ('COP', 'COP - Colombia Peso'), ('CRC', 'CRC - Costa Rica Colon'), ('CUC', 'CUC - Cuba Convertible Peso'), ('CUP', 'CUP - Cuba Peso'), ('CVE', 'CVE - Cape Verde Escudo'), ('CZK', 'CZK - Czech Republic Koruna'), ('DJF', 'DJF - Djibouti Franc'), ('DKK', 'DKK - Denmark Krone'), ('DOP', 'DOP - Dominican Republic Peso'), ('DZD', 'DZD - Algeria Dinar'), ('EGP', 'EGP - Egypt Pound'), ('ERN', 'ERN - Eritrea Nakfa'), ('ETB', 'ETB - Ethiopia Birr'), ('FJD', 'FJD - Fiji Dollar'), ('FKP', 'FKP - Falkland Islands (Malvinas) Pound'), ('GEL', 'GEL - Georgia Lari'), ('GGP', 'GGP - Guernsey Pound'), ('GHS', 'GHS - Ghana Cedi'), ('GIP', 'GIP - Gibraltar Pound'), ('GMD', 'GMD - Gambia Dalasi'), ('GNF', 'GNF - Guinea Franc'), ('GTQ', 'GTQ - Guatemala Quetzal'), ('GYD', 'GYD - Guyana Dollar'), ('HKD', 'HKD - Hong Kong Dollar'), ('HNL', 'HNL - Honduras Lempira'), ('HRK', 'HRK - Croatia Kuna'), ('HTG', 'HTG - Haiti Gourde'), ('HUF', 'HUF - Hungary Forint'), ('IDR', 'IDR - Indonesia Rupiah'), ('ILS', 'ILS - Israel Shekel'), ('IMP', 'IMP - Isle of Man Pound'), ('INR', 'INR - India Rupee'), ('IQD', 'IQD - Iraq Dinar'), ('IRR', 'IRR - Iran Rial'), ('ISK', 'ISK - Iceland Krona'), ('JEP', 'JEP - Jersey Pound'), ('JMD', 'JMD - Jamaica Dollar'), ('JOD', 'JOD - Jordan Dinar'), ('KES', 'KES - Kenya Shilling'), ('KGS', 'KGS - Kyrgyzstan Som'), ('KHR', 'KHR - Cambodia Riel'), ('KMF', 'KMF - Comoros Franc'), ('KPW', 'KPW - Korea (North) Won'), ('KRW', 'KRW - Korea (South) Won'), ('KWD', 'KWD - Kuwait Dinar'), ('KYD', 'KYD - Cayman Islands Dollar'), ('KZT', 'KZT - Kazakhstan Tenge'), ('LAK', 'LAK - Laos Kip'), ('LBP', 'LBP - Lebanon Pound'), ('LKR', 'LKR - Sri Lanka Rupee'), ('LRD', 'LRD - Liberia Dollar'), ('LSL', 'LSL - Lesotho Loti'), ('LTL', 'LTL - Lithuania Litas'), ('LVL', 'LVL - Latvia Lat'), ('LYD', 'LYD - Libya Dinar'), ('MAD', 'MAD - Morocco Dirham'), ('MDL', 'MDL - Moldova Le'), ('MGA', 'MGA - Madagascar Ariary'), ('MKD', 'MKD - Macedonia Denar'), ('MMK', 'MMK - Myanmar (Burma) Kyat'), ('MNT', 'MNT - Mongolia Tughrik'), ('MOP', 'MOP - Macau Pataca'), ('MRO', 'MRO - Mauritania Ouguiya'), ('MUR', 'MUR - Mauritius Rupee'), ('MVR', 'MVR - Maldives (Maldive Islands) Rufiyaa'), ('MWK', 'MWK - Malawi Kwacha'), ('MXN', 'MXN - Mexico Peso'), ('MYR', 'MYR - Malaysia Ringgit'), ('MZN', 'MZN - Mozambique Metical'), ('NAD', 'NAD - Namibia Dollar'), ('NGN', 'NGN - Nigeria Naira'), ('NIO', 'NIO - Nicaragua Cordoba'), ('NOK', 'NOK - Norway Krone'), ('NPR', 'NPR - Nepal Rupee'), ('NZD', 'NZD - New Zealand Dollar'), ('OMR', 'OMR - Oman Rial'), ('PAB', 'PAB - Panama Balboa'), ('PEN', 'PEN - Peru Nuevo Sol'), ('PGK', 'PGK - Papua New Guinea Kina'), ('PHP', 'PHP - Philippines Peso'), ('PKR', 'PKR - Pakistan Rupee'), ('PLN', 'PLN - Poland Zloty'), ('PYG', 'PYG - Paraguay Guarani'), ('QAR', 'QAR - Qatar Riyal'), ('RON', 'RON - Romania New Le'), ('RSD', 'RSD - Serbia Dinar'), ('RUB', 'RUB - Russia Ruble'), ('RWF', 'RWF - Rwanda Franc'), ('SAR', 'SAR - Saudi Arabia Riyal'), ('SBD', 'SBD - Solomon Islands Dollar'), ('SCR', 'SCR - Seychelles Rupee'), ('SDG', 'SDG - Sudan Pound'), ('SEK', 'SEK - Sweden Krona'), ('SGD', 'SGD - Singapore Dollar'), ('SHP', 'SHP - Saint Helena Pound'), ('SLL', 'SLL - Sierra Leone Leone'), ('SOS', 'SOS - Somalia Shilling'), ('SPL', 'SPL - Seborga Luigino'), ('SRD', 'SRD - Suriname Dollar'), ('STD', 'STD - S\xe3o Tom\xe9 and Pr\xedncipe Dobra'), ('SVC', 'SVC - El Salvador Colon'), ('SYP', 'SYP - Syria Pound'), ('SZL', 'SZL - Swaziland Lilangeni'), ('THB', 'THB - Thailand Baht'), ('TJS', 'TJS - Tajikistan Somoni'), ('TMT', 'TMT - Turkmenistan Manat'), ('TND', 'TND - Tunisia Dinar'), ('TOP', "TOP - Tonga Pa'anga"), ('TRY', 'TRY - Turkey Lira'), ('TTD', 'TTD - Trinidad and Tobago Dollar'), ('TVD', 'TVD - Tuvalu Dollar'), ('TWD', 'TWD - Taiwan New Dollar'), ('TZS', 'TZS - Tanzania Shilling'), ('UAH', 'UAH - Ukraine Hryvna'), ('UGX', 'UGX - Uganda Shilling'), ('UYU', 'UYU - Uruguay Peso'), ('UZS', 'UZS - Uzbekistan Som'), ('VEF', 'VEF - Venezuela Bolivar'), ('VND', 'VND - Viet Nam Dong'), ('VUV', 'VUV - Vanuatu Vat'), ('WST', 'WST - Samoa Tala'), ('XAF', 'XAF - Communaut\xe9 Financi\xe8re Africaine (BEAC) CFA Franc BEAC'), ('XCD', 'XCD - East Caribbean Dollar'), ('XDR', 'XDR - International Monetary Fund (IMF) Special Drawing Rights'), ('XOF', 'XOF - Communaut\xe9 Financi\xe8re Africaine (BCEAO) Franc'), ('XPF', 'XPF - Comptoirs Fran\xe7ais du Pacifique (CFP) Franc'), ('YER', 'YER - Yemen Rial'), ('ZAR', 'ZAR - South Africa Rand'), ('ZMK', 'ZMK - Zambia Kwacha'), ('ZWD', 'ZWD - Zimbabwe Dollar')])),
                ('firstname', models.CharField(max_length=300, null=True, verbose_name='Prename', blank=True)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'permissions': (('view_customer', 'Can view customers'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerBillingCycle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name='Name')),
                ('days_to_payment', models.IntegerField(verbose_name='Days to Payment Date')),
            ],
            options={
                'verbose_name': 'Customer Billing Cycle',
                'verbose_name_plural': 'Customer Billing Cycle',
                'permissions': (('view_customerbillingcycle', 'Can view billing cycles'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerCartItem',
            fields=[
                ('cartitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shop.CartItem')),
                ('product', models.ForeignKey(verbose_name='Product', to='shop.Product')),
            ],
            options={
                'abstract': False,
            },
            bases=('shop.cartitem',),
        ),
        migrations.CreateModel(
            name='CustomerEmailAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=200, verbose_name='Email Address')),
                ('purpose', models.CharField(default=b'H', max_length=1, verbose_name='Purpose', choices=[(b'H', 'Private'), (b'O', 'Business')])),
                ('person', models.ForeignKey(related_name='emailaddresses', to='crm_core.Customer')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Email Address',
                'verbose_name_plural': 'Email Address',
                'permissions': (('view_emailaddress', 'Can view email address'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name': 'Customer Group',
                'verbose_name_plural': 'Customer Groups',
                'permissions': (('view_customer_group', 'Can view customer groups'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerPhoneAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=20, verbose_name='Phone Number')),
                ('purpose', models.CharField(default=b'H', max_length=1, verbose_name='Purpose', choices=[(b'H', 'Private'), (b'O', 'Business'), (b'P', 'Mobile Private'), (b'B', 'Mobile Business')])),
                ('person', models.ForeignKey(related_name='phonenumbers', to='crm_core.Customer')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Phone Address',
                'verbose_name_plural': 'Phone Address',
                'permissions': (('view_phoneaddress', 'Can view phone address'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerPostalAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('addressline1', models.CharField(max_length=200, null=True, verbose_name='Addressline 1', blank=True)),
                ('addressline2', models.CharField(max_length=200, null=True, verbose_name='Addressline 2', blank=True)),
                ('zipcode', models.IntegerField(null=True, verbose_name='Zipcode', blank=True)),
                ('city', models.CharField(max_length=100, null=True, verbose_name='City', blank=True)),
                ('state', models.CharField(max_length=100, null=True, verbose_name='State', blank=True)),
                ('country', models.CharField(blank=True, max_length=2, null=True, verbose_name='Country', choices=[('AF', 'Afghanistan'), ('AL', 'Albania'), ('AQ', 'Antarctica'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AG', 'Antigua and Barbuda'), ('AZ', 'Azerbaijan'), ('AR', 'Argentina'), ('AU', 'Australia'), ('AT', 'Austria'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('AM', 'Armenia'), ('BB', 'Barbados'), ('BE', 'Belgium'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('BZ', 'Belize'), ('IO', 'British Indian Ocean Territory'), ('SB', 'Solomon Islands'), ('VG', 'British Virgin Islands'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('MM', 'Myanmar'), ('BI', 'Burundi'), ('BY', 'Belarus'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('LK', 'Sri Lanka'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('TW', 'Taiwan'), ('CX', 'Christmas Island'), ('CC', 'Cocos'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('YT', 'Mayotte'), ('CG', 'Congo'), ('CD', 'Congo'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('BJ', 'Benin'), ('DK', 'Denmark'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ET', 'Ethiopia'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('FO', 'Faroe Islands'), ('FK', 'Falkland Islands'), ('GS', 'South Georgia and the South Sandwich Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('AX', '\xc5land Islands'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('DJ', 'Djibouti'), ('GA', 'Gabon'), ('GE', 'Georgia'), ('GM', 'Gambia'), ('PS', 'Palestinian Territory'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('KI', 'Kiribati'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GN', 'Guinea'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IL', 'Israel'), ('IT', 'Italy'), ('CI', "Cote d'Ivoire"), ('JM', 'Jamaica'), ('JP', 'Japan'), ('KZ', 'Kazakhstan'), ('JO', 'Jordan'), ('KE', 'Kenya'), ('KP', 'Korea'), ('KR', 'Korea'), ('KW', 'Kuwait'), ('KG', 'Kyrgyz Republic'), ('LA', "Lao People's Democratic Republic"), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LV', 'Latvia'), ('LR', 'Liberia'), ('LY', 'Libyan Arab Jamahiriya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('MX', 'Mexico'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('MD', 'Moldova'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('OM', 'Oman'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('AN', 'Netherlands Antilles'), ('CW', 'Cura\xe7ao'), ('AW', 'Aruba'), ('SX', 'Sint Maarten'), ('BQ', 'Bonaire'), ('NC', 'New Caledonia'), ('VU', 'Vanuatu'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('NO', 'Norway'), ('MP', 'Northern Mariana Islands'), ('UM', 'United States Minor Outlying Islands'), ('FM', 'Micronesia'), ('MH', 'Marshall Islands'), ('PW', 'Palau'), ('PK', 'Pakistan'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn Islands'), ('PL', 'Poland'), ('PT', 'Portugal'), ('GW', 'Guinea-Bissau'), ('TL', 'Timor-Leste'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'Reunion'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint Barthelemy'), ('SH', 'Saint Helena'), ('KN', 'Saint Kitts and Nevis'), ('AI', 'Anguilla'), ('LC', 'Saint Lucia'), ('MF', 'Saint Martin'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SK', 'Slovakia'), ('VN', 'Vietnam'), ('SI', 'Slovenia'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('ZW', 'Zimbabwe'), ('ES', 'Spain'), ('SS', 'South Sudan'), ('EH', 'Western Sahara'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard & Jan Mayen Islands'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TJ', 'Tajikistan'), ('TH', 'Thailand'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('AE', 'United Arab Emirates'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('MK', 'Macedonia'), ('EG', 'Egypt'), ('GB', 'United Kingdom'), ('GG', 'Guernsey'), ('JE', 'Jersey'), ('IM', 'Isle of Man'), ('TZ', 'Tanzania'), ('US', 'United States'), ('VI', 'United States Virgin Islands'), ('BF', 'Burkina Faso'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VE', 'Venezuela'), ('WF', 'Wallis and Futuna'), ('WS', 'Samoa'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('XX', 'Disputed Territory'), ('XE', 'Iraq-Saudi Arabia Neutral Zone'), ('XD', 'United Nations Neutral Zone'), ('XS', 'Spratly Islands')])),
                ('purpose', models.CharField(default=b'C', max_length=1, verbose_name='Purpose', choices=[(b'D', 'Delivery Address'), (b'B', 'Billing Address'), (b'C', 'Contact Address')])),
                ('person', models.ForeignKey(related_name='addresses', to='crm_core.Customer')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Postal Address',
                'verbose_name_plural': 'Postal Address',
                'permissions': (('view_postaladdress', 'Can view postal address'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HTMLFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Title', blank=True)),
                ('file', filebrowser_safe.fields.FileBrowseField(max_length=200, verbose_name='HTML File')),
            ],
            options={
                'verbose_name': 'HTML File',
                'verbose_name_plural': 'HTML Files',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_reference', models.CharField(max_length=100, verbose_name='External Reference', blank=True)),
                ('discount', models.DecimalField(null=True, verbose_name='Discount', max_digits=5, decimal_places=2, blank=True)),
                ('description', models.CharField(max_length=100, null=True, verbose_name='Description', blank=True)),
                ('dateofcreation', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='Created at', editable=False, blank=True)),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='Last modified', editable=False, blank=True)),
                ('pdf_path', models.CharField(max_length=200, null=True, editable=False, blank=True)),
                ('payableuntil', models.DateField(verbose_name='To pay until')),
                ('payment_bank_reference', models.CharField(max_length=100, null=True, verbose_name='Payment Bank Reference', blank=True)),
                ('cart', models.ForeignKey(to='shop.Cart', null=True)),
                ('contract', models.ForeignKey(related_name='invoices', verbose_name='Contract', to='crm_core.Contract')),
                ('customer', models.ForeignKey(verbose_name='Customer', to='crm_core.Customer')),
                ('lastmodifiedby', models.ForeignKey(verbose_name='Last modified by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('staff', models.ForeignKey(related_name='db_relscstaff', verbose_name='Staff', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'get_latest_by': 'lastmodification',
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
                'permissions': (('view_invoice', 'Can view invoices'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductTax',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.OneToOneField(related_name='item_tax', verbose_name='Product', to='shop.Product')),
            ],
            options={
                'verbose_name': 'Product Taxrate',
                'verbose_name_plural': 'Product Taxrates',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.OneToOneField(related_name='item_unit', verbose_name='Product', to='shop.Product')),
            ],
            options={
                'verbose_name': 'Product Unit',
                'verbose_name_plural': 'Product Units',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_reference', models.CharField(max_length=100, verbose_name='External Reference', blank=True)),
                ('discount', models.DecimalField(null=True, verbose_name='Discount', max_digits=5, decimal_places=2, blank=True)),
                ('description', models.CharField(max_length=100, null=True, verbose_name='Description', blank=True)),
                ('dateofcreation', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='Created at', editable=False, blank=True)),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='Last modified', editable=False, blank=True)),
                ('pdf_path', models.CharField(max_length=200, null=True, editable=False, blank=True)),
                ('validuntil', models.DateField(null=True, verbose_name='Valid until')),
                ('cart', models.ForeignKey(to='shop.Cart', null=True)),
                ('contract', models.ForeignKey(related_name='purchaseorders', verbose_name='Contract', to='crm_core.Contract')),
                ('customer', models.ForeignKey(verbose_name='Customer', to='crm_core.Customer')),
                ('lastmodifiedby', models.ForeignKey(verbose_name='Last modified by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('staff', models.ForeignKey(related_name='purchaseorder_staff', verbose_name='Staff', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'get_latest_by': 'lastmodification',
                'verbose_name': 'Purchase Order',
                'verbose_name_plural': 'Purchase Order',
                'permissions': (('view_purchaseorder', 'Can view purchase orders'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_reference', models.CharField(max_length=100, verbose_name='External Reference', blank=True)),
                ('discount', models.DecimalField(null=True, verbose_name='Discount', max_digits=5, decimal_places=2, blank=True)),
                ('description', models.CharField(max_length=100, null=True, verbose_name='Description', blank=True)),
                ('dateofcreation', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='Created at', editable=False, blank=True)),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='Last modified', editable=False, blank=True)),
                ('pdf_path', models.CharField(max_length=200, null=True, editable=False, blank=True)),
                ('validuntil', models.DateField(null=True, verbose_name='Valid until')),
                ('cart', models.ForeignKey(to='shop.Cart', null=True)),
                ('contract', models.ForeignKey(related_name='quotes', verbose_name='Contract', to='crm_core.Contract')),
                ('customer', models.ForeignKey(verbose_name='Customer', to='crm_core.Customer')),
                ('lastmodifiedby', models.ForeignKey(verbose_name='Last modified by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('staff', models.ForeignKey(related_name='quote_staff', verbose_name='Staff', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'get_latest_by': 'lastmodification',
                'verbose_name': 'Quote',
                'verbose_name_plural': 'Quotes',
                'permissions': (('view_quote', 'Can view quotes'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prefix', models.CharField(blank=True, max_length=1, null=True, verbose_name='Title', choices=[(b'F', 'Company'), (b'H', 'Mr'), (b'W', 'Mrs'), (b'G', 'Ms')])),
                ('name', models.CharField(max_length=300, verbose_name='Name')),
                ('dateofcreation', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='Created at', editable=False, blank=True)),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='Last modified', editable=False, blank=True)),
                ('default_currency', models.CharField(blank=True, max_length=3, null=True, choices=[('USD', 'USD - United States Dollar'), ('EUR', 'EUR - Euro Members'), ('JPY', 'JPY - Japan Yen'), ('GBP', 'GBP - United Kingdom Pound'), ('CHF', 'CHF - Switzerland Franc'), ('AED', 'AED - United Arab Emirates Dirham'), ('AFN', 'AFN - Afghanistan Afghani'), ('ALL', 'ALL - Albania Lek'), ('AMD', 'AMD - Armenia Dram'), ('ANG', 'ANG - Netherlands Antilles Guilder'), ('AOA', 'AOA - Angola Kwanza'), ('ARS', 'ARS - Argentina Peso'), ('AUD', 'AUD - Australia Dollar'), ('AWG', 'AWG - Aruba Guilder'), ('AZN', 'AZN - Azerbaijan New Manat'), ('BAM', 'BAM - Bosnia and Herzegovina Convertible Marka'), ('BBD', 'BBD - Barbados Dollar'), ('BDT', 'BDT - Bangladesh Taka'), ('BGN', 'BGN - Bulgaria Lev'), ('BHD', 'BHD - Bahrain Dinar'), ('BIF', 'BIF - Burundi Franc'), ('BMD', 'BMD - Bermuda Dollar'), ('BND', 'BND - Brunei Darussalam Dollar'), ('BOB', 'BOB - Bolivia Boliviano'), ('BRL', 'BRL - Brazil Real'), ('BSD', 'BSD - Bahamas Dollar'), ('BTN', 'BTN - Bhutan Ngultrum'), ('BWP', 'BWP - Botswana Pula'), ('BYR', 'BYR - Belarus Ruble'), ('BZD', 'BZD - Belize Dollar'), ('CAD', 'CAD - Canada Dollar'), ('CDF', 'CDF - Congo/Kinshasa Franc'), ('CLP', 'CLP - Chile Peso'), ('CNY', 'CNY - China Yuan Renminbi'), ('COP', 'COP - Colombia Peso'), ('CRC', 'CRC - Costa Rica Colon'), ('CUC', 'CUC - Cuba Convertible Peso'), ('CUP', 'CUP - Cuba Peso'), ('CVE', 'CVE - Cape Verde Escudo'), ('CZK', 'CZK - Czech Republic Koruna'), ('DJF', 'DJF - Djibouti Franc'), ('DKK', 'DKK - Denmark Krone'), ('DOP', 'DOP - Dominican Republic Peso'), ('DZD', 'DZD - Algeria Dinar'), ('EGP', 'EGP - Egypt Pound'), ('ERN', 'ERN - Eritrea Nakfa'), ('ETB', 'ETB - Ethiopia Birr'), ('FJD', 'FJD - Fiji Dollar'), ('FKP', 'FKP - Falkland Islands (Malvinas) Pound'), ('GEL', 'GEL - Georgia Lari'), ('GGP', 'GGP - Guernsey Pound'), ('GHS', 'GHS - Ghana Cedi'), ('GIP', 'GIP - Gibraltar Pound'), ('GMD', 'GMD - Gambia Dalasi'), ('GNF', 'GNF - Guinea Franc'), ('GTQ', 'GTQ - Guatemala Quetzal'), ('GYD', 'GYD - Guyana Dollar'), ('HKD', 'HKD - Hong Kong Dollar'), ('HNL', 'HNL - Honduras Lempira'), ('HRK', 'HRK - Croatia Kuna'), ('HTG', 'HTG - Haiti Gourde'), ('HUF', 'HUF - Hungary Forint'), ('IDR', 'IDR - Indonesia Rupiah'), ('ILS', 'ILS - Israel Shekel'), ('IMP', 'IMP - Isle of Man Pound'), ('INR', 'INR - India Rupee'), ('IQD', 'IQD - Iraq Dinar'), ('IRR', 'IRR - Iran Rial'), ('ISK', 'ISK - Iceland Krona'), ('JEP', 'JEP - Jersey Pound'), ('JMD', 'JMD - Jamaica Dollar'), ('JOD', 'JOD - Jordan Dinar'), ('KES', 'KES - Kenya Shilling'), ('KGS', 'KGS - Kyrgyzstan Som'), ('KHR', 'KHR - Cambodia Riel'), ('KMF', 'KMF - Comoros Franc'), ('KPW', 'KPW - Korea (North) Won'), ('KRW', 'KRW - Korea (South) Won'), ('KWD', 'KWD - Kuwait Dinar'), ('KYD', 'KYD - Cayman Islands Dollar'), ('KZT', 'KZT - Kazakhstan Tenge'), ('LAK', 'LAK - Laos Kip'), ('LBP', 'LBP - Lebanon Pound'), ('LKR', 'LKR - Sri Lanka Rupee'), ('LRD', 'LRD - Liberia Dollar'), ('LSL', 'LSL - Lesotho Loti'), ('LTL', 'LTL - Lithuania Litas'), ('LVL', 'LVL - Latvia Lat'), ('LYD', 'LYD - Libya Dinar'), ('MAD', 'MAD - Morocco Dirham'), ('MDL', 'MDL - Moldova Le'), ('MGA', 'MGA - Madagascar Ariary'), ('MKD', 'MKD - Macedonia Denar'), ('MMK', 'MMK - Myanmar (Burma) Kyat'), ('MNT', 'MNT - Mongolia Tughrik'), ('MOP', 'MOP - Macau Pataca'), ('MRO', 'MRO - Mauritania Ouguiya'), ('MUR', 'MUR - Mauritius Rupee'), ('MVR', 'MVR - Maldives (Maldive Islands) Rufiyaa'), ('MWK', 'MWK - Malawi Kwacha'), ('MXN', 'MXN - Mexico Peso'), ('MYR', 'MYR - Malaysia Ringgit'), ('MZN', 'MZN - Mozambique Metical'), ('NAD', 'NAD - Namibia Dollar'), ('NGN', 'NGN - Nigeria Naira'), ('NIO', 'NIO - Nicaragua Cordoba'), ('NOK', 'NOK - Norway Krone'), ('NPR', 'NPR - Nepal Rupee'), ('NZD', 'NZD - New Zealand Dollar'), ('OMR', 'OMR - Oman Rial'), ('PAB', 'PAB - Panama Balboa'), ('PEN', 'PEN - Peru Nuevo Sol'), ('PGK', 'PGK - Papua New Guinea Kina'), ('PHP', 'PHP - Philippines Peso'), ('PKR', 'PKR - Pakistan Rupee'), ('PLN', 'PLN - Poland Zloty'), ('PYG', 'PYG - Paraguay Guarani'), ('QAR', 'QAR - Qatar Riyal'), ('RON', 'RON - Romania New Le'), ('RSD', 'RSD - Serbia Dinar'), ('RUB', 'RUB - Russia Ruble'), ('RWF', 'RWF - Rwanda Franc'), ('SAR', 'SAR - Saudi Arabia Riyal'), ('SBD', 'SBD - Solomon Islands Dollar'), ('SCR', 'SCR - Seychelles Rupee'), ('SDG', 'SDG - Sudan Pound'), ('SEK', 'SEK - Sweden Krona'), ('SGD', 'SGD - Singapore Dollar'), ('SHP', 'SHP - Saint Helena Pound'), ('SLL', 'SLL - Sierra Leone Leone'), ('SOS', 'SOS - Somalia Shilling'), ('SPL', 'SPL - Seborga Luigino'), ('SRD', 'SRD - Suriname Dollar'), ('STD', 'STD - S\xe3o Tom\xe9 and Pr\xedncipe Dobra'), ('SVC', 'SVC - El Salvador Colon'), ('SYP', 'SYP - Syria Pound'), ('SZL', 'SZL - Swaziland Lilangeni'), ('THB', 'THB - Thailand Baht'), ('TJS', 'TJS - Tajikistan Somoni'), ('TMT', 'TMT - Turkmenistan Manat'), ('TND', 'TND - Tunisia Dinar'), ('TOP', "TOP - Tonga Pa'anga"), ('TRY', 'TRY - Turkey Lira'), ('TTD', 'TTD - Trinidad and Tobago Dollar'), ('TVD', 'TVD - Tuvalu Dollar'), ('TWD', 'TWD - Taiwan New Dollar'), ('TZS', 'TZS - Tanzania Shilling'), ('UAH', 'UAH - Ukraine Hryvna'), ('UGX', 'UGX - Uganda Shilling'), ('UYU', 'UYU - Uruguay Peso'), ('UZS', 'UZS - Uzbekistan Som'), ('VEF', 'VEF - Venezuela Bolivar'), ('VND', 'VND - Viet Nam Dong'), ('VUV', 'VUV - Vanuatu Vat'), ('WST', 'WST - Samoa Tala'), ('XAF', 'XAF - Communaut\xe9 Financi\xe8re Africaine (BEAC) CFA Franc BEAC'), ('XCD', 'XCD - East Caribbean Dollar'), ('XDR', 'XDR - International Monetary Fund (IMF) Special Drawing Rights'), ('XOF', 'XOF - Communaut\xe9 Financi\xe8re Africaine (BCEAO) Franc'), ('XPF', 'XPF - Comptoirs Fran\xe7ais du Pacifique (CFP) Franc'), ('YER', 'YER - Yemen Rial'), ('ZAR', 'ZAR - South Africa Rand'), ('ZMK', 'ZMK - Zambia Kwacha'), ('ZWD', 'ZWD - Zimbabwe Dollar')])),
                ('direct_shipment_to_customers', models.BooleanField(default=False, verbose_name='Offers direct Shipment to Customer')),
                ('lastmodifiedby', models.ForeignKey(verbose_name='Last modified by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
                'permissions': (('view_supplier', 'Can view suppliers'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplierEmailAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=200, verbose_name='Email Address')),
                ('purpose', models.CharField(default=b'H', max_length=1, verbose_name='Purpose', choices=[(b'H', 'Private'), (b'O', 'Business')])),
                ('person', models.ForeignKey(related_name='emailaddresses', to='crm_core.Supplier')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Email Address',
                'verbose_name_plural': 'Email Address',
                'permissions': (('view_emailaddress', 'Can view email address'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplierPhoneAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=20, verbose_name='Phone Number')),
                ('purpose', models.CharField(default=b'H', max_length=1, verbose_name='Purpose', choices=[(b'H', 'Private'), (b'O', 'Business'), (b'P', 'Mobile Private'), (b'B', 'Mobile Business')])),
                ('person', models.ForeignKey(related_name='phonenumbers', to='crm_core.Supplier')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Phone Address',
                'verbose_name_plural': 'Phone Address',
                'permissions': (('view_phoneaddress', 'Can view phone address'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplierPostalAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('addressline1', models.CharField(max_length=200, null=True, verbose_name='Addressline 1', blank=True)),
                ('addressline2', models.CharField(max_length=200, null=True, verbose_name='Addressline 2', blank=True)),
                ('zipcode', models.IntegerField(null=True, verbose_name='Zipcode', blank=True)),
                ('city', models.CharField(max_length=100, null=True, verbose_name='City', blank=True)),
                ('state', models.CharField(max_length=100, null=True, verbose_name='State', blank=True)),
                ('country', models.CharField(blank=True, max_length=2, null=True, verbose_name='Country', choices=[('AF', 'Afghanistan'), ('AL', 'Albania'), ('AQ', 'Antarctica'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AG', 'Antigua and Barbuda'), ('AZ', 'Azerbaijan'), ('AR', 'Argentina'), ('AU', 'Australia'), ('AT', 'Austria'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('AM', 'Armenia'), ('BB', 'Barbados'), ('BE', 'Belgium'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('BZ', 'Belize'), ('IO', 'British Indian Ocean Territory'), ('SB', 'Solomon Islands'), ('VG', 'British Virgin Islands'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('MM', 'Myanmar'), ('BI', 'Burundi'), ('BY', 'Belarus'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('LK', 'Sri Lanka'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('TW', 'Taiwan'), ('CX', 'Christmas Island'), ('CC', 'Cocos'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('YT', 'Mayotte'), ('CG', 'Congo'), ('CD', 'Congo'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('BJ', 'Benin'), ('DK', 'Denmark'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ET', 'Ethiopia'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('FO', 'Faroe Islands'), ('FK', 'Falkland Islands'), ('GS', 'South Georgia and the South Sandwich Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('AX', '\xc5land Islands'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('DJ', 'Djibouti'), ('GA', 'Gabon'), ('GE', 'Georgia'), ('GM', 'Gambia'), ('PS', 'Palestinian Territory'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('KI', 'Kiribati'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GN', 'Guinea'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IL', 'Israel'), ('IT', 'Italy'), ('CI', "Cote d'Ivoire"), ('JM', 'Jamaica'), ('JP', 'Japan'), ('KZ', 'Kazakhstan'), ('JO', 'Jordan'), ('KE', 'Kenya'), ('KP', 'Korea'), ('KR', 'Korea'), ('KW', 'Kuwait'), ('KG', 'Kyrgyz Republic'), ('LA', "Lao People's Democratic Republic"), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LV', 'Latvia'), ('LR', 'Liberia'), ('LY', 'Libyan Arab Jamahiriya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('MX', 'Mexico'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('MD', 'Moldova'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('OM', 'Oman'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('AN', 'Netherlands Antilles'), ('CW', 'Cura\xe7ao'), ('AW', 'Aruba'), ('SX', 'Sint Maarten'), ('BQ', 'Bonaire'), ('NC', 'New Caledonia'), ('VU', 'Vanuatu'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('NO', 'Norway'), ('MP', 'Northern Mariana Islands'), ('UM', 'United States Minor Outlying Islands'), ('FM', 'Micronesia'), ('MH', 'Marshall Islands'), ('PW', 'Palau'), ('PK', 'Pakistan'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn Islands'), ('PL', 'Poland'), ('PT', 'Portugal'), ('GW', 'Guinea-Bissau'), ('TL', 'Timor-Leste'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'Reunion'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint Barthelemy'), ('SH', 'Saint Helena'), ('KN', 'Saint Kitts and Nevis'), ('AI', 'Anguilla'), ('LC', 'Saint Lucia'), ('MF', 'Saint Martin'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SK', 'Slovakia'), ('VN', 'Vietnam'), ('SI', 'Slovenia'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('ZW', 'Zimbabwe'), ('ES', 'Spain'), ('SS', 'South Sudan'), ('EH', 'Western Sahara'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard & Jan Mayen Islands'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TJ', 'Tajikistan'), ('TH', 'Thailand'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('AE', 'United Arab Emirates'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('MK', 'Macedonia'), ('EG', 'Egypt'), ('GB', 'United Kingdom'), ('GG', 'Guernsey'), ('JE', 'Jersey'), ('IM', 'Isle of Man'), ('TZ', 'Tanzania'), ('US', 'United States'), ('VI', 'United States Virgin Islands'), ('BF', 'Burkina Faso'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VE', 'Venezuela'), ('WF', 'Wallis and Futuna'), ('WS', 'Samoa'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('XX', 'Disputed Territory'), ('XE', 'Iraq-Saudi Arabia Neutral Zone'), ('XD', 'United Nations Neutral Zone'), ('XS', 'Spratly Islands')])),
                ('purpose', models.CharField(default=b'C', max_length=1, verbose_name='Purpose', choices=[(b'D', 'Delivery Address'), (b'B', 'Billing Address'), (b'C', 'Contact Address')])),
                ('person', models.ForeignKey(related_name='addresses', to='crm_core.Supplier')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Postal Address',
                'verbose_name_plural': 'Postal Address',
                'permissions': (('view_postaladdress', 'Can view postal address'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaxRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('taxrate_in_percent', models.DecimalField(verbose_name='Taxrate in Percentage', max_digits=5, decimal_places=2)),
                ('name', models.CharField(max_length=100, verbose_name='Taxname')),
            ],
            options={
                'verbose_name': 'Tax',
                'verbose_name_plural': 'Taxes',
                'permissions': (('view_tax', 'Can view tax rates'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TemplateSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organisationname', models.CharField(max_length=200, verbose_name='Name of the Organisation')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('logo', filebrowser_safe.fields.FileBrowseField(max_length=200, null=True, verbose_name='Logo', blank=True)),
                ('addresser', models.CharField(max_length=200, null=True, verbose_name='Addresser', blank=True)),
                ('footer_text_salesorders', models.TextField(null=True, verbose_name='Footer Text On Salesorders', blank=True)),
                ('header_text_salesorders', models.TextField(null=True, verbose_name='Header Text On Salesorders', blank=True)),
                ('header_text_purchaseorders', models.TextField(null=True, verbose_name='Header Text On Purchaseorders', blank=True)),
                ('footer_text_purchaseorders', models.TextField(null=True, verbose_name='Footer Text On Purchaseorders', blank=True)),
                ('page_footer_left', models.CharField(max_length=40, null=True, verbose_name='Page Footer Left', blank=True)),
                ('page_footer_middle', models.CharField(max_length=40, null=True, verbose_name='Page Footer Middle', blank=True)),
                ('invoice_html_file', models.ForeignKey(related_name='invoice_template', verbose_name='HTML File for Invoice', to='crm_core.HTMLFile')),
                ('purchaseorder_html_file', models.ForeignKey(related_name='purchaseorder_template', verbose_name='HTML File for Purchaseorder', to='crm_core.HTMLFile')),
                ('quote_html_file', models.ForeignKey(related_name='quote_template', verbose_name='HTML File for Quote', to='crm_core.HTMLFile')),
            ],
            options={
                'verbose_name': 'Templateset',
                'verbose_name_plural': 'Templatesets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
                ('shortname', models.CharField(max_length=3, verbose_name='Displayed Name After Quantity In The Position')),
                ('factor', models.IntegerField(null=True, verbose_name='Factor Between This And Next Higher Unit', blank=True)),
                ('fractionof', models.ForeignKey(verbose_name='Is A Fraction Of', blank=True, to='crm_core.Unit', null=True)),
            ],
            options={
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
                'permissions': (('view_unit', 'Can view units'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnitTransform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factor', models.IntegerField(null=True, verbose_name='Factor between From and To Unit', blank=True)),
                ('from_unit', models.ForeignKey(related_name='db_reltransformfromunit', verbose_name='From Unit', to='crm_core.Unit')),
                ('product', models.ForeignKey(verbose_name='Product', to='shop.Product')),
                ('to_unit', models.ForeignKey(related_name='db_reltransformtounit', verbose_name='To Unit', to='crm_core.Unit')),
            ],
            options={
                'verbose_name': 'Unit Transform',
                'verbose_name_plural': 'Unit Transforms',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserExtension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default=b'avatars/avatar.jpg', null=True, upload_to=b'avatars/', blank=True)),
                ('default_currency', models.CharField(blank=True, max_length=3, null=True, choices=[('USD', 'USD - United States Dollar'), ('EUR', 'EUR - Euro Members'), ('JPY', 'JPY - Japan Yen'), ('GBP', 'GBP - United Kingdom Pound'), ('CHF', 'CHF - Switzerland Franc'), ('AED', 'AED - United Arab Emirates Dirham'), ('AFN', 'AFN - Afghanistan Afghani'), ('ALL', 'ALL - Albania Lek'), ('AMD', 'AMD - Armenia Dram'), ('ANG', 'ANG - Netherlands Antilles Guilder'), ('AOA', 'AOA - Angola Kwanza'), ('ARS', 'ARS - Argentina Peso'), ('AUD', 'AUD - Australia Dollar'), ('AWG', 'AWG - Aruba Guilder'), ('AZN', 'AZN - Azerbaijan New Manat'), ('BAM', 'BAM - Bosnia and Herzegovina Convertible Marka'), ('BBD', 'BBD - Barbados Dollar'), ('BDT', 'BDT - Bangladesh Taka'), ('BGN', 'BGN - Bulgaria Lev'), ('BHD', 'BHD - Bahrain Dinar'), ('BIF', 'BIF - Burundi Franc'), ('BMD', 'BMD - Bermuda Dollar'), ('BND', 'BND - Brunei Darussalam Dollar'), ('BOB', 'BOB - Bolivia Boliviano'), ('BRL', 'BRL - Brazil Real'), ('BSD', 'BSD - Bahamas Dollar'), ('BTN', 'BTN - Bhutan Ngultrum'), ('BWP', 'BWP - Botswana Pula'), ('BYR', 'BYR - Belarus Ruble'), ('BZD', 'BZD - Belize Dollar'), ('CAD', 'CAD - Canada Dollar'), ('CDF', 'CDF - Congo/Kinshasa Franc'), ('CLP', 'CLP - Chile Peso'), ('CNY', 'CNY - China Yuan Renminbi'), ('COP', 'COP - Colombia Peso'), ('CRC', 'CRC - Costa Rica Colon'), ('CUC', 'CUC - Cuba Convertible Peso'), ('CUP', 'CUP - Cuba Peso'), ('CVE', 'CVE - Cape Verde Escudo'), ('CZK', 'CZK - Czech Republic Koruna'), ('DJF', 'DJF - Djibouti Franc'), ('DKK', 'DKK - Denmark Krone'), ('DOP', 'DOP - Dominican Republic Peso'), ('DZD', 'DZD - Algeria Dinar'), ('EGP', 'EGP - Egypt Pound'), ('ERN', 'ERN - Eritrea Nakfa'), ('ETB', 'ETB - Ethiopia Birr'), ('FJD', 'FJD - Fiji Dollar'), ('FKP', 'FKP - Falkland Islands (Malvinas) Pound'), ('GEL', 'GEL - Georgia Lari'), ('GGP', 'GGP - Guernsey Pound'), ('GHS', 'GHS - Ghana Cedi'), ('GIP', 'GIP - Gibraltar Pound'), ('GMD', 'GMD - Gambia Dalasi'), ('GNF', 'GNF - Guinea Franc'), ('GTQ', 'GTQ - Guatemala Quetzal'), ('GYD', 'GYD - Guyana Dollar'), ('HKD', 'HKD - Hong Kong Dollar'), ('HNL', 'HNL - Honduras Lempira'), ('HRK', 'HRK - Croatia Kuna'), ('HTG', 'HTG - Haiti Gourde'), ('HUF', 'HUF - Hungary Forint'), ('IDR', 'IDR - Indonesia Rupiah'), ('ILS', 'ILS - Israel Shekel'), ('IMP', 'IMP - Isle of Man Pound'), ('INR', 'INR - India Rupee'), ('IQD', 'IQD - Iraq Dinar'), ('IRR', 'IRR - Iran Rial'), ('ISK', 'ISK - Iceland Krona'), ('JEP', 'JEP - Jersey Pound'), ('JMD', 'JMD - Jamaica Dollar'), ('JOD', 'JOD - Jordan Dinar'), ('KES', 'KES - Kenya Shilling'), ('KGS', 'KGS - Kyrgyzstan Som'), ('KHR', 'KHR - Cambodia Riel'), ('KMF', 'KMF - Comoros Franc'), ('KPW', 'KPW - Korea (North) Won'), ('KRW', 'KRW - Korea (South) Won'), ('KWD', 'KWD - Kuwait Dinar'), ('KYD', 'KYD - Cayman Islands Dollar'), ('KZT', 'KZT - Kazakhstan Tenge'), ('LAK', 'LAK - Laos Kip'), ('LBP', 'LBP - Lebanon Pound'), ('LKR', 'LKR - Sri Lanka Rupee'), ('LRD', 'LRD - Liberia Dollar'), ('LSL', 'LSL - Lesotho Loti'), ('LTL', 'LTL - Lithuania Litas'), ('LVL', 'LVL - Latvia Lat'), ('LYD', 'LYD - Libya Dinar'), ('MAD', 'MAD - Morocco Dirham'), ('MDL', 'MDL - Moldova Le'), ('MGA', 'MGA - Madagascar Ariary'), ('MKD', 'MKD - Macedonia Denar'), ('MMK', 'MMK - Myanmar (Burma) Kyat'), ('MNT', 'MNT - Mongolia Tughrik'), ('MOP', 'MOP - Macau Pataca'), ('MRO', 'MRO - Mauritania Ouguiya'), ('MUR', 'MUR - Mauritius Rupee'), ('MVR', 'MVR - Maldives (Maldive Islands) Rufiyaa'), ('MWK', 'MWK - Malawi Kwacha'), ('MXN', 'MXN - Mexico Peso'), ('MYR', 'MYR - Malaysia Ringgit'), ('MZN', 'MZN - Mozambique Metical'), ('NAD', 'NAD - Namibia Dollar'), ('NGN', 'NGN - Nigeria Naira'), ('NIO', 'NIO - Nicaragua Cordoba'), ('NOK', 'NOK - Norway Krone'), ('NPR', 'NPR - Nepal Rupee'), ('NZD', 'NZD - New Zealand Dollar'), ('OMR', 'OMR - Oman Rial'), ('PAB', 'PAB - Panama Balboa'), ('PEN', 'PEN - Peru Nuevo Sol'), ('PGK', 'PGK - Papua New Guinea Kina'), ('PHP', 'PHP - Philippines Peso'), ('PKR', 'PKR - Pakistan Rupee'), ('PLN', 'PLN - Poland Zloty'), ('PYG', 'PYG - Paraguay Guarani'), ('QAR', 'QAR - Qatar Riyal'), ('RON', 'RON - Romania New Le'), ('RSD', 'RSD - Serbia Dinar'), ('RUB', 'RUB - Russia Ruble'), ('RWF', 'RWF - Rwanda Franc'), ('SAR', 'SAR - Saudi Arabia Riyal'), ('SBD', 'SBD - Solomon Islands Dollar'), ('SCR', 'SCR - Seychelles Rupee'), ('SDG', 'SDG - Sudan Pound'), ('SEK', 'SEK - Sweden Krona'), ('SGD', 'SGD - Singapore Dollar'), ('SHP', 'SHP - Saint Helena Pound'), ('SLL', 'SLL - Sierra Leone Leone'), ('SOS', 'SOS - Somalia Shilling'), ('SPL', 'SPL - Seborga Luigino'), ('SRD', 'SRD - Suriname Dollar'), ('STD', 'STD - S\xe3o Tom\xe9 and Pr\xedncipe Dobra'), ('SVC', 'SVC - El Salvador Colon'), ('SYP', 'SYP - Syria Pound'), ('SZL', 'SZL - Swaziland Lilangeni'), ('THB', 'THB - Thailand Baht'), ('TJS', 'TJS - Tajikistan Somoni'), ('TMT', 'TMT - Turkmenistan Manat'), ('TND', 'TND - Tunisia Dinar'), ('TOP', "TOP - Tonga Pa'anga"), ('TRY', 'TRY - Turkey Lira'), ('TTD', 'TTD - Trinidad and Tobago Dollar'), ('TVD', 'TVD - Tuvalu Dollar'), ('TWD', 'TWD - Taiwan New Dollar'), ('TZS', 'TZS - Tanzania Shilling'), ('UAH', 'UAH - Ukraine Hryvna'), ('UGX', 'UGX - Uganda Shilling'), ('UYU', 'UYU - Uruguay Peso'), ('UZS', 'UZS - Uzbekistan Som'), ('VEF', 'VEF - Venezuela Bolivar'), ('VND', 'VND - Viet Nam Dong'), ('VUV', 'VUV - Vanuatu Vat'), ('WST', 'WST - Samoa Tala'), ('XAF', 'XAF - Communaut\xe9 Financi\xe8re Africaine (BEAC) CFA Franc BEAC'), ('XCD', 'XCD - East Caribbean Dollar'), ('XDR', 'XDR - International Monetary Fund (IMF) Special Drawing Rights'), ('XOF', 'XOF - Communaut\xe9 Financi\xe8re Africaine (BCEAO) Franc'), ('XPF', 'XPF - Comptoirs Fran\xe7ais du Pacifique (CFP) Franc'), ('YER', 'YER - Yemen Rial'), ('ZAR', 'ZAR - South Africa Rand'), ('ZMK', 'ZMK - Zambia Kwacha'), ('ZWD', 'ZWD - Zimbabwe Dollar')])),
                ('default_templateset', models.ForeignKey(blank=True, to='crm_core.TemplateSet', null=True)),
                ('user', models.OneToOneField(related_name='extension', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Extension',
                'verbose_name_plural': 'User Extensions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='productunit',
            name='unit',
            field=models.ForeignKey(verbose_name='Unit', to='crm_core.Unit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='producttax',
            name='tax',
            field=models.ForeignKey(verbose_name='Taxrate', to='crm_core.TaxRate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='billingcycle',
            field=models.ForeignKey(verbose_name='Default Billing Cycle', to='crm_core.CustomerBillingCycle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='ismemberof',
            field=models.ManyToManyField(to='crm_core.CustomerGroup', null=True, verbose_name='Is member of', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='lastmodifiedby',
            field=models.ForeignKey(verbose_name='Last modified by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='default_customer',
            field=models.ForeignKey(verbose_name='Default Customer', blank=True, to='crm_core.Customer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='default_supplier',
            field=models.ForeignKey(verbose_name='Default Supplier', blank=True, to='crm_core.Supplier', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='lastmodifiedby',
            field=models.ForeignKey(related_name='db_contractlstmodified', verbose_name='Last modified by', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='staff',
            field=models.ForeignKey(related_name='db_relcontractstaff', verbose_name='Staff', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
