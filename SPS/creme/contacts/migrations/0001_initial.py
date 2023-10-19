# Generated by Django 4.2.6 on 2023-10-13 14:33

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "salutation",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="Salutation",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=255, verbose_name="First name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=255, verbose_name="Last name"),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "organization",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Organization"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, default="", max_length=255, verbose_name="Title"
                    ),
                ),
                ("primary_email", models.EmailField(max_length=254, unique=True)),
                (
                    "secondary_email",
                    models.EmailField(blank=True, default="", max_length=254),
                ),
                (
                    "mobile_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, null=True, region=None, unique=True
                    ),
                ),
                (
                    "secondary_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, null=True, region=None
                    ),
                ),
                (
                    "department",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Department"
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Language"
                    ),
                ),
                ("do_not_call", models.BooleanField(default=False)),
                ("description", models.TextField(blank=True, null=True)),
                ("linked_in_url", models.URLField(blank=True, null=True)),
                ("facebook_url", models.URLField(blank=True, null=True)),
                ("twitter_username", models.CharField(max_length=255, null=True)),
                (
                    "created_on",
                    models.DateTimeField(auto_now=True, verbose_name="Created on"),
                ),
                ("is_active", models.BooleanField(default=False)),
                (
                    "country",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("GB", "United Kingdom"),
                            ("AF", "Afghanistan"),
                            ("AX", "Aland Islands"),
                            ("AL", "Albania"),
                            ("DZ", "Algeria"),
                            ("AS", "American Samoa"),
                            ("AD", "Andorra"),
                            ("AO", "Angola"),
                            ("AI", "Anguilla"),
                            ("AQ", "Antarctica"),
                            ("AG", "Antigua and Barbuda"),
                            ("AR", "Argentina"),
                            ("AM", "Armenia"),
                            ("AW", "Aruba"),
                            ("AU", "Australia"),
                            ("AT", "Austria"),
                            ("AZ", "Azerbaijan"),
                            ("BS", "Bahamas"),
                            ("BH", "Bahrain"),
                            ("BD", "Bangladesh"),
                            ("BB", "Barbados"),
                            ("BY", "Belarus"),
                            ("BE", "Belgium"),
                            ("BZ", "Belize"),
                            ("BJ", "Benin"),
                            ("BM", "Bermuda"),
                            ("BT", "Bhutan"),
                            ("BO", "Bolivia"),
                            ("BA", "Bosnia and Herzegovina"),
                            ("BW", "Botswana"),
                            ("BV", "Bouvet Island"),
                            ("BR", "Brazil"),
                            ("IO", "British Indian Ocean Territory"),
                            ("BN", "Brunei Darussalam"),
                            ("BG", "Bulgaria"),
                            ("BF", "Burkina Faso"),
                            ("BI", "Burundi"),
                            ("KH", "Cambodia"),
                            ("CM", "Cameroon"),
                            ("CA", "Canada"),
                            ("CV", "Cape Verde"),
                            ("KY", "Cayman Islands"),
                            ("CF", "Central African Republic"),
                            ("TD", "Chad"),
                            ("CL", "Chile"),
                            ("CN", "China"),
                            ("CX", "Christmas Island"),
                            ("CC", "Cocos (Keeling) Islands"),
                            ("CO", "Colombia"),
                            ("KM", "Comoros"),
                            ("CG", "Congo"),
                            ("CD", "Congo, The Democratic Republic of the"),
                            ("CK", "Cook Islands"),
                            ("CR", "Costa Rica"),
                            ("CI", "Cote d'Ivoire"),
                            ("HR", "Croatia"),
                            ("CU", "Cuba"),
                            ("CY", "Cyprus"),
                            ("CZ", "Czech Republic"),
                            ("DK", "Denmark"),
                            ("DJ", "Djibouti"),
                            ("DM", "Dominica"),
                            ("DO", "Dominican Republic"),
                            ("EC", "Ecuador"),
                            ("EG", "Egypt"),
                            ("SV", "El Salvador"),
                            ("GQ", "Equatorial Guinea"),
                            ("ER", "Eritrea"),
                            ("EE", "Estonia"),
                            ("ET", "Ethiopia"),
                            ("FK", "Falkland Islands (Malvinas)"),
                            ("FO", "Faroe Islands"),
                            ("FJ", "Fiji"),
                            ("FI", "Finland"),
                            ("FR", "France"),
                            ("GF", "French Guiana"),
                            ("PF", "French Polynesia"),
                            ("TF", "French Southern Territories"),
                            ("GA", "Gabon"),
                            ("GM", "Gambia"),
                            ("GE", "Georgia"),
                            ("DE", "Germany"),
                            ("GH", "Ghana"),
                            ("GI", "Gibraltar"),
                            ("GR", "Greece"),
                            ("GL", "Greenland"),
                            ("GD", "Grenada"),
                            ("GP", "Guadeloupe"),
                            ("GU", "Guam"),
                            ("GT", "Guatemala"),
                            ("GG", "Guernsey"),
                            ("GN", "Guinea"),
                            ("GW", "Guinea-Bissau"),
                            ("GY", "Guyana"),
                            ("HT", "Haiti"),
                            ("HM", "Heard Island and McDonald Islands"),
                            ("VA", "Holy See (Vatican City State)"),
                            ("HN", "Honduras"),
                            ("HK", "Hong Kong"),
                            ("HU", "Hungary"),
                            ("IS", "Iceland"),
                            ("IN", "India"),
                            ("ID", "Indonesia"),
                            ("IR", "Iran, Islamic Republic of"),
                            ("IQ", "Iraq"),
                            ("IE", "Ireland"),
                            ("IM", "Isle of Man"),
                            ("IL", "Israel"),
                            ("IT", "Italy"),
                            ("JM", "Jamaica"),
                            ("JP", "Japan"),
                            ("JE", "Jersey"),
                            ("JO", "Jordan"),
                            ("KZ", "Kazakhstan"),
                            ("KE", "Kenya"),
                            ("KI", "Kiribati"),
                            ("KP", "Korea, Democratic People's Republic of"),
                            ("KR", "Korea, Republic of"),
                            ("KW", "Kuwait"),
                            ("KG", "Kyrgyzstan"),
                            ("LA", "Lao People's Democratic Republic"),
                            ("LV", "Latvia"),
                            ("LB", "Lebanon"),
                            ("LS", "Lesotho"),
                            ("LR", "Liberia"),
                            ("LY", "Libyan Arab Jamahiriya"),
                            ("LI", "Liechtenstein"),
                            ("LT", "Lithuania"),
                            ("LU", "Luxembourg"),
                            ("MO", "Macao"),
                            ("MK", "Macedonia, The Former Yugoslav Republic of"),
                            ("MG", "Madagascar"),
                            ("MW", "Malawi"),
                            ("MY", "Malaysia"),
                            ("MV", "Maldives"),
                            ("ML", "Mali"),
                            ("MT", "Malta"),
                            ("MH", "Marshall Islands"),
                            ("MQ", "Martinique"),
                            ("MR", "Mauritania"),
                            ("MU", "Mauritius"),
                            ("YT", "Mayotte"),
                            ("MX", "Mexico"),
                            ("FM", "Micronesia, Federated States of"),
                            ("MD", "Moldova"),
                            ("MC", "Monaco"),
                            ("MN", "Mongolia"),
                            ("ME", "Montenegro"),
                            ("MS", "Montserrat"),
                            ("MA", "Morocco"),
                            ("MZ", "Mozambique"),
                            ("MM", "Myanmar"),
                            ("NA", "Namibia"),
                            ("NR", "Nauru"),
                            ("NP", "Nepal"),
                            ("NL", "Netherlands"),
                            ("AN", "Netherlands Antilles"),
                            ("NC", "New Caledonia"),
                            ("NZ", "New Zealand"),
                            ("NI", "Nicaragua"),
                            ("NE", "Niger"),
                            ("NG", "Nigeria"),
                            ("NU", "Niue"),
                            ("NF", "Norfolk Island"),
                            ("MP", "Northern Mariana Islands"),
                            ("NO", "Norway"),
                            ("OM", "Oman"),
                            ("PK", "Pakistan"),
                            ("PW", "Palau"),
                            ("PS", "Palestinian Territory, Occupied"),
                            ("PA", "Panama"),
                            ("PG", "Papua New Guinea"),
                            ("PY", "Paraguay"),
                            ("PE", "Peru"),
                            ("PH", "Philippines"),
                            ("PN", "Pitcairn"),
                            ("PL", "Poland"),
                            ("PT", "Portugal"),
                            ("PR", "Puerto Rico"),
                            ("QA", "Qatar"),
                            ("RE", "Reunion"),
                            ("RO", "Romania"),
                            ("RU", "Russian Federation"),
                            ("RW", "Rwanda"),
                            ("BL", "Saint Barthelemy"),
                            ("SH", "Saint Helena"),
                            ("KN", "Saint Kitts and Nevis"),
                            ("LC", "Saint Lucia"),
                            ("MF", "Saint Martin"),
                            ("PM", "Saint Pierre and Miquelon"),
                            ("VC", "Saint Vincent and the Grenadines"),
                            ("WS", "Samoa"),
                            ("SM", "San Marino"),
                            ("ST", "Sao Tome and Principe"),
                            ("SA", "Saudi Arabia"),
                            ("SN", "Senegal"),
                            ("RS", "Serbia"),
                            ("SC", "Seychelles"),
                            ("SL", "Sierra Leone"),
                            ("SG", "Singapore"),
                            ("SK", "Slovakia"),
                            ("SI", "Slovenia"),
                            ("SB", "Solomon Islands"),
                            ("SO", "Somalia"),
                            ("ZA", "South Africa"),
                            ("GS", "South Georgia and the South Sandwich Islands"),
                            ("ES", "Spain"),
                            ("LK", "Sri Lanka"),
                            ("SD", "Sudan"),
                            ("SR", "Suriname"),
                            ("SJ", "Svalbard and Jan Mayen"),
                            ("SZ", "Swaziland"),
                            ("SE", "Sweden"),
                            ("CH", "Switzerland"),
                            ("SY", "Syrian Arab Republic"),
                            ("TW", "Taiwan, Province of China"),
                            ("TJ", "Tajikistan"),
                            ("TZ", "Tanzania, United Republic of"),
                            ("TH", "Thailand"),
                            ("TL", "Timor-Leste"),
                            ("TG", "Togo"),
                            ("TK", "Tokelau"),
                            ("TO", "Tonga"),
                            ("TT", "Trinidad and Tobago"),
                            ("TN", "Tunisia"),
                            ("TR", "Turkey"),
                            ("TM", "Turkmenistan"),
                            ("TC", "Turks and Caicos Islands"),
                            ("TV", "Tuvalu"),
                            ("UG", "Uganda"),
                            ("UA", "Ukraine"),
                            ("AE", "United Arab Emirates"),
                            ("US", "United States"),
                            ("UM", "United States Minor Outlying Islands"),
                            ("UY", "Uruguay"),
                            ("UZ", "Uzbekistan"),
                            ("VU", "Vanuatu"),
                            ("VE", "Venezuela"),
                            ("VN", "Viet Nam"),
                            ("VG", "Virgin Islands, British"),
                            ("VI", "Virgin Islands, U.S."),
                            ("WF", "Wallis and Futuna"),
                            ("EH", "Western Sahara"),
                            ("YE", "Yemen"),
                            ("ZM", "Zambia"),
                            ("ZW", "Zimbabwe"),
                        ],
                        max_length=3,
                        null=True,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_on"],
            },
        ),
    ]
