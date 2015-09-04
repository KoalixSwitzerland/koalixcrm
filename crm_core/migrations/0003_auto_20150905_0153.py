# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_core', '0002_auto_20150903_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyContactData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name='Name')),
                ('slogan', models.CharField(max_length=120, null=True, verbose_name='Slogan', blank=True)),
                ('logo', models.ImageField(max_length=200, upload_to=b'', null=True, verbose_name='Logo', blank=True)),
                ('addresser', models.CharField(max_length=200, null=True, verbose_name='Addresser', blank=True)),
                ('addressline1', models.CharField(max_length=200, null=True, verbose_name='Addressline 1', blank=True)),
                ('addressline2', models.CharField(max_length=200, null=True, verbose_name='Addressline 2', blank=True)),
                ('zipcode', models.IntegerField(null=True, verbose_name='Zipcode', blank=True)),
                ('city', models.CharField(max_length=100, null=True, verbose_name='City', blank=True)),
                ('state', models.CharField(max_length=100, null=True, verbose_name='State', blank=True)),
                ('country', models.CharField(blank=True, max_length=2, null=True, verbose_name='Country', choices=[('AF', 'Afghanistan'), ('AL', 'Albania'), ('AQ', 'Antarctica'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AG', 'Antigua and Barbuda'), ('AZ', 'Azerbaijan'), ('AR', 'Argentina'), ('AU', 'Australia'), ('AT', 'Austria'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('AM', 'Armenia'), ('BB', 'Barbados'), ('BE', 'Belgium'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('BZ', 'Belize'), ('IO', 'British Indian Ocean Territory'), ('SB', 'Solomon Islands'), ('VG', 'British Virgin Islands'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('MM', 'Myanmar'), ('BI', 'Burundi'), ('BY', 'Belarus'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('LK', 'Sri Lanka'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('TW', 'Taiwan'), ('CX', 'Christmas Island'), ('CC', 'Cocos'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('YT', 'Mayotte'), ('CG', 'Congo'), ('CD', 'Congo'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('BJ', 'Benin'), ('DK', 'Denmark'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ET', 'Ethiopia'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('FO', 'Faroe Islands'), ('FK', 'Falkland Islands'), ('GS', 'South Georgia and the South Sandwich Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('AX', '\xc5land Islands'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('DJ', 'Djibouti'), ('GA', 'Gabon'), ('GE', 'Georgia'), ('GM', 'Gambia'), ('PS', 'Palestinian Territory'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('KI', 'Kiribati'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GN', 'Guinea'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IL', 'Israel'), ('IT', 'Italy'), ('CI', "Cote d'Ivoire"), ('JM', 'Jamaica'), ('JP', 'Japan'), ('KZ', 'Kazakhstan'), ('JO', 'Jordan'), ('KE', 'Kenya'), ('KP', 'Korea'), ('KR', 'Korea'), ('KW', 'Kuwait'), ('KG', 'Kyrgyz Republic'), ('LA', "Lao People's Democratic Republic"), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LV', 'Latvia'), ('LR', 'Liberia'), ('LY', 'Libyan Arab Jamahiriya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('MX', 'Mexico'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('MD', 'Moldova'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('OM', 'Oman'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('AN', 'Netherlands Antilles'), ('CW', 'Cura\xe7ao'), ('AW', 'Aruba'), ('SX', 'Sint Maarten'), ('BQ', 'Bonaire'), ('NC', 'New Caledonia'), ('VU', 'Vanuatu'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('NO', 'Norway'), ('MP', 'Northern Mariana Islands'), ('UM', 'United States Minor Outlying Islands'), ('FM', 'Micronesia'), ('MH', 'Marshall Islands'), ('PW', 'Palau'), ('PK', 'Pakistan'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn Islands'), ('PL', 'Poland'), ('PT', 'Portugal'), ('GW', 'Guinea-Bissau'), ('TL', 'Timor-Leste'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'Reunion'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint Barthelemy'), ('SH', 'Saint Helena'), ('KN', 'Saint Kitts and Nevis'), ('AI', 'Anguilla'), ('LC', 'Saint Lucia'), ('MF', 'Saint Martin'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SK', 'Slovakia'), ('VN', 'Vietnam'), ('SI', 'Slovenia'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('ZW', 'Zimbabwe'), ('ES', 'Spain'), ('SS', 'South Sudan'), ('EH', 'Western Sahara'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard & Jan Mayen Islands'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TJ', 'Tajikistan'), ('TH', 'Thailand'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('AE', 'United Arab Emirates'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('MK', 'Macedonia'), ('EG', 'Egypt'), ('GB', 'United Kingdom'), ('GG', 'Guernsey'), ('JE', 'Jersey'), ('IM', 'Isle of Man'), ('TZ', 'Tanzania'), ('US', 'United States'), ('VI', 'United States Virgin Islands'), ('BF', 'Burkina Faso'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VE', 'Venezuela'), ('WF', 'Wallis and Futuna'), ('WS', 'Samoa'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('XX', 'Disputed Territory'), ('XE', 'Iraq-Saudi Arabia Neutral Zone'), ('XD', 'United Nations Neutral Zone'), ('XS', 'Spratly Islands')])),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='Phone Number', blank=True)),
                ('email', models.EmailField(max_length=200, null=True, verbose_name='Email Address', blank=True)),
                ('header_text_salesorders', models.TextField(null=True, verbose_name='Header Text On Salesorders', blank=True)),
                ('header_text_purchaseorders', models.TextField(null=True, verbose_name='Header Text On Purchaseorders', blank=True)),
                ('page_footer_left', models.CharField(max_length=40, null=True, verbose_name='Page Footer Left', blank=True)),
                ('footer_text_salesorders', models.TextField(null=True, verbose_name='Footer Text On Salesorders', blank=True)),
                ('footer_text_purchaseorders', models.TextField(null=True, verbose_name='Footer Text On Purchaseorders', blank=True)),
            ],
            options={
                'verbose_name': 'Company settings',
                'verbose_name_plural': 'Company settings',
            },
        ),
        migrations.RemoveField(
            model_name='templateset',
            name='addresser',
        ),
        migrations.RemoveField(
            model_name='templateset',
            name='footer_text_purchaseorders',
        ),
        migrations.RemoveField(
            model_name='templateset',
            name='footer_text_salesorders',
        ),
        migrations.RemoveField(
            model_name='templateset',
            name='header_text_purchaseorders',
        ),
        migrations.RemoveField(
            model_name='templateset',
            name='header_text_salesorders',
        ),
        migrations.RemoveField(
            model_name='templateset',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='templateset',
            name='organisationname',
        ),
        migrations.RemoveField(
            model_name='templateset',
            name='page_footer_left',
        ),
        migrations.RemoveField(
            model_name='templateset',
            name='page_footer_middle',
        ),
        migrations.AlterField(
            model_name='htmlfile',
            name='title',
            field=models.CharField(default='', max_length=60, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='templateset',
            name='title',
            field=models.CharField(max_length=60, verbose_name='Title'),
        ),
    ]
