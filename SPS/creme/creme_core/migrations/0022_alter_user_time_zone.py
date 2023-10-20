# Generated by Django 4.2.6 on 2023-10-17 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creme_core', '0021_alter_user_time_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='time_zone',
            field=models.CharField(choices=[('Pacific/Guam', 'Pacific/Guam'), ('America/Santa_Isabel', 'America/Santa_Isabel'), ('Europe/Busingen', 'Europe/Busingen'), ('Asia/Dhaka', 'Asia/Dhaka'), ('Europe/Amsterdam', 'Europe/Amsterdam'), ('America/Argentina/Ushuaia', 'America/Argentina/Ushuaia'), ('NZ', 'NZ'), ('Australia/Darwin', 'Australia/Darwin'), ('Africa/Lubumbashi', 'Africa/Lubumbashi'), ('Africa/Niamey', 'Africa/Niamey'), ('America/Denver', 'America/Denver'), ('Africa/Bangui', 'Africa/Bangui'), ('Etc/Zulu', 'Etc/Zulu'), ('Pacific/Pago_Pago', 'Pacific/Pago_Pago'), ('America/Montevideo', 'America/Montevideo'), ('America/Bahia_Banderas', 'America/Bahia_Banderas'), ('Indian/Reunion', 'Indian/Reunion'), ('Brazil/DeNoronha', 'Brazil/DeNoronha'), ('US/Hawaii', 'US/Hawaii'), ('Brazil/West', 'Brazil/West'), ('Asia/Anadyr', 'Asia/Anadyr'), ('Pacific/Marquesas', 'Pacific/Marquesas'), ('America/Nipigon', 'America/Nipigon'), ('Australia/South', 'Australia/South'), ('US/Central', 'US/Central'), ('America/Argentina/Cordoba', 'America/Argentina/Cordoba'), ('America/Toronto', 'America/Toronto'), ('Europe/Budapest', 'Europe/Budapest'), ('Zulu', 'Zulu'), ('Australia/Victoria', 'Australia/Victoria'), ('America/Curacao', 'America/Curacao'), ('America/Porto_Velho', 'America/Porto_Velho'), ('America/Buenos_Aires', 'America/Buenos_Aires'), ('Indian/Mayotte', 'Indian/Mayotte'), ('Pacific/Norfolk', 'Pacific/Norfolk'), ('Asia/Baku', 'Asia/Baku'), ('Europe/Helsinki', 'Europe/Helsinki'), ('Pacific/Wallis', 'Pacific/Wallis'), ('America/Rainy_River', 'America/Rainy_River'), ('Asia/Samarkand', 'Asia/Samarkand'), ('Asia/Ho_Chi_Minh', 'Asia/Ho_Chi_Minh'), ('America/Kralendijk', 'America/Kralendijk'), ('Asia/Thimbu', 'Asia/Thimbu'), ('America/Moncton', 'America/Moncton'), ('CST6CDT', 'CST6CDT'), ('Etc/GMT-4', 'Etc/GMT-4'), ('Pacific/Johnston', 'Pacific/Johnston'), ('America/Coral_Harbour', 'America/Coral_Harbour'), ('Australia/Currie', 'Australia/Currie'), ('Turkey', 'Turkey'), ('Asia/Tehran', 'Asia/Tehran'), ('Etc/Greenwich', 'Etc/Greenwich'), ('America/Indiana/Vincennes', 'America/Indiana/Vincennes'), ('WET', 'WET'), ('Atlantic/Bermuda', 'Atlantic/Bermuda'), ('Etc/GMT+8', 'Etc/GMT+8'), ('US/Michigan', 'US/Michigan'), ('Australia/Lord_Howe', 'Australia/Lord_Howe'), ('Africa/Djibouti', 'Africa/Djibouti'), ('Etc/GMT-3', 'Etc/GMT-3'), ('Brazil/Acre', 'Brazil/Acre'), ('PST8PDT', 'PST8PDT'), ('Australia/West', 'Australia/West'), ('America/Fortaleza', 'America/Fortaleza'), ('America/St_Barthelemy', 'America/St_Barthelemy'), ('Europe/Ljubljana', 'Europe/Ljubljana'), ('Pacific/Port_Moresby', 'Pacific/Port_Moresby'), ('Asia/Beirut', 'Asia/Beirut'), ('America/Cambridge_Bay', 'America/Cambridge_Bay'), ('Australia/Queensland', 'Australia/Queensland'), ('Etc/GMT+11', 'Etc/GMT+11'), ('America/Atikokan', 'America/Atikokan'), ('America/Martinique', 'America/Martinique'), ('Europe/Malta', 'Europe/Malta'), ('Pacific/Samoa', 'Pacific/Samoa'), ('Asia/Kabul', 'Asia/Kabul'), ('Asia/Pontianak', 'Asia/Pontianak'), ('America/Panama', 'America/Panama'), ('Asia/Dacca', 'Asia/Dacca'), ('America/Grenada', 'America/Grenada'), ('America/Jujuy', 'America/Jujuy'), ('Antarctica/Vostok', 'Antarctica/Vostok'), ('Australia/Eucla', 'Australia/Eucla'), ('Europe/Vatican', 'Europe/Vatican'), ('Africa/Gaborone', 'Africa/Gaborone'), ('Asia/Makassar', 'Asia/Makassar'), ('Etc/Universal', 'Etc/Universal'), ('Singapore', 'Singapore'), ('Europe/Belfast', 'Europe/Belfast'), ('Antarctica/McMurdo', 'Antarctica/McMurdo'), ('Pacific/Gambier', 'Pacific/Gambier'), ('America/Sitka', 'America/Sitka'), ('America/Catamarca', 'America/Catamarca'), ('America/Kentucky/Louisville', 'America/Kentucky/Louisville'), ('Europe/Paris', 'Europe/Paris'), ('Europe/Athens', 'Europe/Athens'), ('America/Araguaina', 'America/Araguaina'), ('Asia/Katmandu', 'Asia/Katmandu'), ('America/Argentina/San_Luis', 'America/Argentina/San_Luis'), ('Australia/LHI', 'Australia/LHI'), ('Asia/Chita', 'Asia/Chita'), ('America/Guayaquil', 'America/Guayaquil'), ('Asia/Krasnoyarsk', 'Asia/Krasnoyarsk'), ('Europe/Isle_of_Man', 'Europe/Isle_of_Man'), ('Asia/Ulan_Bator', 'Asia/Ulan_Bator'), ('Europe/Bucharest', 'Europe/Bucharest'), ('Asia/Bangkok', 'Asia/Bangkok'), ('Atlantic/Reykjavik', 'Atlantic/Reykjavik'), ('America/Santarem', 'America/Santarem'), ('Europe/Lisbon', 'Europe/Lisbon'), ('America/Scoresbysund', 'America/Scoresbysund'), ('Africa/Libreville', 'Africa/Libreville'), ('Antarctica/Palmer', 'Antarctica/Palmer'), ('Europe/Berlin', 'Europe/Berlin'), ('Asia/Srednekolymsk', 'Asia/Srednekolymsk'), ('EST5EDT', 'EST5EDT'), ('America/El_Salvador', 'America/El_Salvador'), ('Asia/Rangoon', 'Asia/Rangoon'), ('Greenwich', 'Greenwich'), ('America/Noronha', 'America/Noronha'), ('Atlantic/St_Helena', 'Atlantic/St_Helena'), ('Arctic/Longyearbyen', 'Arctic/Longyearbyen'), ('America/Winnipeg', 'America/Winnipeg'), ('Africa/Algiers', 'Africa/Algiers'), ('Europe/Chisinau', 'Europe/Chisinau'), ('Etc/GMT+9', 'Etc/GMT+9'), ('Africa/Kigali', 'Africa/Kigali'), ('Pacific/Palau', 'Pacific/Palau'), ('Asia/Hovd', 'Asia/Hovd'), ('America/Blanc-Sablon', 'America/Blanc-Sablon'), ('America/Argentina/Rio_Gallegos', 'America/Argentina/Rio_Gallegos'), ('Europe/Kyiv', 'Europe/Kyiv'), ('America/Maceio', 'America/Maceio'), ('Africa/Monrovia', 'Africa/Monrovia'), ('Africa/Bujumbura', 'Africa/Bujumbura'), ('Africa/Khartoum', 'Africa/Khartoum'), ('Asia/Magadan', 'Asia/Magadan'), ('Etc/GMT+10', 'Etc/GMT+10'), ('Asia/Famagusta', 'Asia/Famagusta'), ('Antarctica/Rothera', 'Antarctica/Rothera'), ('Africa/Casablanca', 'Africa/Casablanca'), ('Indian/Maldives', 'Indian/Maldives'), ('Europe/Ulyanovsk', 'Europe/Ulyanovsk'), ('Africa/Bissau', 'Africa/Bissau'), ('Asia/Aqtau', 'Asia/Aqtau'), ('Asia/Pyongyang', 'Asia/Pyongyang'), ('America/Juneau', 'America/Juneau'), ('Asia/Urumqi', 'Asia/Urumqi'), ('Asia/Khandyga', 'Asia/Khandyga'), ('America/Punta_Arenas', 'America/Punta_Arenas'), ('Chile/EasterIsland', 'Chile/EasterIsland'), ('Pacific/Niue', 'Pacific/Niue'), ('MST', 'MST'), ('Asia/Jerusalem', 'Asia/Jerusalem'), ('America/Nome', 'America/Nome'), ('America/Argentina/Tucuman', 'America/Argentina/Tucuman'), ('Pacific/Bougainville', 'Pacific/Bougainville'), ('Egypt', 'Egypt'), ('Europe/Tiraspol', 'Europe/Tiraspol'), ('America/North_Dakota/Beulah', 'America/North_Dakota/Beulah'), ('Africa/Sao_Tome', 'Africa/Sao_Tome'), ('America/Montserrat', 'America/Montserrat'), ('US/Mountain', 'US/Mountain'), ('Africa/Cairo', 'Africa/Cairo'), ('Asia/Thimphu', 'Asia/Thimphu'), ('America/Indiana/Petersburg', 'America/Indiana/Petersburg'), ('Antarctica/Casey', 'Antarctica/Casey'), ('Europe/London', 'Europe/London'), ('America/Sao_Paulo', 'America/Sao_Paulo'), ('Pacific/Funafuti', 'Pacific/Funafuti'), ('America/Tortola', 'America/Tortola'), ('Etc/GMT-1', 'Etc/GMT-1'), ('Australia/Tasmania', 'Australia/Tasmania'), ('America/St_Thomas', 'America/St_Thomas'), ('America/Indiana/Tell_City', 'America/Indiana/Tell_City'), ('America/Hermosillo', 'America/Hermosillo'), ('Europe/Zurich', 'Europe/Zurich'), ('Africa/Lagos', 'Africa/Lagos'), ('Africa/Douala', 'Africa/Douala'), ('America/Edmonton', 'America/Edmonton'), ('America/Havana', 'America/Havana'), ('America/Mexico_City', 'America/Mexico_City'), ('Europe/Warsaw', 'Europe/Warsaw'), ('Asia/Macau', 'Asia/Macau'), ('America/Matamoros', 'America/Matamoros'), ('Asia/Yangon', 'Asia/Yangon'), ('Pacific/Kwajalein', 'Pacific/Kwajalein'), ('Europe/Gibraltar', 'Europe/Gibraltar'), ('Europe/Podgorica', 'Europe/Podgorica'), ('Europe/Dublin', 'Europe/Dublin'), ('Europe/Prague', 'Europe/Prague'), ('America/Boise', 'America/Boise'), ('Africa/Abidjan', 'Africa/Abidjan'), ('America/Thule', 'America/Thule'), ('America/Anchorage', 'America/Anchorage'), ('America/Lower_Princes', 'America/Lower_Princes'), ('America/Dawson_Creek', 'America/Dawson_Creek'), ('Australia/Yancowinna', 'Australia/Yancowinna'), ('America/Argentina/Jujuy', 'America/Argentina/Jujuy'), ('GB-Eire', 'GB-Eire'), ('Africa/Johannesburg', 'Africa/Johannesburg'), ('America/Argentina/Salta', 'America/Argentina/Salta'), ('Asia/Jakarta', 'Asia/Jakarta'), ('Pacific/Fakaofo', 'Pacific/Fakaofo'), ('Europe/Istanbul', 'Europe/Istanbul'), ('Asia/Yakutsk', 'Asia/Yakutsk'), ('Canada/Newfoundland', 'Canada/Newfoundland'), ('Antarctica/Macquarie', 'Antarctica/Macquarie'), ('Mexico/General', 'Mexico/General'), ('America/Detroit', 'America/Detroit'), ('America/Goose_Bay', 'America/Goose_Bay'), ('Cuba', 'Cuba'), ('Africa/Harare', 'Africa/Harare'), ('America/Swift_Current', 'America/Swift_Current'), ('America/Monterrey', 'America/Monterrey'), ('America/Pangnirtung', 'America/Pangnirtung'), ('America/Cayman', 'America/Cayman'), ('Atlantic/Faeroe', 'Atlantic/Faeroe'), ('Africa/Ndjamena', 'Africa/Ndjamena'), ('Canada/Eastern', 'Canada/Eastern'), ('Antarctica/Davis', 'Antarctica/Davis'), ('Europe/Vienna', 'Europe/Vienna'), ('Pacific/Wake', 'Pacific/Wake'), ('America/Rankin_Inlet', 'America/Rankin_Inlet'), ('America/Argentina/Buenos_Aires', 'America/Argentina/Buenos_Aires'), ('Africa/Kinshasa', 'Africa/Kinshasa'), ('America/Thunder_Bay', 'America/Thunder_Bay'), ('GB', 'GB'), ('Europe/Zagreb', 'Europe/Zagreb'), ('America/Cancun', 'America/Cancun'), ('Asia/Jayapura', 'Asia/Jayapura'), ('America/Paramaribo', 'America/Paramaribo'), ('Africa/Malabo', 'Africa/Malabo'), ('Europe/Astrakhan', 'Europe/Astrakhan'), ('Asia/Gaza', 'Asia/Gaza'), ('Etc/GMT+4', 'Etc/GMT+4'), ('America/Jamaica', 'America/Jamaica'), ('Etc/GMT+5', 'Etc/GMT+5'), ('Atlantic/Azores', 'Atlantic/Azores'), ('America/Rosario', 'America/Rosario'), ('America/Montreal', 'America/Montreal'), ('Pacific/Truk', 'Pacific/Truk'), ('America/Santo_Domingo', 'America/Santo_Domingo'), ('America/Adak', 'America/Adak'), ('ROK', 'ROK'), ('US/Pacific', 'US/Pacific'), ('Asia/Hebron', 'Asia/Hebron'), ('America/Tijuana', 'America/Tijuana'), ('America/Los_Angeles', 'America/Los_Angeles'), ('Navajo', 'Navajo'), ('Africa/Conakry', 'Africa/Conakry'), ('Africa/Addis_Ababa', 'Africa/Addis_Ababa'), ('Brazil/East', 'Brazil/East'), ('Atlantic/Canary', 'Atlantic/Canary'), ('EST', 'EST'), ('Europe/Bratislava', 'Europe/Bratislava'), ('America/Aruba', 'America/Aruba'), ('Pacific/Saipan', 'Pacific/Saipan'), ('Asia/Dubai', 'Asia/Dubai'), ('Europe/Guernsey', 'Europe/Guernsey'), ('Australia/Lindeman', 'Australia/Lindeman'), ('Mexico/BajaSur', 'Mexico/BajaSur'), ('America/Menominee', 'America/Menominee'), ('America/Ojinaga', 'America/Ojinaga'), ('America/Virgin', 'America/Virgin'), ('Asia/Calcutta', 'Asia/Calcutta'), ('Pacific/Pitcairn', 'Pacific/Pitcairn'), ('Asia/Phnom_Penh', 'Asia/Phnom_Penh'), ('America/Shiprock', 'America/Shiprock'), ('US/Aleutian', 'US/Aleutian'), ('Africa/Lusaka', 'Africa/Lusaka'), ('Europe/Kiev', 'Europe/Kiev'), ('America/Dawson', 'America/Dawson'), ('Etc/UTC', 'Etc/UTC'), ('Indian/Comoro', 'Indian/Comoro'), ('Mexico/BajaNorte', 'Mexico/BajaNorte'), ('Etc/UCT', 'Etc/UCT'), ('Asia/Ashkhabad', 'Asia/Ashkhabad'), ('America/Cayenne', 'America/Cayenne'), ('Asia/Ust-Nera', 'Asia/Ust-Nera'), ('Pacific/Galapagos', 'Pacific/Galapagos'), ('Europe/Mariehamn', 'Europe/Mariehamn'), ('Etc/GMT+0', 'Etc/GMT+0'), ('Hongkong', 'Hongkong'), ('America/North_Dakota/New_Salem', 'America/North_Dakota/New_Salem'), ('Atlantic/South_Georgia', 'Atlantic/South_Georgia'), ('America/Bahia', 'America/Bahia'), ('Africa/Freetown', 'Africa/Freetown'), ('Portugal', 'Portugal'), ('Jamaica', 'Jamaica'), ('W-SU', 'W-SU'), ('Antarctica/DumontDUrville', 'Antarctica/DumontDUrville'), ('US/Eastern', 'US/Eastern'), ('Europe/Luxembourg', 'Europe/Luxembourg'), ('Asia/Saigon', 'Asia/Saigon'), ('Asia/Kuching', 'Asia/Kuching'), ('Etc/GMT-14', 'Etc/GMT-14'), ('Indian/Antananarivo', 'Indian/Antananarivo'), ('Africa/Ceuta', 'Africa/Ceuta'), ('America/Phoenix', 'America/Phoenix'), ('America/Fort_Nelson', 'America/Fort_Nelson'), ('America/Cuiaba', 'America/Cuiaba'), ('Indian/Christmas', 'Indian/Christmas'), ('Asia/Shanghai', 'Asia/Shanghai'), ('Factory', 'Factory'), ('Asia/Bishkek', 'Asia/Bishkek'), ('Asia/Seoul', 'Asia/Seoul'), ('Asia/Ulaanbaatar', 'Asia/Ulaanbaatar'), ('Australia/Melbourne', 'Australia/Melbourne'), ('Pacific/Easter', 'Pacific/Easter'), ('America/Guyana', 'America/Guyana'), ('Etc/GMT', 'Etc/GMT'), ('Africa/El_Aaiun', 'Africa/El_Aaiun'), ('Etc/GMT-13', 'Etc/GMT-13'), ('Etc/GMT+2', 'Etc/GMT+2'), ('Asia/Atyrau', 'Asia/Atyrau'), ('America/Metlakatla', 'America/Metlakatla'), ('Eire', 'Eire'), ('UCT', 'UCT'), ('America/Dominica', 'America/Dominica'), ('America/Anguilla', 'America/Anguilla'), ('Israel', 'Israel'), ('America/Antigua', 'America/Antigua'), ('Africa/Maseru', 'Africa/Maseru'), ('Asia/Baghdad', 'Asia/Baghdad'), ('Etc/GMT-2', 'Etc/GMT-2'), ('America/Ensenada', 'America/Ensenada'), ('Pacific/Rarotonga', 'Pacific/Rarotonga'), ('Asia/Chongqing', 'Asia/Chongqing'), ('Europe/Copenhagen', 'Europe/Copenhagen'), ('Asia/Oral', 'Asia/Oral'), ('America/Vancouver', 'America/Vancouver'), ('America/Resolute', 'America/Resolute'), ('Asia/Omsk', 'Asia/Omsk'), ('Europe/Rome', 'Europe/Rome'), ('Australia/North', 'Australia/North'), ('America/Campo_Grande', 'America/Campo_Grande'), ('Africa/Bamako', 'Africa/Bamako'), ('GMT0', 'GMT0'), ('Asia/Hong_Kong', 'Asia/Hong_Kong'), ('America/Regina', 'America/Regina'), ('Pacific/Enderbury', 'Pacific/Enderbury'), ('Africa/Luanda', 'Africa/Luanda'), ('America/Fort_Wayne', 'America/Fort_Wayne'), ('Europe/Saratov', 'Europe/Saratov'), ('MET', 'MET'), ('US/Arizona', 'US/Arizona'), ('Africa/Asmara', 'Africa/Asmara'), ('Etc/GMT-9', 'Etc/GMT-9'), ('Asia/Dili', 'Asia/Dili'), ('Pacific/Chatham', 'Pacific/Chatham'), ('Etc/GMT-0', 'Etc/GMT-0'), ('America/Indiana/Knox', 'America/Indiana/Knox'), ('Asia/Kuala_Lumpur', 'Asia/Kuala_Lumpur'), ('Etc/GMT-8', 'Etc/GMT-8'), ('US/Indiana-Starke', 'US/Indiana-Starke'), ('Africa/Timbuktu', 'Africa/Timbuktu'), ('America/Ciudad_Juarez', 'America/Ciudad_Juarez'), ('ROC', 'ROC'), ('America/Knox_IN', 'America/Knox_IN'), ('America/St_Johns', 'America/St_Johns'), ('America/Nassau', 'America/Nassau'), ('America/Mazatlan', 'America/Mazatlan'), ('Asia/Yekaterinburg', 'Asia/Yekaterinburg'), ('Europe/Minsk', 'Europe/Minsk'), ('Europe/Samara', 'Europe/Samara'), ('Asia/Nicosia', 'Asia/Nicosia'), ('America/Chicago', 'America/Chicago'), ('Europe/Stockholm', 'Europe/Stockholm'), ('Indian/Cocos', 'Indian/Cocos'), ('Asia/Ujung_Pandang', 'Asia/Ujung_Pandang'), ('Pacific/Tongatapu', 'Pacific/Tongatapu'), ('America/Danmarkshavn', 'America/Danmarkshavn'), ('America/Creston', 'America/Creston'), ('Etc/GMT+3', 'Etc/GMT+3'), ('Europe/Kaliningrad', 'Europe/Kaliningrad'), ('UTC', 'UTC'), ('America/Cordoba', 'America/Cordoba'), ('Asia/Riyadh', 'Asia/Riyadh'), ('Indian/Mahe', 'Indian/Mahe'), ('Australia/Adelaide', 'Australia/Adelaide'), ('Indian/Chagos', 'Indian/Chagos'), ('Canada/Pacific', 'Canada/Pacific'), ('Africa/Nouakchott', 'Africa/Nouakchott'), ('Etc/GMT-12', 'Etc/GMT-12'), ('Etc/GMT+1', 'Etc/GMT+1'), ('America/Kentucky/Monticello', 'America/Kentucky/Monticello'), ('Asia/Ashgabat', 'Asia/Ashgabat'), ('Pacific/Pohnpei', 'Pacific/Pohnpei'), ('Asia/Manila', 'Asia/Manila'), ('Atlantic/Madeira', 'Atlantic/Madeira'), ('America/Puerto_Rico', 'America/Puerto_Rico'), ('Canada/Atlantic', 'Canada/Atlantic'), ('Europe/Tallinn', 'Europe/Tallinn'), ('Etc/GMT-10', 'Etc/GMT-10'), ('America/Iqaluit', 'America/Iqaluit'), ('Africa/Dakar', 'Africa/Dakar'), ('Asia/Barnaul', 'Asia/Barnaul'), ('HST', 'HST'), ('America/Atka', 'America/Atka'), ('Africa/Ouagadougou', 'Africa/Ouagadougou'), ('GMT', 'GMT'), ('America/Indiana/Winamac', 'America/Indiana/Winamac'), ('GMT-0', 'GMT-0'), ('Pacific/Majuro', 'Pacific/Majuro'), ('America/Chihuahua', 'America/Chihuahua'), ('Libya', 'Libya'), ('Asia/Kuwait', 'Asia/Kuwait'), ('Pacific/Ponape', 'Pacific/Ponape'), ('America/Tegucigalpa', 'America/Tegucigalpa'), ('Atlantic/Faroe', 'Atlantic/Faroe'), ('America/Indiana/Indianapolis', 'America/Indiana/Indianapolis'), ('America/Miquelon', 'America/Miquelon'), ('Africa/Maputo', 'Africa/Maputo'), ('America/Boa_Vista', 'America/Boa_Vista'), ('Asia/Muscat', 'Asia/Muscat'), ('America/Indiana/Marengo', 'America/Indiana/Marengo'), ('US/East-Indiana', 'US/East-Indiana'), ('America/Santiago', 'America/Santiago'), ('Kwajalein', 'Kwajalein'), ('America/Grand_Turk', 'America/Grand_Turk'), ('Africa/Windhoek', 'Africa/Windhoek'), ('America/Argentina/ComodRivadavia', 'America/Argentina/ComodRivadavia'), ('Asia/Irkutsk', 'Asia/Irkutsk'), ('MST7MDT', 'MST7MDT'), ('Asia/Singapore', 'Asia/Singapore'), ('Etc/GMT-5', 'Etc/GMT-5'), ('Europe/Monaco', 'Europe/Monaco'), ('Asia/Tokyo', 'Asia/Tokyo'), ('Asia/Amman', 'Asia/Amman'), ('America/Manaus', 'America/Manaus'), ('Europe/Sarajevo', 'Europe/Sarajevo'), ('America/St_Kitts', 'America/St_Kitts'), ('Europe/Vilnius', 'Europe/Vilnius'), ('US/Alaska', 'US/Alaska'), ('Pacific/Kanton', 'Pacific/Kanton'), ('America/Yakutat', 'America/Yakutat'), ('Asia/Aqtobe', 'Asia/Aqtobe'), ('Africa/Lome', 'Africa/Lome'), ('Africa/Accra', 'Africa/Accra'), ('Pacific/Yap', 'Pacific/Yap'), ('Asia/Qyzylorda', 'Asia/Qyzylorda'), ('America/Merida', 'America/Merida'), ('Asia/Tel_Aviv', 'Asia/Tel_Aviv'), ('Indian/Mauritius', 'Indian/Mauritius'), ('Iran', 'Iran'), ('Asia/Kamchatka', 'Asia/Kamchatka'), ('Asia/Kolkata', 'Asia/Kolkata'), ('Etc/GMT+12', 'Etc/GMT+12'), ('Africa/Banjul', 'Africa/Banjul'), ('Etc/GMT-7', 'Etc/GMT-7'), ('Europe/Volgograd', 'Europe/Volgograd'), ('Etc/GMT+7', 'Etc/GMT+7'), ('Asia/Bahrain', 'Asia/Bahrain'), ('Europe/Simferopol', 'Europe/Simferopol'), ('Pacific/Noumea', 'Pacific/Noumea'), ('America/Godthab', 'America/Godthab'), ('America/La_Paz', 'America/La_Paz'), ('NZ-CHAT', 'NZ-CHAT'), ('America/Port_of_Spain', 'America/Port_of_Spain'), ('America/Marigot', 'America/Marigot'), ('Australia/Hobart', 'Australia/Hobart'), ('America/Inuvik', 'America/Inuvik'), ('Canada/Central', 'Canada/Central'), ('Asia/Harbin', 'Asia/Harbin'), ('America/New_York', 'America/New_York'), ('CET', 'CET'), ('Antarctica/Mawson', 'Antarctica/Mawson'), ('America/Yellowknife', 'America/Yellowknife'), ('US/Samoa', 'US/Samoa'), ('America/Belem', 'America/Belem'), ('Africa/Asmera', 'Africa/Asmera'), ('Canada/Mountain', 'Canada/Mountain'), ('Africa/Juba', 'Africa/Juba'), ('Asia/Choibalsan', 'Asia/Choibalsan'), ('Europe/Oslo', 'Europe/Oslo'), ('Asia/Qostanay', 'Asia/Qostanay'), ('America/Belize', 'America/Belize'), ('America/Mendoza', 'America/Mendoza'), ('Africa/Dar_es_Salaam', 'Africa/Dar_es_Salaam'), ('Antarctica/Syowa', 'Antarctica/Syowa'), ('Asia/Vientiane', 'Asia/Vientiane'), ('America/Indiana/Vevay', 'America/Indiana/Vevay'), ('Pacific/Efate', 'Pacific/Efate'), ('Antarctica/Troll', 'Antarctica/Troll'), ('Asia/Chungking', 'Asia/Chungking'), ('Australia/Canberra', 'Australia/Canberra'), ('America/St_Lucia', 'America/St_Lucia'), ('Australia/Perth', 'Australia/Perth'), ('America/North_Dakota/Center', 'America/North_Dakota/Center'), ('Pacific/Apia', 'Pacific/Apia'), ('Europe/Sofia', 'Europe/Sofia'), ('Etc/GMT-6', 'Etc/GMT-6'), ('America/Port-au-Prince', 'America/Port-au-Prince'), ('Pacific/Tahiti', 'Pacific/Tahiti'), ('Asia/Novosibirsk', 'Asia/Novosibirsk'), ('Universal', 'Universal'), ('Africa/Tunis', 'Africa/Tunis'), ('Africa/Kampala', 'Africa/Kampala'), ('GMT+0', 'GMT+0'), ('Asia/Novokuznetsk', 'Asia/Novokuznetsk'), ('Africa/Tripoli', 'Africa/Tripoli'), ('Pacific/Nauru', 'Pacific/Nauru'), ('Atlantic/Stanley', 'Atlantic/Stanley'), ('Africa/Mogadishu', 'Africa/Mogadishu'), ('Europe/Jersey', 'Europe/Jersey'), ('America/Indianapolis', 'America/Indianapolis'), ('Pacific/Auckland', 'Pacific/Auckland'), ('Asia/Almaty', 'Asia/Almaty'), ('Japan', 'Japan'), ('Asia/Tashkent', 'Asia/Tashkent'), ('Asia/Aden', 'Asia/Aden'), ('Canada/Yukon', 'Canada/Yukon'), ('America/Nuuk', 'America/Nuuk'), ('Australia/NSW', 'Australia/NSW'), ('America/Eirunepe', 'America/Eirunepe'), ('Asia/Istanbul', 'Asia/Istanbul'), ('Atlantic/Jan_Mayen', 'Atlantic/Jan_Mayen'), ('Chile/Continental', 'Chile/Continental'), ('America/Argentina/La_Rioja', 'America/Argentina/La_Rioja'), ('Africa/Porto-Novo', 'Africa/Porto-Novo'), ('America/Rio_Branco', 'America/Rio_Branco'), ('Pacific/Tarawa', 'Pacific/Tarawa'), ('Europe/San_Marino', 'Europe/San_Marino'), ('Asia/Taipei', 'Asia/Taipei'), ('Asia/Tomsk', 'Asia/Tomsk'), ('Pacific/Midway', 'Pacific/Midway'), ('Europe/Nicosia', 'Europe/Nicosia'), ('America/Argentina/Catamarca', 'America/Argentina/Catamarca'), ('America/Lima', 'America/Lima'), ('Asia/Damascus', 'Asia/Damascus'), ('America/Asuncion', 'America/Asuncion'), ('Pacific/Kosrae', 'Pacific/Kosrae'), ('Europe/Kirov', 'Europe/Kirov'), ('America/Guatemala', 'America/Guatemala'), ('Poland', 'Poland'), ('America/Argentina/Mendoza', 'America/Argentina/Mendoza'), ('America/Porto_Acre', 'America/Porto_Acre'), ('Europe/Zaporozhye', 'Europe/Zaporozhye'), ('Asia/Qatar', 'Asia/Qatar'), ('America/Managua', 'America/Managua'), ('Etc/GMT+6', 'Etc/GMT+6'), ('Asia/Kathmandu', 'Asia/Kathmandu'), ('America/Barbados', 'America/Barbados'), ('Asia/Brunei', 'Asia/Brunei'), ('Europe/Vaduz', 'Europe/Vaduz'), ('America/Costa_Rica', 'America/Costa_Rica'), ('Asia/Yerevan', 'Asia/Yerevan'), ('Iceland', 'Iceland'), ('Antarctica/South_Pole', 'Antarctica/South_Pole'), ('Europe/Skopje', 'Europe/Skopje'), ('Australia/Brisbane', 'Australia/Brisbane'), ('Etc/GMT0', 'Etc/GMT0'), ('Africa/Mbabane', 'Africa/Mbabane'), ('Australia/Broken_Hill', 'Australia/Broken_Hill'), ('Asia/Macao', 'Asia/Macao'), ('Europe/Riga', 'Europe/Riga'), ('Australia/ACT', 'Australia/ACT'), ('Europe/Brussels', 'Europe/Brussels'), ('Africa/Nairobi', 'Africa/Nairobi'), ('America/St_Vincent', 'America/St_Vincent'), ('America/Argentina/San_Juan', 'America/Argentina/San_Juan'), ('Pacific/Chuuk', 'Pacific/Chuuk'), ('Asia/Karachi', 'Asia/Karachi'), ('Europe/Tirane', 'Europe/Tirane'), ('Pacific/Fiji', 'Pacific/Fiji'), ('America/Caracas', 'America/Caracas'), ('Europe/Moscow', 'Europe/Moscow'), ('America/Recife', 'America/Recife'), ('America/Bogota', 'America/Bogota'), ('Africa/Blantyre', 'Africa/Blantyre'), ('Asia/Dushanbe', 'Asia/Dushanbe'), ('Asia/Vladivostok', 'Asia/Vladivostok'), ('Pacific/Honolulu', 'Pacific/Honolulu'), ('America/Louisville', 'America/Louisville'), ('Asia/Colombo', 'Asia/Colombo'), ('Europe/Madrid', 'Europe/Madrid'), ('America/Halifax', 'America/Halifax'), ('Atlantic/Cape_Verde', 'Atlantic/Cape_Verde'), ('Europe/Uzhgorod', 'Europe/Uzhgorod'), ('Indian/Kerguelen', 'Indian/Kerguelen'), ('Canada/Saskatchewan', 'Canada/Saskatchewan'), ('EET', 'EET'), ('Pacific/Kiritimati', 'Pacific/Kiritimati'), ('America/Guadeloupe', 'America/Guadeloupe'), ('Europe/Andorra', 'Europe/Andorra'), ('Etc/GMT-11', 'Etc/GMT-11'), ('Europe/Belgrade', 'Europe/Belgrade'), ('America/Whitehorse', 'America/Whitehorse'), ('America/Glace_Bay', 'America/Glace_Bay'), ('Pacific/Guadalcanal', 'Pacific/Guadalcanal'), ('Africa/Brazzaville', 'Africa/Brazzaville'), ('Asia/Tbilisi', 'Asia/Tbilisi'), ('Australia/Sydney', 'Australia/Sydney'), ('Asia/Kashgar', 'Asia/Kashgar'), ('Asia/Sakhalin', 'Asia/Sakhalin'), ('PRC', 'PRC')], default='Asia/Kolkata', max_length=50, verbose_name='Time zone'),
        ),
    ]