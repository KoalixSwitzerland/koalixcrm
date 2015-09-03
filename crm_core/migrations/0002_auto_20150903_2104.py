# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('crm_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customerbillingcycle',
            options={'verbose_name': 'Billing Cycle', 'verbose_name_plural': 'Billing Cycles', 'permissions': (('view_customerbillingcycle', 'Can view billing cycles'),)},
        ),
        migrations.AddField(
            model_name='contract',
            name='_meta_title',
            field=models.CharField(help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='created',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='contract',
            name='expiry_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on', blank=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='gen_description',
            field=models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description'),
        ),
        migrations.AddField(
            model_name='contract',
            name='in_sitemap',
            field=models.BooleanField(default=True, verbose_name='Show in sitemap'),
        ),
        migrations.AddField(
            model_name='contract',
            name='keywords_string',
            field=models.CharField(max_length=500, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='publish_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from', db_index=True, blank=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='short_url',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='site',
            field=models.ForeignKey(default=1, editable=False, to='sites.Site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contract',
            name='slug',
            field=models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='status',
            field=models.IntegerField(default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Draft'), (2, 'Published')]),
        ),
        migrations.AddField(
            model_name='contract',
            name='title',
            field=models.CharField(default='', max_length=500, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contract',
            name='updated',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='_meta_title',
            field=models.CharField(help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='created',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='description',
            field=models.TextField(verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='expiry_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on', blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='gen_description',
            field=models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description'),
        ),
        migrations.AddField(
            model_name='customer',
            name='in_sitemap',
            field=models.BooleanField(default=True, verbose_name='Show in sitemap'),
        ),
        migrations.AddField(
            model_name='customer',
            name='keywords_string',
            field=models.CharField(max_length=500, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='publish_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from', db_index=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='short_url',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='site',
            field=models.ForeignKey(default=1, editable=False, to='sites.Site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='slug',
            field=models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.IntegerField(default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Draft'), (2, 'Published')]),
        ),
        migrations.AddField(
            model_name='customer',
            name='title',
            field=models.CharField(default='', max_length=500, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='updated',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='customerbillingcycle',
            name='prefix',
            field=models.CharField(max_length=300, null=True, verbose_name='Prefix'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='_meta_title',
            field=models.CharField(help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='created',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='invoice',
            name='expiry_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on', blank=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='gen_description',
            field=models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='in_sitemap',
            field=models.BooleanField(default=True, verbose_name='Show in sitemap'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='keywords_string',
            field=models.CharField(max_length=500, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='publish_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from', db_index=True, blank=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='short_url',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='site',
            field=models.ForeignKey(default=1, editable=False, to='sites.Site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='slug',
            field=models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.IntegerField(default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Draft'), (2, 'Published')]),
        ),
        migrations.AddField(
            model_name='invoice',
            name='title',
            field=models.CharField(default='', max_length=500, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='updated',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='_meta_title',
            field=models.CharField(help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='created',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='expiry_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on', blank=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='gen_description',
            field=models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='in_sitemap',
            field=models.BooleanField(default=True, verbose_name='Show in sitemap'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='keywords_string',
            field=models.CharField(max_length=500, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='publish_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from', db_index=True, blank=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='short_url',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='site',
            field=models.ForeignKey(default=1, editable=False, to='sites.Site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='slug',
            field=models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='status',
            field=models.IntegerField(default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Draft'), (2, 'Published')]),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='title',
            field=models.CharField(default='', max_length=500, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='updated',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='quote',
            name='_meta_title',
            field=models.CharField(help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='quote',
            name='created',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='quote',
            name='expiry_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on', blank=True),
        ),
        migrations.AddField(
            model_name='quote',
            name='gen_description',
            field=models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description'),
        ),
        migrations.AddField(
            model_name='quote',
            name='in_sitemap',
            field=models.BooleanField(default=True, verbose_name='Show in sitemap'),
        ),
        migrations.AddField(
            model_name='quote',
            name='keywords_string',
            field=models.CharField(max_length=500, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='quote',
            name='publish_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from', db_index=True, blank=True),
        ),
        migrations.AddField(
            model_name='quote',
            name='short_url',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='quote',
            name='site',
            field=models.ForeignKey(default=1, editable=False, to='sites.Site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quote',
            name='slug',
            field=models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True),
        ),
        migrations.AddField(
            model_name='quote',
            name='status',
            field=models.IntegerField(default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Draft'), (2, 'Published')]),
        ),
        migrations.AddField(
            model_name='quote',
            name='title',
            field=models.CharField(default='', max_length=500, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quote',
            name='updated',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='supplier',
            name='_meta_title',
            field=models.CharField(help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='created',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='supplier',
            name='description',
            field=models.TextField(verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='expiry_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on', blank=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='gen_description',
            field=models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='in_sitemap',
            field=models.BooleanField(default=True, verbose_name='Show in sitemap'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='keywords_string',
            field=models.CharField(max_length=500, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='publish_date',
            field=models.DateTimeField(help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from', db_index=True, blank=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='short_url',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='site',
            field=models.ForeignKey(default=1, editable=False, to='sites.Site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='slug',
            field=models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='status',
            field=models.IntegerField(default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Draft'), (2, 'Published')]),
        ),
        migrations.AddField(
            model_name='supplier',
            name='title',
            field=models.CharField(default='', max_length=500, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='updated',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='contract',
            name='default_currency',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Currency', choices=[('USD', 'USD - United States Dollar'), ('EUR', 'EUR - Euro Members'), ('JPY', 'JPY - Japan Yen'), ('GBP', 'GBP - United Kingdom Pound'), ('CHF', 'CHF - Switzerland Franc'), ('AED', 'AED - United Arab Emirates Dirham'), ('AFN', 'AFN - Afghanistan Afghani'), ('ALL', 'ALL - Albania Lek'), ('AMD', 'AMD - Armenia Dram'), ('ANG', 'ANG - Netherlands Antilles Guilder'), ('AOA', 'AOA - Angola Kwanza'), ('ARS', 'ARS - Argentina Peso'), ('AUD', 'AUD - Australia Dollar'), ('AWG', 'AWG - Aruba Guilder'), ('AZN', 'AZN - Azerbaijan New Manat'), ('BAM', 'BAM - Bosnia and Herzegovina Convertible Marka'), ('BBD', 'BBD - Barbados Dollar'), ('BDT', 'BDT - Bangladesh Taka'), ('BGN', 'BGN - Bulgaria Lev'), ('BHD', 'BHD - Bahrain Dinar'), ('BIF', 'BIF - Burundi Franc'), ('BMD', 'BMD - Bermuda Dollar'), ('BND', 'BND - Brunei Darussalam Dollar'), ('BOB', 'BOB - Bolivia Boliviano'), ('BRL', 'BRL - Brazil Real'), ('BSD', 'BSD - Bahamas Dollar'), ('BTN', 'BTN - Bhutan Ngultrum'), ('BWP', 'BWP - Botswana Pula'), ('BYR', 'BYR - Belarus Ruble'), ('BZD', 'BZD - Belize Dollar'), ('CAD', 'CAD - Canada Dollar'), ('CDF', 'CDF - Congo/Kinshasa Franc'), ('CLP', 'CLP - Chile Peso'), ('CNY', 'CNY - China Yuan Renminbi'), ('COP', 'COP - Colombia Peso'), ('CRC', 'CRC - Costa Rica Colon'), ('CUC', 'CUC - Cuba Convertible Peso'), ('CUP', 'CUP - Cuba Peso'), ('CVE', 'CVE - Cape Verde Escudo'), ('CZK', 'CZK - Czech Republic Koruna'), ('DJF', 'DJF - Djibouti Franc'), ('DKK', 'DKK - Denmark Krone'), ('DOP', 'DOP - Dominican Republic Peso'), ('DZD', 'DZD - Algeria Dinar'), ('EGP', 'EGP - Egypt Pound'), ('ERN', 'ERN - Eritrea Nakfa'), ('ETB', 'ETB - Ethiopia Birr'), ('FJD', 'FJD - Fiji Dollar'), ('FKP', 'FKP - Falkland Islands (Malvinas) Pound'), ('GEL', 'GEL - Georgia Lari'), ('GGP', 'GGP - Guernsey Pound'), ('GHS', 'GHS - Ghana Cedi'), ('GIP', 'GIP - Gibraltar Pound'), ('GMD', 'GMD - Gambia Dalasi'), ('GNF', 'GNF - Guinea Franc'), ('GTQ', 'GTQ - Guatemala Quetzal'), ('GYD', 'GYD - Guyana Dollar'), ('HKD', 'HKD - Hong Kong Dollar'), ('HNL', 'HNL - Honduras Lempira'), ('HRK', 'HRK - Croatia Kuna'), ('HTG', 'HTG - Haiti Gourde'), ('HUF', 'HUF - Hungary Forint'), ('IDR', 'IDR - Indonesia Rupiah'), ('ILS', 'ILS - Israel Shekel'), ('IMP', 'IMP - Isle of Man Pound'), ('INR', 'INR - India Rupee'), ('IQD', 'IQD - Iraq Dinar'), ('IRR', 'IRR - Iran Rial'), ('ISK', 'ISK - Iceland Krona'), ('JEP', 'JEP - Jersey Pound'), ('JMD', 'JMD - Jamaica Dollar'), ('JOD', 'JOD - Jordan Dinar'), ('KES', 'KES - Kenya Shilling'), ('KGS', 'KGS - Kyrgyzstan Som'), ('KHR', 'KHR - Cambodia Riel'), ('KMF', 'KMF - Comoros Franc'), ('KPW', 'KPW - Korea (North) Won'), ('KRW', 'KRW - Korea (South) Won'), ('KWD', 'KWD - Kuwait Dinar'), ('KYD', 'KYD - Cayman Islands Dollar'), ('KZT', 'KZT - Kazakhstan Tenge'), ('LAK', 'LAK - Laos Kip'), ('LBP', 'LBP - Lebanon Pound'), ('LKR', 'LKR - Sri Lanka Rupee'), ('LRD', 'LRD - Liberia Dollar'), ('LSL', 'LSL - Lesotho Loti'), ('LTL', 'LTL - Lithuania Litas'), ('LVL', 'LVL - Latvia Lat'), ('LYD', 'LYD - Libya Dinar'), ('MAD', 'MAD - Morocco Dirham'), ('MDL', 'MDL - Moldova Le'), ('MGA', 'MGA - Madagascar Ariary'), ('MKD', 'MKD - Macedonia Denar'), ('MMK', 'MMK - Myanmar (Burma) Kyat'), ('MNT', 'MNT - Mongolia Tughrik'), ('MOP', 'MOP - Macau Pataca'), ('MRO', 'MRO - Mauritania Ouguiya'), ('MUR', 'MUR - Mauritius Rupee'), ('MVR', 'MVR - Maldives (Maldive Islands) Rufiyaa'), ('MWK', 'MWK - Malawi Kwacha'), ('MXN', 'MXN - Mexico Peso'), ('MYR', 'MYR - Malaysia Ringgit'), ('MZN', 'MZN - Mozambique Metical'), ('NAD', 'NAD - Namibia Dollar'), ('NGN', 'NGN - Nigeria Naira'), ('NIO', 'NIO - Nicaragua Cordoba'), ('NOK', 'NOK - Norway Krone'), ('NPR', 'NPR - Nepal Rupee'), ('NZD', 'NZD - New Zealand Dollar'), ('OMR', 'OMR - Oman Rial'), ('PAB', 'PAB - Panama Balboa'), ('PEN', 'PEN - Peru Nuevo Sol'), ('PGK', 'PGK - Papua New Guinea Kina'), ('PHP', 'PHP - Philippines Peso'), ('PKR', 'PKR - Pakistan Rupee'), ('PLN', 'PLN - Poland Zloty'), ('PYG', 'PYG - Paraguay Guarani'), ('QAR', 'QAR - Qatar Riyal'), ('RON', 'RON - Romania New Le'), ('RSD', 'RSD - Serbia Dinar'), ('RUB', 'RUB - Russia Ruble'), ('RWF', 'RWF - Rwanda Franc'), ('SAR', 'SAR - Saudi Arabia Riyal'), ('SBD', 'SBD - Solomon Islands Dollar'), ('SCR', 'SCR - Seychelles Rupee'), ('SDG', 'SDG - Sudan Pound'), ('SEK', 'SEK - Sweden Krona'), ('SGD', 'SGD - Singapore Dollar'), ('SHP', 'SHP - Saint Helena Pound'), ('SLL', 'SLL - Sierra Leone Leone'), ('SOS', 'SOS - Somalia Shilling'), ('SPL', 'SPL - Seborga Luigino'), ('SRD', 'SRD - Suriname Dollar'), ('STD', 'STD - S\xe3o Tom\xe9 and Pr\xedncipe Dobra'), ('SVC', 'SVC - El Salvador Colon'), ('SYP', 'SYP - Syria Pound'), ('SZL', 'SZL - Swaziland Lilangeni'), ('THB', 'THB - Thailand Baht'), ('TJS', 'TJS - Tajikistan Somoni'), ('TMT', 'TMT - Turkmenistan Manat'), ('TND', 'TND - Tunisia Dinar'), ('TOP', "TOP - Tonga Pa'anga"), ('TRY', 'TRY - Turkey Lira'), ('TTD', 'TTD - Trinidad and Tobago Dollar'), ('TVD', 'TVD - Tuvalu Dollar'), ('TWD', 'TWD - Taiwan New Dollar'), ('TZS', 'TZS - Tanzania Shilling'), ('UAH', 'UAH - Ukraine Hryvna'), ('UGX', 'UGX - Uganda Shilling'), ('UYU', 'UYU - Uruguay Peso'), ('UZS', 'UZS - Uzbekistan Som'), ('VEF', 'VEF - Venezuela Bolivar'), ('VND', 'VND - Viet Nam Dong'), ('VUV', 'VUV - Vanuatu Vat'), ('WST', 'WST - Samoa Tala'), ('XAF', 'XAF - Communaut\xe9 Financi\xe8re Africaine (BEAC) CFA Franc BEAC'), ('XCD', 'XCD - East Caribbean Dollar'), ('XDR', 'XDR - International Monetary Fund (IMF) Special Drawing Rights'), ('XOF', 'XOF - Communaut\xe9 Financi\xe8re Africaine (BCEAO) Franc'), ('XPF', 'XPF - Comptoirs Fran\xe7ais du Pacifique (CFP) Franc'), ('YER', 'YER - Yemen Rial'), ('ZAR', 'ZAR - South Africa Rand'), ('ZMK', 'ZMK - Zambia Kwacha'), ('ZWD', 'ZWD - Zimbabwe Dollar')]),
        ),
        migrations.AlterField(
            model_name='contract',
            name='description',
            field=models.TextField(default='', verbose_name='Description', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='billingcycle',
            field=models.ForeignKey(verbose_name='Billing Cycle', to='crm_core.CustomerBillingCycle'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='default_currency',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Currency', choices=[('USD', 'USD - United States Dollar'), ('EUR', 'EUR - Euro Members'), ('JPY', 'JPY - Japan Yen'), ('GBP', 'GBP - United Kingdom Pound'), ('CHF', 'CHF - Switzerland Franc'), ('AED', 'AED - United Arab Emirates Dirham'), ('AFN', 'AFN - Afghanistan Afghani'), ('ALL', 'ALL - Albania Lek'), ('AMD', 'AMD - Armenia Dram'), ('ANG', 'ANG - Netherlands Antilles Guilder'), ('AOA', 'AOA - Angola Kwanza'), ('ARS', 'ARS - Argentina Peso'), ('AUD', 'AUD - Australia Dollar'), ('AWG', 'AWG - Aruba Guilder'), ('AZN', 'AZN - Azerbaijan New Manat'), ('BAM', 'BAM - Bosnia and Herzegovina Convertible Marka'), ('BBD', 'BBD - Barbados Dollar'), ('BDT', 'BDT - Bangladesh Taka'), ('BGN', 'BGN - Bulgaria Lev'), ('BHD', 'BHD - Bahrain Dinar'), ('BIF', 'BIF - Burundi Franc'), ('BMD', 'BMD - Bermuda Dollar'), ('BND', 'BND - Brunei Darussalam Dollar'), ('BOB', 'BOB - Bolivia Boliviano'), ('BRL', 'BRL - Brazil Real'), ('BSD', 'BSD - Bahamas Dollar'), ('BTN', 'BTN - Bhutan Ngultrum'), ('BWP', 'BWP - Botswana Pula'), ('BYR', 'BYR - Belarus Ruble'), ('BZD', 'BZD - Belize Dollar'), ('CAD', 'CAD - Canada Dollar'), ('CDF', 'CDF - Congo/Kinshasa Franc'), ('CLP', 'CLP - Chile Peso'), ('CNY', 'CNY - China Yuan Renminbi'), ('COP', 'COP - Colombia Peso'), ('CRC', 'CRC - Costa Rica Colon'), ('CUC', 'CUC - Cuba Convertible Peso'), ('CUP', 'CUP - Cuba Peso'), ('CVE', 'CVE - Cape Verde Escudo'), ('CZK', 'CZK - Czech Republic Koruna'), ('DJF', 'DJF - Djibouti Franc'), ('DKK', 'DKK - Denmark Krone'), ('DOP', 'DOP - Dominican Republic Peso'), ('DZD', 'DZD - Algeria Dinar'), ('EGP', 'EGP - Egypt Pound'), ('ERN', 'ERN - Eritrea Nakfa'), ('ETB', 'ETB - Ethiopia Birr'), ('FJD', 'FJD - Fiji Dollar'), ('FKP', 'FKP - Falkland Islands (Malvinas) Pound'), ('GEL', 'GEL - Georgia Lari'), ('GGP', 'GGP - Guernsey Pound'), ('GHS', 'GHS - Ghana Cedi'), ('GIP', 'GIP - Gibraltar Pound'), ('GMD', 'GMD - Gambia Dalasi'), ('GNF', 'GNF - Guinea Franc'), ('GTQ', 'GTQ - Guatemala Quetzal'), ('GYD', 'GYD - Guyana Dollar'), ('HKD', 'HKD - Hong Kong Dollar'), ('HNL', 'HNL - Honduras Lempira'), ('HRK', 'HRK - Croatia Kuna'), ('HTG', 'HTG - Haiti Gourde'), ('HUF', 'HUF - Hungary Forint'), ('IDR', 'IDR - Indonesia Rupiah'), ('ILS', 'ILS - Israel Shekel'), ('IMP', 'IMP - Isle of Man Pound'), ('INR', 'INR - India Rupee'), ('IQD', 'IQD - Iraq Dinar'), ('IRR', 'IRR - Iran Rial'), ('ISK', 'ISK - Iceland Krona'), ('JEP', 'JEP - Jersey Pound'), ('JMD', 'JMD - Jamaica Dollar'), ('JOD', 'JOD - Jordan Dinar'), ('KES', 'KES - Kenya Shilling'), ('KGS', 'KGS - Kyrgyzstan Som'), ('KHR', 'KHR - Cambodia Riel'), ('KMF', 'KMF - Comoros Franc'), ('KPW', 'KPW - Korea (North) Won'), ('KRW', 'KRW - Korea (South) Won'), ('KWD', 'KWD - Kuwait Dinar'), ('KYD', 'KYD - Cayman Islands Dollar'), ('KZT', 'KZT - Kazakhstan Tenge'), ('LAK', 'LAK - Laos Kip'), ('LBP', 'LBP - Lebanon Pound'), ('LKR', 'LKR - Sri Lanka Rupee'), ('LRD', 'LRD - Liberia Dollar'), ('LSL', 'LSL - Lesotho Loti'), ('LTL', 'LTL - Lithuania Litas'), ('LVL', 'LVL - Latvia Lat'), ('LYD', 'LYD - Libya Dinar'), ('MAD', 'MAD - Morocco Dirham'), ('MDL', 'MDL - Moldova Le'), ('MGA', 'MGA - Madagascar Ariary'), ('MKD', 'MKD - Macedonia Denar'), ('MMK', 'MMK - Myanmar (Burma) Kyat'), ('MNT', 'MNT - Mongolia Tughrik'), ('MOP', 'MOP - Macau Pataca'), ('MRO', 'MRO - Mauritania Ouguiya'), ('MUR', 'MUR - Mauritius Rupee'), ('MVR', 'MVR - Maldives (Maldive Islands) Rufiyaa'), ('MWK', 'MWK - Malawi Kwacha'), ('MXN', 'MXN - Mexico Peso'), ('MYR', 'MYR - Malaysia Ringgit'), ('MZN', 'MZN - Mozambique Metical'), ('NAD', 'NAD - Namibia Dollar'), ('NGN', 'NGN - Nigeria Naira'), ('NIO', 'NIO - Nicaragua Cordoba'), ('NOK', 'NOK - Norway Krone'), ('NPR', 'NPR - Nepal Rupee'), ('NZD', 'NZD - New Zealand Dollar'), ('OMR', 'OMR - Oman Rial'), ('PAB', 'PAB - Panama Balboa'), ('PEN', 'PEN - Peru Nuevo Sol'), ('PGK', 'PGK - Papua New Guinea Kina'), ('PHP', 'PHP - Philippines Peso'), ('PKR', 'PKR - Pakistan Rupee'), ('PLN', 'PLN - Poland Zloty'), ('PYG', 'PYG - Paraguay Guarani'), ('QAR', 'QAR - Qatar Riyal'), ('RON', 'RON - Romania New Le'), ('RSD', 'RSD - Serbia Dinar'), ('RUB', 'RUB - Russia Ruble'), ('RWF', 'RWF - Rwanda Franc'), ('SAR', 'SAR - Saudi Arabia Riyal'), ('SBD', 'SBD - Solomon Islands Dollar'), ('SCR', 'SCR - Seychelles Rupee'), ('SDG', 'SDG - Sudan Pound'), ('SEK', 'SEK - Sweden Krona'), ('SGD', 'SGD - Singapore Dollar'), ('SHP', 'SHP - Saint Helena Pound'), ('SLL', 'SLL - Sierra Leone Leone'), ('SOS', 'SOS - Somalia Shilling'), ('SPL', 'SPL - Seborga Luigino'), ('SRD', 'SRD - Suriname Dollar'), ('STD', 'STD - S\xe3o Tom\xe9 and Pr\xedncipe Dobra'), ('SVC', 'SVC - El Salvador Colon'), ('SYP', 'SYP - Syria Pound'), ('SZL', 'SZL - Swaziland Lilangeni'), ('THB', 'THB - Thailand Baht'), ('TJS', 'TJS - Tajikistan Somoni'), ('TMT', 'TMT - Turkmenistan Manat'), ('TND', 'TND - Tunisia Dinar'), ('TOP', "TOP - Tonga Pa'anga"), ('TRY', 'TRY - Turkey Lira'), ('TTD', 'TTD - Trinidad and Tobago Dollar'), ('TVD', 'TVD - Tuvalu Dollar'), ('TWD', 'TWD - Taiwan New Dollar'), ('TZS', 'TZS - Tanzania Shilling'), ('UAH', 'UAH - Ukraine Hryvna'), ('UGX', 'UGX - Uganda Shilling'), ('UYU', 'UYU - Uruguay Peso'), ('UZS', 'UZS - Uzbekistan Som'), ('VEF', 'VEF - Venezuela Bolivar'), ('VND', 'VND - Viet Nam Dong'), ('VUV', 'VUV - Vanuatu Vat'), ('WST', 'WST - Samoa Tala'), ('XAF', 'XAF - Communaut\xe9 Financi\xe8re Africaine (BEAC) CFA Franc BEAC'), ('XCD', 'XCD - East Caribbean Dollar'), ('XDR', 'XDR - International Monetary Fund (IMF) Special Drawing Rights'), ('XOF', 'XOF - Communaut\xe9 Financi\xe8re Africaine (BCEAO) Franc'), ('XPF', 'XPF - Comptoirs Fran\xe7ais du Pacifique (CFP) Franc'), ('YER', 'YER - Yemen Rial'), ('ZAR', 'ZAR - South Africa Rand'), ('ZMK', 'ZMK - Zambia Kwacha'), ('ZWD', 'ZWD - Zimbabwe Dollar')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='ismemberof',
            field=models.ManyToManyField(to='crm_core.CustomerGroup', verbose_name='Is member of', blank=True),
        ),
        migrations.AlterField(
            model_name='customergroup',
            name='name',
            field=models.CharField(max_length=300, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='description',
            field=models.TextField(default='', verbose_name='Description', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='producttax',
            name='tax',
            field=models.ForeignKey(verbose_name='Tax Rate', to='crm_core.TaxRate'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='description',
            field=models.TextField(default='', verbose_name='Description', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quote',
            name='description',
            field=models.TextField(default='', verbose_name='Description', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='supplier',
            name='default_currency',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Currency', choices=[('USD', 'USD - United States Dollar'), ('EUR', 'EUR - Euro Members'), ('JPY', 'JPY - Japan Yen'), ('GBP', 'GBP - United Kingdom Pound'), ('CHF', 'CHF - Switzerland Franc'), ('AED', 'AED - United Arab Emirates Dirham'), ('AFN', 'AFN - Afghanistan Afghani'), ('ALL', 'ALL - Albania Lek'), ('AMD', 'AMD - Armenia Dram'), ('ANG', 'ANG - Netherlands Antilles Guilder'), ('AOA', 'AOA - Angola Kwanza'), ('ARS', 'ARS - Argentina Peso'), ('AUD', 'AUD - Australia Dollar'), ('AWG', 'AWG - Aruba Guilder'), ('AZN', 'AZN - Azerbaijan New Manat'), ('BAM', 'BAM - Bosnia and Herzegovina Convertible Marka'), ('BBD', 'BBD - Barbados Dollar'), ('BDT', 'BDT - Bangladesh Taka'), ('BGN', 'BGN - Bulgaria Lev'), ('BHD', 'BHD - Bahrain Dinar'), ('BIF', 'BIF - Burundi Franc'), ('BMD', 'BMD - Bermuda Dollar'), ('BND', 'BND - Brunei Darussalam Dollar'), ('BOB', 'BOB - Bolivia Boliviano'), ('BRL', 'BRL - Brazil Real'), ('BSD', 'BSD - Bahamas Dollar'), ('BTN', 'BTN - Bhutan Ngultrum'), ('BWP', 'BWP - Botswana Pula'), ('BYR', 'BYR - Belarus Ruble'), ('BZD', 'BZD - Belize Dollar'), ('CAD', 'CAD - Canada Dollar'), ('CDF', 'CDF - Congo/Kinshasa Franc'), ('CLP', 'CLP - Chile Peso'), ('CNY', 'CNY - China Yuan Renminbi'), ('COP', 'COP - Colombia Peso'), ('CRC', 'CRC - Costa Rica Colon'), ('CUC', 'CUC - Cuba Convertible Peso'), ('CUP', 'CUP - Cuba Peso'), ('CVE', 'CVE - Cape Verde Escudo'), ('CZK', 'CZK - Czech Republic Koruna'), ('DJF', 'DJF - Djibouti Franc'), ('DKK', 'DKK - Denmark Krone'), ('DOP', 'DOP - Dominican Republic Peso'), ('DZD', 'DZD - Algeria Dinar'), ('EGP', 'EGP - Egypt Pound'), ('ERN', 'ERN - Eritrea Nakfa'), ('ETB', 'ETB - Ethiopia Birr'), ('FJD', 'FJD - Fiji Dollar'), ('FKP', 'FKP - Falkland Islands (Malvinas) Pound'), ('GEL', 'GEL - Georgia Lari'), ('GGP', 'GGP - Guernsey Pound'), ('GHS', 'GHS - Ghana Cedi'), ('GIP', 'GIP - Gibraltar Pound'), ('GMD', 'GMD - Gambia Dalasi'), ('GNF', 'GNF - Guinea Franc'), ('GTQ', 'GTQ - Guatemala Quetzal'), ('GYD', 'GYD - Guyana Dollar'), ('HKD', 'HKD - Hong Kong Dollar'), ('HNL', 'HNL - Honduras Lempira'), ('HRK', 'HRK - Croatia Kuna'), ('HTG', 'HTG - Haiti Gourde'), ('HUF', 'HUF - Hungary Forint'), ('IDR', 'IDR - Indonesia Rupiah'), ('ILS', 'ILS - Israel Shekel'), ('IMP', 'IMP - Isle of Man Pound'), ('INR', 'INR - India Rupee'), ('IQD', 'IQD - Iraq Dinar'), ('IRR', 'IRR - Iran Rial'), ('ISK', 'ISK - Iceland Krona'), ('JEP', 'JEP - Jersey Pound'), ('JMD', 'JMD - Jamaica Dollar'), ('JOD', 'JOD - Jordan Dinar'), ('KES', 'KES - Kenya Shilling'), ('KGS', 'KGS - Kyrgyzstan Som'), ('KHR', 'KHR - Cambodia Riel'), ('KMF', 'KMF - Comoros Franc'), ('KPW', 'KPW - Korea (North) Won'), ('KRW', 'KRW - Korea (South) Won'), ('KWD', 'KWD - Kuwait Dinar'), ('KYD', 'KYD - Cayman Islands Dollar'), ('KZT', 'KZT - Kazakhstan Tenge'), ('LAK', 'LAK - Laos Kip'), ('LBP', 'LBP - Lebanon Pound'), ('LKR', 'LKR - Sri Lanka Rupee'), ('LRD', 'LRD - Liberia Dollar'), ('LSL', 'LSL - Lesotho Loti'), ('LTL', 'LTL - Lithuania Litas'), ('LVL', 'LVL - Latvia Lat'), ('LYD', 'LYD - Libya Dinar'), ('MAD', 'MAD - Morocco Dirham'), ('MDL', 'MDL - Moldova Le'), ('MGA', 'MGA - Madagascar Ariary'), ('MKD', 'MKD - Macedonia Denar'), ('MMK', 'MMK - Myanmar (Burma) Kyat'), ('MNT', 'MNT - Mongolia Tughrik'), ('MOP', 'MOP - Macau Pataca'), ('MRO', 'MRO - Mauritania Ouguiya'), ('MUR', 'MUR - Mauritius Rupee'), ('MVR', 'MVR - Maldives (Maldive Islands) Rufiyaa'), ('MWK', 'MWK - Malawi Kwacha'), ('MXN', 'MXN - Mexico Peso'), ('MYR', 'MYR - Malaysia Ringgit'), ('MZN', 'MZN - Mozambique Metical'), ('NAD', 'NAD - Namibia Dollar'), ('NGN', 'NGN - Nigeria Naira'), ('NIO', 'NIO - Nicaragua Cordoba'), ('NOK', 'NOK - Norway Krone'), ('NPR', 'NPR - Nepal Rupee'), ('NZD', 'NZD - New Zealand Dollar'), ('OMR', 'OMR - Oman Rial'), ('PAB', 'PAB - Panama Balboa'), ('PEN', 'PEN - Peru Nuevo Sol'), ('PGK', 'PGK - Papua New Guinea Kina'), ('PHP', 'PHP - Philippines Peso'), ('PKR', 'PKR - Pakistan Rupee'), ('PLN', 'PLN - Poland Zloty'), ('PYG', 'PYG - Paraguay Guarani'), ('QAR', 'QAR - Qatar Riyal'), ('RON', 'RON - Romania New Le'), ('RSD', 'RSD - Serbia Dinar'), ('RUB', 'RUB - Russia Ruble'), ('RWF', 'RWF - Rwanda Franc'), ('SAR', 'SAR - Saudi Arabia Riyal'), ('SBD', 'SBD - Solomon Islands Dollar'), ('SCR', 'SCR - Seychelles Rupee'), ('SDG', 'SDG - Sudan Pound'), ('SEK', 'SEK - Sweden Krona'), ('SGD', 'SGD - Singapore Dollar'), ('SHP', 'SHP - Saint Helena Pound'), ('SLL', 'SLL - Sierra Leone Leone'), ('SOS', 'SOS - Somalia Shilling'), ('SPL', 'SPL - Seborga Luigino'), ('SRD', 'SRD - Suriname Dollar'), ('STD', 'STD - S\xe3o Tom\xe9 and Pr\xedncipe Dobra'), ('SVC', 'SVC - El Salvador Colon'), ('SYP', 'SYP - Syria Pound'), ('SZL', 'SZL - Swaziland Lilangeni'), ('THB', 'THB - Thailand Baht'), ('TJS', 'TJS - Tajikistan Somoni'), ('TMT', 'TMT - Turkmenistan Manat'), ('TND', 'TND - Tunisia Dinar'), ('TOP', "TOP - Tonga Pa'anga"), ('TRY', 'TRY - Turkey Lira'), ('TTD', 'TTD - Trinidad and Tobago Dollar'), ('TVD', 'TVD - Tuvalu Dollar'), ('TWD', 'TWD - Taiwan New Dollar'), ('TZS', 'TZS - Tanzania Shilling'), ('UAH', 'UAH - Ukraine Hryvna'), ('UGX', 'UGX - Uganda Shilling'), ('UYU', 'UYU - Uruguay Peso'), ('UZS', 'UZS - Uzbekistan Som'), ('VEF', 'VEF - Venezuela Bolivar'), ('VND', 'VND - Viet Nam Dong'), ('VUV', 'VUV - Vanuatu Vat'), ('WST', 'WST - Samoa Tala'), ('XAF', 'XAF - Communaut\xe9 Financi\xe8re Africaine (BEAC) CFA Franc BEAC'), ('XCD', 'XCD - East Caribbean Dollar'), ('XDR', 'XDR - International Monetary Fund (IMF) Special Drawing Rights'), ('XOF', 'XOF - Communaut\xe9 Financi\xe8re Africaine (BCEAO) Franc'), ('XPF', 'XPF - Comptoirs Fran\xe7ais du Pacifique (CFP) Franc'), ('YER', 'YER - Yemen Rial'), ('ZAR', 'ZAR - South Africa Rand'), ('ZMK', 'ZMK - Zambia Kwacha'), ('ZWD', 'ZWD - Zimbabwe Dollar')]),
        ),
        migrations.AlterField(
            model_name='userextension',
            name='default_currency',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Currency', choices=[('USD', 'USD - United States Dollar'), ('EUR', 'EUR - Euro Members'), ('JPY', 'JPY - Japan Yen'), ('GBP', 'GBP - United Kingdom Pound'), ('CHF', 'CHF - Switzerland Franc'), ('AED', 'AED - United Arab Emirates Dirham'), ('AFN', 'AFN - Afghanistan Afghani'), ('ALL', 'ALL - Albania Lek'), ('AMD', 'AMD - Armenia Dram'), ('ANG', 'ANG - Netherlands Antilles Guilder'), ('AOA', 'AOA - Angola Kwanza'), ('ARS', 'ARS - Argentina Peso'), ('AUD', 'AUD - Australia Dollar'), ('AWG', 'AWG - Aruba Guilder'), ('AZN', 'AZN - Azerbaijan New Manat'), ('BAM', 'BAM - Bosnia and Herzegovina Convertible Marka'), ('BBD', 'BBD - Barbados Dollar'), ('BDT', 'BDT - Bangladesh Taka'), ('BGN', 'BGN - Bulgaria Lev'), ('BHD', 'BHD - Bahrain Dinar'), ('BIF', 'BIF - Burundi Franc'), ('BMD', 'BMD - Bermuda Dollar'), ('BND', 'BND - Brunei Darussalam Dollar'), ('BOB', 'BOB - Bolivia Boliviano'), ('BRL', 'BRL - Brazil Real'), ('BSD', 'BSD - Bahamas Dollar'), ('BTN', 'BTN - Bhutan Ngultrum'), ('BWP', 'BWP - Botswana Pula'), ('BYR', 'BYR - Belarus Ruble'), ('BZD', 'BZD - Belize Dollar'), ('CAD', 'CAD - Canada Dollar'), ('CDF', 'CDF - Congo/Kinshasa Franc'), ('CLP', 'CLP - Chile Peso'), ('CNY', 'CNY - China Yuan Renminbi'), ('COP', 'COP - Colombia Peso'), ('CRC', 'CRC - Costa Rica Colon'), ('CUC', 'CUC - Cuba Convertible Peso'), ('CUP', 'CUP - Cuba Peso'), ('CVE', 'CVE - Cape Verde Escudo'), ('CZK', 'CZK - Czech Republic Koruna'), ('DJF', 'DJF - Djibouti Franc'), ('DKK', 'DKK - Denmark Krone'), ('DOP', 'DOP - Dominican Republic Peso'), ('DZD', 'DZD - Algeria Dinar'), ('EGP', 'EGP - Egypt Pound'), ('ERN', 'ERN - Eritrea Nakfa'), ('ETB', 'ETB - Ethiopia Birr'), ('FJD', 'FJD - Fiji Dollar'), ('FKP', 'FKP - Falkland Islands (Malvinas) Pound'), ('GEL', 'GEL - Georgia Lari'), ('GGP', 'GGP - Guernsey Pound'), ('GHS', 'GHS - Ghana Cedi'), ('GIP', 'GIP - Gibraltar Pound'), ('GMD', 'GMD - Gambia Dalasi'), ('GNF', 'GNF - Guinea Franc'), ('GTQ', 'GTQ - Guatemala Quetzal'), ('GYD', 'GYD - Guyana Dollar'), ('HKD', 'HKD - Hong Kong Dollar'), ('HNL', 'HNL - Honduras Lempira'), ('HRK', 'HRK - Croatia Kuna'), ('HTG', 'HTG - Haiti Gourde'), ('HUF', 'HUF - Hungary Forint'), ('IDR', 'IDR - Indonesia Rupiah'), ('ILS', 'ILS - Israel Shekel'), ('IMP', 'IMP - Isle of Man Pound'), ('INR', 'INR - India Rupee'), ('IQD', 'IQD - Iraq Dinar'), ('IRR', 'IRR - Iran Rial'), ('ISK', 'ISK - Iceland Krona'), ('JEP', 'JEP - Jersey Pound'), ('JMD', 'JMD - Jamaica Dollar'), ('JOD', 'JOD - Jordan Dinar'), ('KES', 'KES - Kenya Shilling'), ('KGS', 'KGS - Kyrgyzstan Som'), ('KHR', 'KHR - Cambodia Riel'), ('KMF', 'KMF - Comoros Franc'), ('KPW', 'KPW - Korea (North) Won'), ('KRW', 'KRW - Korea (South) Won'), ('KWD', 'KWD - Kuwait Dinar'), ('KYD', 'KYD - Cayman Islands Dollar'), ('KZT', 'KZT - Kazakhstan Tenge'), ('LAK', 'LAK - Laos Kip'), ('LBP', 'LBP - Lebanon Pound'), ('LKR', 'LKR - Sri Lanka Rupee'), ('LRD', 'LRD - Liberia Dollar'), ('LSL', 'LSL - Lesotho Loti'), ('LTL', 'LTL - Lithuania Litas'), ('LVL', 'LVL - Latvia Lat'), ('LYD', 'LYD - Libya Dinar'), ('MAD', 'MAD - Morocco Dirham'), ('MDL', 'MDL - Moldova Le'), ('MGA', 'MGA - Madagascar Ariary'), ('MKD', 'MKD - Macedonia Denar'), ('MMK', 'MMK - Myanmar (Burma) Kyat'), ('MNT', 'MNT - Mongolia Tughrik'), ('MOP', 'MOP - Macau Pataca'), ('MRO', 'MRO - Mauritania Ouguiya'), ('MUR', 'MUR - Mauritius Rupee'), ('MVR', 'MVR - Maldives (Maldive Islands) Rufiyaa'), ('MWK', 'MWK - Malawi Kwacha'), ('MXN', 'MXN - Mexico Peso'), ('MYR', 'MYR - Malaysia Ringgit'), ('MZN', 'MZN - Mozambique Metical'), ('NAD', 'NAD - Namibia Dollar'), ('NGN', 'NGN - Nigeria Naira'), ('NIO', 'NIO - Nicaragua Cordoba'), ('NOK', 'NOK - Norway Krone'), ('NPR', 'NPR - Nepal Rupee'), ('NZD', 'NZD - New Zealand Dollar'), ('OMR', 'OMR - Oman Rial'), ('PAB', 'PAB - Panama Balboa'), ('PEN', 'PEN - Peru Nuevo Sol'), ('PGK', 'PGK - Papua New Guinea Kina'), ('PHP', 'PHP - Philippines Peso'), ('PKR', 'PKR - Pakistan Rupee'), ('PLN', 'PLN - Poland Zloty'), ('PYG', 'PYG - Paraguay Guarani'), ('QAR', 'QAR - Qatar Riyal'), ('RON', 'RON - Romania New Le'), ('RSD', 'RSD - Serbia Dinar'), ('RUB', 'RUB - Russia Ruble'), ('RWF', 'RWF - Rwanda Franc'), ('SAR', 'SAR - Saudi Arabia Riyal'), ('SBD', 'SBD - Solomon Islands Dollar'), ('SCR', 'SCR - Seychelles Rupee'), ('SDG', 'SDG - Sudan Pound'), ('SEK', 'SEK - Sweden Krona'), ('SGD', 'SGD - Singapore Dollar'), ('SHP', 'SHP - Saint Helena Pound'), ('SLL', 'SLL - Sierra Leone Leone'), ('SOS', 'SOS - Somalia Shilling'), ('SPL', 'SPL - Seborga Luigino'), ('SRD', 'SRD - Suriname Dollar'), ('STD', 'STD - S\xe3o Tom\xe9 and Pr\xedncipe Dobra'), ('SVC', 'SVC - El Salvador Colon'), ('SYP', 'SYP - Syria Pound'), ('SZL', 'SZL - Swaziland Lilangeni'), ('THB', 'THB - Thailand Baht'), ('TJS', 'TJS - Tajikistan Somoni'), ('TMT', 'TMT - Turkmenistan Manat'), ('TND', 'TND - Tunisia Dinar'), ('TOP', "TOP - Tonga Pa'anga"), ('TRY', 'TRY - Turkey Lira'), ('TTD', 'TTD - Trinidad and Tobago Dollar'), ('TVD', 'TVD - Tuvalu Dollar'), ('TWD', 'TWD - Taiwan New Dollar'), ('TZS', 'TZS - Tanzania Shilling'), ('UAH', 'UAH - Ukraine Hryvna'), ('UGX', 'UGX - Uganda Shilling'), ('UYU', 'UYU - Uruguay Peso'), ('UZS', 'UZS - Uzbekistan Som'), ('VEF', 'VEF - Venezuela Bolivar'), ('VND', 'VND - Viet Nam Dong'), ('VUV', 'VUV - Vanuatu Vat'), ('WST', 'WST - Samoa Tala'), ('XAF', 'XAF - Communaut\xe9 Financi\xe8re Africaine (BEAC) CFA Franc BEAC'), ('XCD', 'XCD - East Caribbean Dollar'), ('XDR', 'XDR - International Monetary Fund (IMF) Special Drawing Rights'), ('XOF', 'XOF - Communaut\xe9 Financi\xe8re Africaine (BCEAO) Franc'), ('XPF', 'XPF - Comptoirs Fran\xe7ais du Pacifique (CFP) Franc'), ('YER', 'YER - Yemen Rial'), ('ZAR', 'ZAR - South Africa Rand'), ('ZMK', 'ZMK - Zambia Kwacha'), ('ZWD', 'ZWD - Zimbabwe Dollar')]),
        ),
        migrations.AlterField(
            model_name='userextension',
            name='default_templateset',
            field=models.ForeignKey(verbose_name='Vorlagen', blank=True, to='crm_core.TemplateSet', null=True),
        ),
        migrations.AlterField(
            model_name='userextension',
            name='image',
            field=models.ImageField(default=b'avatars/avatar.jpg', upload_to=b'avatars/', null=True, verbose_name='Bild', blank=True),
        ),
        migrations.AlterField(
            model_name='userextension',
            name='user',
            field=models.OneToOneField(related_name='extension', verbose_name='Benutzer', to=settings.AUTH_USER_MODEL),
        ),
    ]
