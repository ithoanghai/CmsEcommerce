# Generated by Django 4.2.6 on 2023-10-17 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creme_core', '0061_alter_currency_options_alter_buttonmenuitem_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='time_zone',
            field=models.CharField(choices=[('America/Maceio', 'America/Maceio'), ('America/Havana', 'America/Havana'), ('Asia/Harbin', 'Asia/Harbin'), ('Europe/Sofia', 'Europe/Sofia'), ('America/Argentina/Rio_Gallegos', 'America/Argentina/Rio_Gallegos'), ('Australia/Adelaide', 'Australia/Adelaide'), ('Asia/Dushanbe', 'Asia/Dushanbe'), ('Etc/GMT+5', 'Etc/GMT+5'), ('America/Santo_Domingo', 'America/Santo_Domingo'), ('Pacific/Pago_Pago', 'Pacific/Pago_Pago'), ('Antarctica/DumontDUrville', 'Antarctica/DumontDUrville'), ('Asia/Kabul', 'Asia/Kabul'), ('EST5EDT', 'EST5EDT'), ('Europe/Kiev', 'Europe/Kiev'), ('Mexico/General', 'Mexico/General'), ('America/Mazatlan', 'America/Mazatlan'), ('America/Ciudad_Juarez', 'America/Ciudad_Juarez'), ('America/Boise', 'America/Boise'), ('Pacific/Pohnpei', 'Pacific/Pohnpei'), ('America/Bahia', 'America/Bahia'), ('America/St_Thomas', 'America/St_Thomas'), ('Africa/Casablanca', 'Africa/Casablanca'), ('America/Anchorage', 'America/Anchorage'), ('America/Boa_Vista', 'America/Boa_Vista'), ('America/Tijuana', 'America/Tijuana'), ('America/Shiprock', 'America/Shiprock'), ('Europe/Ljubljana', 'Europe/Ljubljana'), ('Asia/Makassar', 'Asia/Makassar'), ('America/Antigua', 'America/Antigua'), ('America/Creston', 'America/Creston'), ('Europe/Vaduz', 'Europe/Vaduz'), ('Etc/GMT+6', 'Etc/GMT+6'), ('Asia/Kolkata', 'Asia/Kolkata'), ('Asia/Ashgabat', 'Asia/Ashgabat'), ('Asia/Pontianak', 'Asia/Pontianak'), ('US/Alaska', 'US/Alaska'), ('Europe/Dublin', 'Europe/Dublin'), ('Atlantic/Madeira', 'Atlantic/Madeira'), ('America/Marigot', 'America/Marigot'), ('America/La_Paz', 'America/La_Paz'), ('America/Nome', 'America/Nome'), ('Asia/Istanbul', 'Asia/Istanbul'), ('Africa/Abidjan', 'Africa/Abidjan'), ('Africa/Tripoli', 'Africa/Tripoli'), ('Pacific/Gambier', 'Pacific/Gambier'), ('Asia/Bahrain', 'Asia/Bahrain'), ('Pacific/Guam', 'Pacific/Guam'), ('America/Lima', 'America/Lima'), ('America/Iqaluit', 'America/Iqaluit'), ('Asia/Aqtau', 'Asia/Aqtau'), ('America/Glace_Bay', 'America/Glace_Bay'), ('Asia/Choibalsan', 'Asia/Choibalsan'), ('America/Fort_Nelson', 'America/Fort_Nelson'), ('US/Samoa', 'US/Samoa'), ('America/Sao_Paulo', 'America/Sao_Paulo'), ('America/Santiago', 'America/Santiago'), ('Mexico/BajaNorte', 'Mexico/BajaNorte'), ('America/Argentina/Mendoza', 'America/Argentina/Mendoza'), ('Universal', 'Universal'), ('Australia/Hobart', 'Australia/Hobart'), ('US/Hawaii', 'US/Hawaii'), ('Etc/GMT', 'Etc/GMT'), ('Atlantic/Azores', 'Atlantic/Azores'), ('Asia/Yangon', 'Asia/Yangon'), ('Europe/Oslo', 'Europe/Oslo'), ('Australia/Tasmania', 'Australia/Tasmania'), ('Israel', 'Israel'), ('America/Argentina/Cordoba', 'America/Argentina/Cordoba'), ('Asia/Rangoon', 'Asia/Rangoon'), ('Atlantic/Canary', 'Atlantic/Canary'), ('Africa/Luanda', 'Africa/Luanda'), ('Pacific/Marquesas', 'Pacific/Marquesas'), ('Indian/Cocos', 'Indian/Cocos'), ('Africa/Nouakchott', 'Africa/Nouakchott'), ('Asia/Tel_Aviv', 'Asia/Tel_Aviv'), ('Africa/Monrovia', 'Africa/Monrovia'), ('Europe/Sarajevo', 'Europe/Sarajevo'), ('Etc/Greenwich', 'Etc/Greenwich'), ('Asia/Tomsk', 'Asia/Tomsk'), ('Africa/Maseru', 'Africa/Maseru'), ('EST', 'EST'), ('America/Argentina/San_Juan', 'America/Argentina/San_Juan'), ('Antarctica/South_Pole', 'Antarctica/South_Pole'), ('Pacific/Bougainville', 'Pacific/Bougainville'), ('America/Costa_Rica', 'America/Costa_Rica'), ('MST7MDT', 'MST7MDT'), ('Africa/Mbabane', 'Africa/Mbabane'), ('Antarctica/McMurdo', 'Antarctica/McMurdo'), ('America/Punta_Arenas', 'America/Punta_Arenas'), ('America/Chicago', 'America/Chicago'), ('Kwajalein', 'Kwajalein'), ('America/Fort_Wayne', 'America/Fort_Wayne'), ('Africa/Algiers', 'Africa/Algiers'), ('America/Atka', 'America/Atka'), ('America/Halifax', 'America/Halifax'), ('Europe/Madrid', 'Europe/Madrid'), ('Africa/Kampala', 'Africa/Kampala'), ('Etc/GMT-6', 'Etc/GMT-6'), ('America/Louisville', 'America/Louisville'), ('Europe/Belfast', 'Europe/Belfast'), ('Pacific/Port_Moresby', 'Pacific/Port_Moresby'), ('America/Nipigon', 'America/Nipigon'), ('Asia/Dili', 'Asia/Dili'), ('America/Argentina/La_Rioja', 'America/Argentina/La_Rioja'), ('Asia/Phnom_Penh', 'Asia/Phnom_Penh'), ('America/Detroit', 'America/Detroit'), ('Pacific/Honolulu', 'Pacific/Honolulu'), ('Europe/Minsk', 'Europe/Minsk'), ('Asia/Samarkand', 'Asia/Samarkand'), ('Africa/Freetown', 'Africa/Freetown'), ('Australia/Queensland', 'Australia/Queensland'), ('Asia/Thimbu', 'Asia/Thimbu'), ('Zulu', 'Zulu'), ('Africa/Khartoum', 'Africa/Khartoum'), ('America/Regina', 'America/Regina'), ('Poland', 'Poland'), ('Asia/Hebron', 'Asia/Hebron'), ('Asia/Tokyo', 'Asia/Tokyo'), ('America/Indiana/Vincennes', 'America/Indiana/Vincennes'), ('Asia/Amman', 'Asia/Amman'), ('Indian/Comoro', 'Indian/Comoro'), ('Africa/Bissau', 'Africa/Bissau'), ('America/St_Barthelemy', 'America/St_Barthelemy'), ('Africa/Libreville', 'Africa/Libreville'), ('Australia/Victoria', 'Australia/Victoria'), ('Asia/Gaza', 'Asia/Gaza'), ('Chile/Continental', 'Chile/Continental'), ('Europe/Tallinn', 'Europe/Tallinn'), ('Etc/Universal', 'Etc/Universal'), ('Atlantic/Reykjavik', 'Atlantic/Reykjavik'), ('Pacific/Johnston', 'Pacific/Johnston'), ('Europe/Zurich', 'Europe/Zurich'), ('Factory', 'Factory'), ('Indian/Mauritius', 'Indian/Mauritius'), ('Pacific/Easter', 'Pacific/Easter'), ('America/Rainy_River', 'America/Rainy_River'), ('Asia/Macao', 'Asia/Macao'), ('Asia/Ust-Nera', 'Asia/Ust-Nera'), ('Africa/Dar_es_Salaam', 'Africa/Dar_es_Salaam'), ('Australia/West', 'Australia/West'), ('America/Fortaleza', 'America/Fortaleza'), ('Europe/Budapest', 'Europe/Budapest'), ('Europe/Busingen', 'Europe/Busingen'), ('America/Manaus', 'America/Manaus'), ('America/Argentina/San_Luis', 'America/Argentina/San_Luis'), ('Africa/Mogadishu', 'Africa/Mogadishu'), ('MST', 'MST'), ('America/Porto_Acre', 'America/Porto_Acre'), ('Brazil/West', 'Brazil/West'), ('Europe/Lisbon', 'Europe/Lisbon'), ('Pacific/Fiji', 'Pacific/Fiji'), ('America/Anguilla', 'America/Anguilla'), ('US/Arizona', 'US/Arizona'), ('America/Indiana/Winamac', 'America/Indiana/Winamac'), ('Australia/Lord_Howe', 'Australia/Lord_Howe'), ('Europe/Warsaw', 'Europe/Warsaw'), ('America/Bogota', 'America/Bogota'), ('US/East-Indiana', 'US/East-Indiana'), ('Australia/Sydney', 'Australia/Sydney'), ('Asia/Famagusta', 'Asia/Famagusta'), ('America/Mendoza', 'America/Mendoza'), ('Africa/Djibouti', 'Africa/Djibouti'), ('America/Araguaina', 'America/Araguaina'), ('Pacific/Tahiti', 'Pacific/Tahiti'), ('Etc/UTC', 'Etc/UTC'), ('Asia/Chita', 'Asia/Chita'), ('Europe/Brussels', 'Europe/Brussels'), ('Japan', 'Japan'), ('America/Thunder_Bay', 'America/Thunder_Bay'), ('Europe/Samara', 'Europe/Samara'), ('Asia/Irkutsk', 'Asia/Irkutsk'), ('Canada/Yukon', 'Canada/Yukon'), ('Pacific/Kanton', 'Pacific/Kanton'), ('Pacific/Pitcairn', 'Pacific/Pitcairn'), ('Brazil/DeNoronha', 'Brazil/DeNoronha'), ('Canada/Saskatchewan', 'Canada/Saskatchewan'), ('Asia/Qyzylorda', 'Asia/Qyzylorda'), ('America/Coral_Harbour', 'America/Coral_Harbour'), ('America/Dawson', 'America/Dawson'), ('America/Adak', 'America/Adak'), ('Asia/Ashkhabad', 'Asia/Ashkhabad'), ('Etc/GMT+10', 'Etc/GMT+10'), ('Pacific/Efate', 'Pacific/Efate'), ('Africa/Tunis', 'Africa/Tunis'), ('America/Miquelon', 'America/Miquelon'), ('Pacific/Kosrae', 'Pacific/Kosrae'), ('Indian/Chagos', 'Indian/Chagos'), ('Atlantic/Stanley', 'Atlantic/Stanley'), ('Asia/Pyongyang', 'Asia/Pyongyang'), ('Pacific/Kiritimati', 'Pacific/Kiritimati'), ('Atlantic/Faroe', 'Atlantic/Faroe'), ('America/Indiana/Petersburg', 'America/Indiana/Petersburg'), ('Asia/Karachi', 'Asia/Karachi'), ('Pacific/Auckland', 'Pacific/Auckland'), ('Pacific/Saipan', 'Pacific/Saipan'), ('Indian/Maldives', 'Indian/Maldives'), ('America/Cayenne', 'America/Cayenne'), ('Africa/Bamako', 'Africa/Bamako'), ('Asia/Shanghai', 'Asia/Shanghai'), ('Asia/Qatar', 'Asia/Qatar'), ('EET', 'EET'), ('America/Recife', 'America/Recife'), ('Asia/Oral', 'Asia/Oral'), ('Asia/Riyadh', 'Asia/Riyadh'), ('Atlantic/Bermuda', 'Atlantic/Bermuda'), ('America/Godthab', 'America/Godthab'), ('Australia/LHI', 'Australia/LHI'), ('Atlantic/Faeroe', 'Atlantic/Faeroe'), ('Indian/Kerguelen', 'Indian/Kerguelen'), ('Pacific/Noumea', 'Pacific/Noumea'), ('Indian/Mahe', 'Indian/Mahe'), ('America/Guadeloupe', 'America/Guadeloupe'), ('America/Virgin', 'America/Virgin'), ('HST', 'HST'), ('Asia/Katmandu', 'Asia/Katmandu'), ('Asia/Brunei', 'Asia/Brunei'), ('America/Aruba', 'America/Aruba'), ('Europe/Malta', 'Europe/Malta'), ('Europe/Paris', 'Europe/Paris'), ('Europe/Andorra', 'Europe/Andorra'), ('Chile/EasterIsland', 'Chile/EasterIsland'), ('America/Kentucky/Monticello', 'America/Kentucky/Monticello'), ('America/Denver', 'America/Denver'), ('America/Asuncion', 'America/Asuncion'), ('GMT+0', 'GMT+0'), ('America/Guayaquil', 'America/Guayaquil'), ('Europe/Bucharest', 'Europe/Bucharest'), ('Etc/GMT-12', 'Etc/GMT-12'), ('Etc/GMT-7', 'Etc/GMT-7'), ('Etc/GMT-3', 'Etc/GMT-3'), ('Australia/Brisbane', 'Australia/Brisbane'), ('Asia/Yakutsk', 'Asia/Yakutsk'), ('America/Noronha', 'America/Noronha'), ('Europe/Riga', 'Europe/Riga'), ('Asia/Kamchatka', 'Asia/Kamchatka'), ('Africa/Lubumbashi', 'Africa/Lubumbashi'), ('America/North_Dakota/Center', 'America/North_Dakota/Center'), ('America/Edmonton', 'America/Edmonton'), ('Etc/GMT+4', 'Etc/GMT+4'), ('Etc/GMT+9', 'Etc/GMT+9'), ('America/St_Kitts', 'America/St_Kitts'), ('Asia/Barnaul', 'Asia/Barnaul'), ('Antarctica/Rothera', 'Antarctica/Rothera'), ('Etc/GMT-4', 'Etc/GMT-4'), ('Australia/Canberra', 'Australia/Canberra'), ('Europe/Volgograd', 'Europe/Volgograd'), ('Europe/Vienna', 'Europe/Vienna'), ('Africa/Sao_Tome', 'Africa/Sao_Tome'), ('Etc/GMT+12', 'Etc/GMT+12'), ('America/St_Johns', 'America/St_Johns'), ('Canada/Newfoundland', 'Canada/Newfoundland'), ('America/Argentina/Jujuy', 'America/Argentina/Jujuy'), ('US/Eastern', 'US/Eastern'), ('Europe/Bratislava', 'Europe/Bratislava'), ('Pacific/Yap', 'Pacific/Yap'), ('America/Winnipeg', 'America/Winnipeg'), ('Europe/Amsterdam', 'Europe/Amsterdam'), ('Europe/Helsinki', 'Europe/Helsinki'), ('Antarctica/Macquarie', 'Antarctica/Macquarie'), ('America/Pangnirtung', 'America/Pangnirtung'), ('Australia/Melbourne', 'Australia/Melbourne'), ('Asia/Yekaterinburg', 'Asia/Yekaterinburg'), ('Australia/ACT', 'Australia/ACT'), ('America/Porto_Velho', 'America/Porto_Velho'), ('Africa/Blantyre', 'Africa/Blantyre'), ('America/St_Lucia', 'America/St_Lucia'), ('America/Guatemala', 'America/Guatemala'), ('America/North_Dakota/New_Salem', 'America/North_Dakota/New_Salem'), ('Pacific/Kwajalein', 'Pacific/Kwajalein'), ('Europe/Istanbul', 'Europe/Istanbul'), ('Asia/Jakarta', 'Asia/Jakarta'), ('America/Cordoba', 'America/Cordoba'), ('Asia/Damascus', 'Asia/Damascus'), ('NZ', 'NZ'), ('Australia/Darwin', 'Australia/Darwin'), ('Antarctica/Davis', 'Antarctica/Davis'), ('America/Ojinaga', 'America/Ojinaga'), ('Antarctica/Mawson', 'Antarctica/Mawson'), ('Asia/Taipei', 'Asia/Taipei'), ('Africa/Niamey', 'Africa/Niamey'), ('America/Port-au-Prince', 'America/Port-au-Prince'), ('UTC', 'UTC'), ('America/Rankin_Inlet', 'America/Rankin_Inlet'), ('Asia/Nicosia', 'Asia/Nicosia'), ('CET', 'CET'), ('Australia/North', 'Australia/North'), ('Asia/Tbilisi', 'Asia/Tbilisi'), ('Asia/Chongqing', 'Asia/Chongqing'), ('Asia/Jayapura', 'Asia/Jayapura'), ('Pacific/Wallis', 'Pacific/Wallis'), ('Europe/Uzhgorod', 'Europe/Uzhgorod'), ('Asia/Krasnoyarsk', 'Asia/Krasnoyarsk'), ('America/North_Dakota/Beulah', 'America/North_Dakota/Beulah'), ('Europe/Ulyanovsk', 'Europe/Ulyanovsk'), ('Libya', 'Libya'), ('Indian/Mayotte', 'Indian/Mayotte'), ('Antarctica/Troll', 'Antarctica/Troll'), ('Asia/Kuala_Lumpur', 'Asia/Kuala_Lumpur'), ('Iran', 'Iran'), ('America/Tegucigalpa', 'America/Tegucigalpa'), ('Pacific/Guadalcanal', 'Pacific/Guadalcanal'), ('Africa/Johannesburg', 'Africa/Johannesburg'), ('America/Nuuk', 'America/Nuuk'), ('America/Blanc-Sablon', 'America/Blanc-Sablon'), ('Asia/Muscat', 'Asia/Muscat'), ('Asia/Macau', 'Asia/Macau'), ('Asia/Hovd', 'Asia/Hovd'), ('Asia/Omsk', 'Asia/Omsk'), ('Etc/Zulu', 'Etc/Zulu'), ('Asia/Vladivostok', 'Asia/Vladivostok'), ('America/Bahia_Banderas', 'America/Bahia_Banderas'), ('Europe/Kyiv', 'Europe/Kyiv'), ('Asia/Thimphu', 'Asia/Thimphu'), ('America/Vancouver', 'America/Vancouver'), ('Mexico/BajaSur', 'Mexico/BajaSur'), ('America/Cuiaba', 'America/Cuiaba'), ('Etc/GMT-5', 'Etc/GMT-5'), ('Pacific/Majuro', 'Pacific/Majuro'), ('Africa/Windhoek', 'Africa/Windhoek'), ('Asia/Tehran', 'Asia/Tehran'), ('America/Indiana/Vevay', 'America/Indiana/Vevay'), ('Pacific/Palau', 'Pacific/Palau'), ('Pacific/Niue', 'Pacific/Niue'), ('Etc/GMT+11', 'Etc/GMT+11'), ('Asia/Ulan_Bator', 'Asia/Ulan_Bator'), ('Pacific/Truk', 'Pacific/Truk'), ('America/Matamoros', 'America/Matamoros'), ('Etc/GMT-10', 'Etc/GMT-10'), ('Africa/Lusaka', 'Africa/Lusaka'), ('Etc/GMT+0', 'Etc/GMT+0'), ('America/Thule', 'America/Thule'), ('Africa/Malabo', 'Africa/Malabo'), ('Asia/Kuwait', 'Asia/Kuwait'), ('Europe/Kirov', 'Europe/Kirov'), ('Asia/Tashkent', 'Asia/Tashkent'), ('America/Santarem', 'America/Santarem'), ('America/Indiana/Indianapolis', 'America/Indiana/Indianapolis'), ('Etc/GMT-13', 'Etc/GMT-13'), ('Asia/Ujung_Pandang', 'Asia/Ujung_Pandang'), ('Europe/Luxembourg', 'Europe/Luxembourg'), ('Etc/GMT+3', 'Etc/GMT+3'), ('Europe/Prague', 'Europe/Prague'), ('Asia/Jerusalem', 'Asia/Jerusalem'), ('Australia/Lindeman', 'Australia/Lindeman'), ('Antarctica/Palmer', 'Antarctica/Palmer'), ('America/Lower_Princes', 'America/Lower_Princes'), ('Europe/San_Marino', 'Europe/San_Marino'), ('Africa/Ndjamena', 'Africa/Ndjamena'), ('Indian/Antananarivo', 'Indian/Antananarivo'), ('America/Puerto_Rico', 'America/Puerto_Rico'), ('Africa/Maputo', 'Africa/Maputo'), ('Etc/GMT+8', 'Etc/GMT+8'), ('America/Merida', 'America/Merida'), ('Europe/Guernsey', 'Europe/Guernsey'), ('Africa/Conakry', 'Africa/Conakry'), ('America/Eirunepe', 'America/Eirunepe'), ('Australia/Eucla', 'Australia/Eucla'), ('America/Dominica', 'America/Dominica'), ('America/Swift_Current', 'America/Swift_Current'), ('America/Menominee', 'America/Menominee'), ('Pacific/Samoa', 'Pacific/Samoa'), ('America/Rosario', 'America/Rosario'), ('Atlantic/Jan_Mayen', 'Atlantic/Jan_Mayen'), ('Asia/Aden', 'Asia/Aden'), ('Africa/Ouagadougou', 'Africa/Ouagadougou'), ('Antarctica/Syowa', 'Antarctica/Syowa'), ('Arctic/Longyearbyen', 'Arctic/Longyearbyen'), ('Asia/Singapore', 'Asia/Singapore'), ('NZ-CHAT', 'NZ-CHAT'), ('America/Grenada', 'America/Grenada'), ('America/Ensenada', 'America/Ensenada'), ('Etc/GMT0', 'Etc/GMT0'), ('Europe/Gibraltar', 'Europe/Gibraltar'), ('America/Metlakatla', 'America/Metlakatla'), ('Etc/GMT-0', 'Etc/GMT-0'), ('America/Rio_Branco', 'America/Rio_Branco'), ('Asia/Vientiane', 'Asia/Vientiane'), ('Asia/Dacca', 'Asia/Dacca'), ('UCT', 'UCT'), ('Asia/Ho_Chi_Minh', 'Asia/Ho_Chi_Minh'), ('Asia/Beirut', 'Asia/Beirut'), ('Asia/Magadan', 'Asia/Magadan'), ('Canada/Mountain', 'Canada/Mountain'), ('Canada/Eastern', 'Canada/Eastern'), ('US/Indiana-Starke', 'US/Indiana-Starke'), ('America/Jujuy', 'America/Jujuy'), ('PST8PDT', 'PST8PDT'), ('Turkey', 'Turkey'), ('Europe/Saratov', 'Europe/Saratov'), ('Asia/Dubai', 'Asia/Dubai'), ('America/Montevideo', 'America/Montevideo'), ('GB', 'GB'), ('America/Mexico_City', 'America/Mexico_City'), ('Indian/Christmas', 'Indian/Christmas'), ('America/Santa_Isabel', 'America/Santa_Isabel'), ('America/Dawson_Creek', 'America/Dawson_Creek'), ('Pacific/Rarotonga', 'Pacific/Rarotonga'), ('Cuba', 'Cuba'), ('Etc/GMT-1', 'Etc/GMT-1'), ('Australia/Yancowinna', 'Australia/Yancowinna'), ('US/Michigan', 'US/Michigan'), ('Africa/Addis_Ababa', 'Africa/Addis_Ababa'), ('GMT-0', 'GMT-0'), ('Etc/GMT-8', 'Etc/GMT-8'), ('Africa/Timbuktu', 'Africa/Timbuktu'), ('America/Barbados', 'America/Barbados'), ('Australia/Perth', 'Australia/Perth'), ('CST6CDT', 'CST6CDT'), ('America/Yakutat', 'America/Yakutat'), ('Asia/Sakhalin', 'Asia/Sakhalin'), ('America/Jamaica', 'America/Jamaica'), ('America/Los_Angeles', 'America/Los_Angeles'), ('Europe/Athens', 'Europe/Athens'), ('Navajo', 'Navajo'), ('America/Kentucky/Louisville', 'America/Kentucky/Louisville'), ('Asia/Anadyr', 'Asia/Anadyr'), ('Egypt', 'Egypt'), ('Australia/Currie', 'Australia/Currie'), ('America/Managua', 'America/Managua'), ('America/Indiana/Knox', 'America/Indiana/Knox'), ('Asia/Qostanay', 'Asia/Qostanay'), ('Europe/Vilnius', 'Europe/Vilnius'), ('Asia/Bangkok', 'Asia/Bangkok'), ('Asia/Novosibirsk', 'Asia/Novosibirsk'), ('America/Resolute', 'America/Resolute'), ('America/Chihuahua', 'America/Chihuahua'), ('Asia/Yerevan', 'Asia/Yerevan'), ('America/Yellowknife', 'America/Yellowknife'), ('America/Scoresbysund', 'America/Scoresbysund'), ('Europe/London', 'Europe/London'), ('Europe/Tirane', 'Europe/Tirane'), ('Iceland', 'Iceland'), ('Africa/Juba', 'Africa/Juba'), ('Hongkong', 'Hongkong'), ('Asia/Aqtobe', 'Asia/Aqtobe'), ('Asia/Novokuznetsk', 'Asia/Novokuznetsk'), ('America/Cancun', 'America/Cancun'), ('America/Buenos_Aires', 'America/Buenos_Aires'), ('Europe/Berlin', 'Europe/Berlin'), ('Europe/Nicosia', 'Europe/Nicosia'), ('GB-Eire', 'GB-Eire'), ('Greenwich', 'Greenwich'), ('America/Kralendijk', 'America/Kralendijk'), ('Africa/Kigali', 'Africa/Kigali'), ('Europe/Monaco', 'Europe/Monaco'), ('Asia/Colombo', 'Asia/Colombo'), ('America/Montreal', 'America/Montreal'), ('Asia/Kuching', 'Asia/Kuching'), ('Europe/Rome', 'Europe/Rome'), ('Asia/Bishkek', 'Asia/Bishkek'), ('America/Argentina/Ushuaia', 'America/Argentina/Ushuaia'), ('Europe/Jersey', 'Europe/Jersey'), ('Etc/GMT-14', 'Etc/GMT-14'), ('Africa/Nairobi', 'Africa/Nairobi'), ('America/Goose_Bay', 'America/Goose_Bay'), ('America/St_Vincent', 'America/St_Vincent'), ('America/Whitehorse', 'America/Whitehorse'), ('Atlantic/South_Georgia', 'Atlantic/South_Georgia'), ('GMT0', 'GMT0'), ('Asia/Khandyga', 'Asia/Khandyga'), ('America/Belem', 'America/Belem'), ('America/Juneau', 'America/Juneau'), ('Pacific/Chuuk', 'Pacific/Chuuk'), ('Asia/Baghdad', 'Asia/Baghdad'), ('Europe/Vatican', 'Europe/Vatican'), ('MET', 'MET'), ('Etc/GMT-2', 'Etc/GMT-2'), ('America/Argentina/Tucuman', 'America/Argentina/Tucuman'), ('Europe/Moscow', 'Europe/Moscow'), ('Africa/Douala', 'Africa/Douala'), ('Africa/Harare', 'Africa/Harare'), ('America/Caracas', 'America/Caracas'), ('Etc/GMT-9', 'Etc/GMT-9'), ('WET', 'WET'), ('America/Hermosillo', 'America/Hermosillo'), ('America/Catamarca', 'America/Catamarca'), ('Pacific/Funafuti', 'Pacific/Funafuti'), ('Pacific/Nauru', 'Pacific/Nauru'), ('America/Paramaribo', 'America/Paramaribo'), ('Asia/Calcutta', 'Asia/Calcutta'), ('Asia/Dhaka', 'Asia/Dhaka'), ('W-SU', 'W-SU'), ('America/Inuvik', 'America/Inuvik'), ('Asia/Srednekolymsk', 'Asia/Srednekolymsk'), ('America/Campo_Grande', 'America/Campo_Grande'), ('America/Martinique', 'America/Martinique'), ('Australia/South', 'Australia/South'), ('Europe/Astrakhan', 'Europe/Astrakhan'), ('US/Mountain', 'US/Mountain'), ('Africa/Brazzaville', 'Africa/Brazzaville'), ('Asia/Kathmandu', 'Asia/Kathmandu'), ('America/Danmarkshavn', 'America/Danmarkshavn'), ('Australia/NSW', 'Australia/NSW'), ('Africa/Gaborone', 'Africa/Gaborone'), ('Europe/Isle_of_Man', 'Europe/Isle_of_Man'), ('Europe/Zaporozhye', 'Europe/Zaporozhye'), ('America/Belize', 'America/Belize'), ('Etc/UCT', 'Etc/UCT'), ('Europe/Skopje', 'Europe/Skopje'), ('Asia/Manila', 'Asia/Manila'), ('Pacific/Wake', 'Pacific/Wake'), ('America/Cambridge_Bay', 'America/Cambridge_Bay'), ('Portugal', 'Portugal'), ('America/El_Salvador', 'America/El_Salvador'), ('Pacific/Chatham', 'Pacific/Chatham'), ('Asia/Chungking', 'Asia/Chungking'), ('Asia/Urumqi', 'Asia/Urumqi'), ('Pacific/Fakaofo', 'Pacific/Fakaofo'), ('Pacific/Galapagos', 'Pacific/Galapagos'), ('Africa/Cairo', 'Africa/Cairo'), ('Canada/Atlantic', 'Canada/Atlantic'), ('Europe/Simferopol', 'Europe/Simferopol'), ('Africa/Lagos', 'Africa/Lagos'), ('Asia/Almaty', 'Asia/Almaty'), ('Africa/Dakar', 'Africa/Dakar'), ('Brazil/Acre', 'Brazil/Acre'), ('ROK', 'ROK'), ('America/Atikokan', 'America/Atikokan'), ('America/Moncton', 'America/Moncton'), ('Africa/El_Aaiun', 'Africa/El_Aaiun'), ('Etc/GMT+7', 'Etc/GMT+7'), ('America/Argentina/ComodRivadavia', 'America/Argentina/ComodRivadavia'), ('Europe/Podgorica', 'Europe/Podgorica'), ('America/Indiana/Marengo', 'America/Indiana/Marengo'), ('America/Argentina/Salta', 'America/Argentina/Salta'), ('America/New_York', 'America/New_York'), ('Pacific/Ponape', 'Pacific/Ponape'), ('Europe/Chisinau', 'Europe/Chisinau'), ('America/Knox_IN', 'America/Knox_IN'), ('Singapore', 'Singapore'), ('Etc/GMT-11', 'Etc/GMT-11'), ('Pacific/Tarawa', 'Pacific/Tarawa'), ('Jamaica', 'Jamaica'), ('Asia/Ulaanbaatar', 'Asia/Ulaanbaatar'), ('Atlantic/St_Helena', 'Atlantic/St_Helena'), ('America/Indiana/Tell_City', 'America/Indiana/Tell_City'), ('US/Pacific', 'US/Pacific'), ('Africa/Banjul', 'Africa/Banjul'), ('Eire', 'Eire'), ('Etc/GMT+2', 'Etc/GMT+2'), ('America/Nassau', 'America/Nassau'), ('America/Guyana', 'America/Guyana'), ('Europe/Kaliningrad', 'Europe/Kaliningrad'), ('Africa/Asmera', 'Africa/Asmera'), ('Pacific/Midway', 'Pacific/Midway'), ('Europe/Stockholm', 'Europe/Stockholm'), ('US/Aleutian', 'US/Aleutian'), ('Europe/Mariehamn', 'Europe/Mariehamn'), ('Antarctica/Casey', 'Antarctica/Casey'), ('America/Montserrat', 'America/Montserrat'), ('America/Panama', 'America/Panama'), ('America/Indianapolis', 'America/Indianapolis'), ('Asia/Hong_Kong', 'Asia/Hong_Kong'), ('Europe/Copenhagen', 'Europe/Copenhagen'), ('Atlantic/Cape_Verde', 'Atlantic/Cape_Verde'), ('Africa/Bujumbura', 'Africa/Bujumbura'), ('America/Argentina/Buenos_Aires', 'America/Argentina/Buenos_Aires'), ('Africa/Accra', 'Africa/Accra'), ('Etc/GMT+1', 'Etc/GMT+1'), ('Antarctica/Vostok', 'Antarctica/Vostok'), ('America/Monterrey', 'America/Monterrey'), ('America/Cayman', 'America/Cayman'), ('Indian/Reunion', 'Indian/Reunion'), ('ROC', 'ROC'), ('Brazil/East', 'Brazil/East'), ('America/Tortola', 'America/Tortola'), ('Africa/Asmara', 'Africa/Asmara'), ('Pacific/Enderbury', 'Pacific/Enderbury'), ('America/Port_of_Spain', 'America/Port_of_Spain'), ('America/Sitka', 'America/Sitka'), ('GMT', 'GMT'), ('Africa/Porto-Novo', 'Africa/Porto-Novo'), ('Africa/Ceuta', 'Africa/Ceuta'), ('Asia/Baku', 'Asia/Baku'), ('Africa/Kinshasa', 'Africa/Kinshasa'), ('PRC', 'PRC'), ('Canada/Central', 'Canada/Central'), ('Asia/Saigon', 'Asia/Saigon'), ('America/Phoenix', 'America/Phoenix'), ('Asia/Kashgar', 'Asia/Kashgar'), ('Europe/Zagreb', 'Europe/Zagreb'), ('America/Toronto', 'America/Toronto'), ('Asia/Seoul', 'Asia/Seoul'), ('Europe/Tiraspol', 'Europe/Tiraspol'), ('Australia/Broken_Hill', 'Australia/Broken_Hill'), ('Pacific/Tongatapu', 'Pacific/Tongatapu'), ('Canada/Pacific', 'Canada/Pacific'), ('US/Central', 'US/Central'), ('Europe/Belgrade', 'Europe/Belgrade'), ('Asia/Atyrau', 'Asia/Atyrau'), ('Pacific/Norfolk', 'Pacific/Norfolk'), ('Pacific/Apia', 'Pacific/Apia'), ('America/Grand_Turk', 'America/Grand_Turk'), ('America/Argentina/Catamarca', 'America/Argentina/Catamarca'), ('Africa/Bangui', 'Africa/Bangui'), ('America/Curacao', 'America/Curacao'), ('Africa/Lome', 'Africa/Lome')], default='Asia/Kolkata', max_length=50, verbose_name='Time zone'),
        ),
    ]
