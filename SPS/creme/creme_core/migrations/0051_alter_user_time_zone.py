# Generated by Django 4.2.6 on 2023-10-17 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creme_core', '0050_alter_user_time_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='time_zone',
            field=models.CharField(choices=[('Pacific/Chatham', 'Pacific/Chatham'), ('Asia/Makassar', 'Asia/Makassar'), ('GB', 'GB'), ('Europe/Copenhagen', 'Europe/Copenhagen'), ('Asia/Qatar', 'Asia/Qatar'), ('Asia/Aden', 'Asia/Aden'), ('Antarctica/DumontDUrville', 'Antarctica/DumontDUrville'), ('MET', 'MET'), ('Pacific/Fiji', 'Pacific/Fiji'), ('Australia/Yancowinna', 'Australia/Yancowinna'), ('Australia/Lord_Howe', 'Australia/Lord_Howe'), ('Asia/Phnom_Penh', 'Asia/Phnom_Penh'), ('GMT-0', 'GMT-0'), ('Australia/Queensland', 'Australia/Queensland'), ('America/Louisville', 'America/Louisville'), ('Europe/Podgorica', 'Europe/Podgorica'), ('America/Argentina/ComodRivadavia', 'America/Argentina/ComodRivadavia'), ('Atlantic/Bermuda', 'Atlantic/Bermuda'), ('Etc/Greenwich', 'Etc/Greenwich'), ('America/Creston', 'America/Creston'), ('America/Guyana', 'America/Guyana'), ('Asia/Dushanbe', 'Asia/Dushanbe'), ('Asia/Thimphu', 'Asia/Thimphu'), ('Asia/Bishkek', 'Asia/Bishkek'), ('America/Lima', 'America/Lima'), ('Asia/Jakarta', 'Asia/Jakarta'), ('Arctic/Longyearbyen', 'Arctic/Longyearbyen'), ('Atlantic/Canary', 'Atlantic/Canary'), ('Pacific/Kosrae', 'Pacific/Kosrae'), ('America/North_Dakota/Center', 'America/North_Dakota/Center'), ('Etc/GMT+7', 'Etc/GMT+7'), ('Europe/Andorra', 'Europe/Andorra'), ('Asia/Chita', 'Asia/Chita'), ('Greenwich', 'Greenwich'), ('America/El_Salvador', 'America/El_Salvador'), ('Africa/Addis_Ababa', 'Africa/Addis_Ababa'), ('America/Buenos_Aires', 'America/Buenos_Aires'), ('America/Argentina/Mendoza', 'America/Argentina/Mendoza'), ('America/Blanc-Sablon', 'America/Blanc-Sablon'), ('Africa/Niamey', 'Africa/Niamey'), ('America/Metlakatla', 'America/Metlakatla'), ('Africa/Johannesburg', 'Africa/Johannesburg'), ('America/Thule', 'America/Thule'), ('Canada/Saskatchewan', 'Canada/Saskatchewan'), ('America/Indiana/Vevay', 'America/Indiana/Vevay'), ('America/La_Paz', 'America/La_Paz'), ('America/Santa_Isabel', 'America/Santa_Isabel'), ('Africa/Asmara', 'Africa/Asmara'), ('America/Punta_Arenas', 'America/Punta_Arenas'), ('Asia/Pyongyang', 'Asia/Pyongyang'), ('Europe/Guernsey', 'Europe/Guernsey'), ('Antarctica/Troll', 'Antarctica/Troll'), ('Europe/Ljubljana', 'Europe/Ljubljana'), ('Pacific/Samoa', 'Pacific/Samoa'), ('America/Danmarkshavn', 'America/Danmarkshavn'), ('America/Lower_Princes', 'America/Lower_Princes'), ('America/Caracas', 'America/Caracas'), ('Asia/Brunei', 'Asia/Brunei'), ('America/Belize', 'America/Belize'), ('CET', 'CET'), ('America/Boa_Vista', 'America/Boa_Vista'), ('Europe/Vienna', 'Europe/Vienna'), ('Indian/Mayotte', 'Indian/Mayotte'), ('Asia/Karachi', 'Asia/Karachi'), ('America/Porto_Velho', 'America/Porto_Velho'), ('Etc/UTC', 'Etc/UTC'), ('Africa/Kampala', 'Africa/Kampala'), ('Europe/Chisinau', 'Europe/Chisinau'), ('America/Argentina/San_Luis', 'America/Argentina/San_Luis'), ('Asia/Qostanay', 'Asia/Qostanay'), ('Etc/GMT+5', 'Etc/GMT+5'), ('Africa/Libreville', 'Africa/Libreville'), ('Asia/Kolkata', 'Asia/Kolkata'), ('Asia/Colombo', 'Asia/Colombo'), ('Europe/Kirov', 'Europe/Kirov'), ('Europe/Athens', 'Europe/Athens'), ('Etc/GMT-6', 'Etc/GMT-6'), ('Asia/Kamchatka', 'Asia/Kamchatka'), ('America/Kralendijk', 'America/Kralendijk'), ('Atlantic/St_Helena', 'Atlantic/St_Helena'), ('America/Yakutat', 'America/Yakutat'), ('Asia/Choibalsan', 'Asia/Choibalsan'), ('Asia/Khandyga', 'Asia/Khandyga'), ('Factory', 'Factory'), ('America/Santo_Domingo', 'America/Santo_Domingo'), ('Europe/Skopje', 'Europe/Skopje'), ('UTC', 'UTC'), ('America/Barbados', 'America/Barbados'), ('Europe/Zagreb', 'Europe/Zagreb'), ('Asia/Seoul', 'Asia/Seoul'), ('US/Samoa', 'US/Samoa'), ('Africa/Ouagadougou', 'Africa/Ouagadougou'), ('America/Adak', 'America/Adak'), ('America/Glace_Bay', 'America/Glace_Bay'), ('Chile/Continental', 'Chile/Continental'), ('Asia/Shanghai', 'Asia/Shanghai'), ('America/Argentina/Cordoba', 'America/Argentina/Cordoba'), ('Europe/Ulyanovsk', 'Europe/Ulyanovsk'), ('Canada/Pacific', 'Canada/Pacific'), ('Asia/Yangon', 'Asia/Yangon'), ('America/Kentucky/Louisville', 'America/Kentucky/Louisville'), ('Europe/Isle_of_Man', 'Europe/Isle_of_Man'), ('Europe/Dublin', 'Europe/Dublin'), ('America/Fort_Nelson', 'America/Fort_Nelson'), ('Australia/LHI', 'Australia/LHI'), ('America/Asuncion', 'America/Asuncion'), ('Africa/Monrovia', 'Africa/Monrovia'), ('Europe/Vaduz', 'Europe/Vaduz'), ('Iran', 'Iran'), ('America/Araguaina', 'America/Araguaina'), ('Africa/Maputo', 'Africa/Maputo'), ('America/Dominica', 'America/Dominica'), ('Europe/Nicosia', 'Europe/Nicosia'), ('Universal', 'Universal'), ('Pacific/Marquesas', 'Pacific/Marquesas'), ('Antarctica/South_Pole', 'Antarctica/South_Pole'), ('Brazil/West', 'Brazil/West'), ('America/Inuvik', 'America/Inuvik'), ('Africa/Malabo', 'Africa/Malabo'), ('America/Shiprock', 'America/Shiprock'), ('Antarctica/Rothera', 'Antarctica/Rothera'), ('Pacific/Port_Moresby', 'Pacific/Port_Moresby'), ('US/East-Indiana', 'US/East-Indiana'), ('Africa/Cairo', 'Africa/Cairo'), ('Australia/Eucla', 'Australia/Eucla'), ('Europe/Luxembourg', 'Europe/Luxembourg'), ('America/Chicago', 'America/Chicago'), ('America/Panama', 'America/Panama'), ('America/Phoenix', 'America/Phoenix'), ('Australia/Brisbane', 'Australia/Brisbane'), ('Indian/Reunion', 'Indian/Reunion'), ('America/Santiago', 'America/Santiago'), ('Atlantic/Cape_Verde', 'Atlantic/Cape_Verde'), ('Europe/Oslo', 'Europe/Oslo'), ('America/Grenada', 'America/Grenada'), ('America/Fort_Wayne', 'America/Fort_Wayne'), ('America/Bahia', 'America/Bahia'), ('Africa/Tunis', 'Africa/Tunis'), ('Asia/Baku', 'Asia/Baku'), ('Europe/Saratov', 'Europe/Saratov'), ('Brazil/Acre', 'Brazil/Acre'), ('Europe/Belgrade', 'Europe/Belgrade'), ('Asia/Dili', 'Asia/Dili'), ('W-SU', 'W-SU'), ('Asia/Krasnoyarsk', 'Asia/Krasnoyarsk'), ('Australia/ACT', 'Australia/ACT'), ('America/Menominee', 'America/Menominee'), ('Europe/Tiraspol', 'Europe/Tiraspol'), ('Pacific/Chuuk', 'Pacific/Chuuk'), ('America/Godthab', 'America/Godthab'), ('Antarctica/Davis', 'Antarctica/Davis'), ('Pacific/Midway', 'Pacific/Midway'), ('Asia/Samarkand', 'Asia/Samarkand'), ('Africa/Douala', 'Africa/Douala'), ('Asia/Nicosia', 'Asia/Nicosia'), ('Asia/Ust-Nera', 'Asia/Ust-Nera'), ('Brazil/East', 'Brazil/East'), ('Pacific/Guadalcanal', 'Pacific/Guadalcanal'), ('NZ-CHAT', 'NZ-CHAT'), ('Asia/Aqtobe', 'Asia/Aqtobe'), ('Asia/Kuching', 'Asia/Kuching'), ('Asia/Singapore', 'Asia/Singapore'), ('Africa/Casablanca', 'Africa/Casablanca'), ('Europe/Istanbul', 'Europe/Istanbul'), ('Canada/Atlantic', 'Canada/Atlantic'), ('Etc/GMT+8', 'Etc/GMT+8'), ('America/Anchorage', 'America/Anchorage'), ('Europe/Simferopol', 'Europe/Simferopol'), ('Europe/Rome', 'Europe/Rome'), ('America/Miquelon', 'America/Miquelon'), ('US/Arizona', 'US/Arizona'), ('America/Whitehorse', 'America/Whitehorse'), ('America/Sao_Paulo', 'America/Sao_Paulo'), ('Atlantic/Madeira', 'Atlantic/Madeira'), ('Africa/Conakry', 'Africa/Conakry'), ('America/North_Dakota/Beulah', 'America/North_Dakota/Beulah'), ('Jamaica', 'Jamaica'), ('Etc/GMT+12', 'Etc/GMT+12'), ('America/Manaus', 'America/Manaus'), ('Cuba', 'Cuba'), ('Asia/Magadan', 'Asia/Magadan'), ('America/Boise', 'America/Boise'), ('Europe/San_Marino', 'Europe/San_Marino'), ('Asia/Hovd', 'Asia/Hovd'), ('America/Grand_Turk', 'America/Grand_Turk'), ('America/Indiana/Knox', 'America/Indiana/Knox'), ('Turkey', 'Turkey'), ('Etc/GMT+6', 'Etc/GMT+6'), ('Atlantic/Faeroe', 'Atlantic/Faeroe'), ('Etc/GMT-7', 'Etc/GMT-7'), ('Europe/Minsk', 'Europe/Minsk'), ('Libya', 'Libya'), ('America/Virgin', 'America/Virgin'), ('Etc/GMT+2', 'Etc/GMT+2'), ('Canada/Central', 'Canada/Central'), ('America/Anguilla', 'America/Anguilla'), ('America/St_Thomas', 'America/St_Thomas'), ('America/Mendoza', 'America/Mendoza'), ('Pacific/Galapagos', 'Pacific/Galapagos'), ('America/Bahia_Banderas', 'America/Bahia_Banderas'), ('Atlantic/Jan_Mayen', 'Atlantic/Jan_Mayen'), ('Etc/GMT-12', 'Etc/GMT-12'), ('Asia/Istanbul', 'Asia/Istanbul'), ('Australia/NSW', 'Australia/NSW'), ('Asia/Urumqi', 'Asia/Urumqi'), ('Pacific/Rarotonga', 'Pacific/Rarotonga'), ('Europe/Tirane', 'Europe/Tirane'), ('Asia/Ashkhabad', 'Asia/Ashkhabad'), ('America/Argentina/Salta', 'America/Argentina/Salta'), ('Asia/Ulan_Bator', 'Asia/Ulan_Bator'), ('Asia/Tbilisi', 'Asia/Tbilisi'), ('Etc/GMT+11', 'Etc/GMT+11'), ('America/Resolute', 'America/Resolute'), ('EST5EDT', 'EST5EDT'), ('America/Recife', 'America/Recife'), ('America/Montreal', 'America/Montreal'), ('Asia/Oral', 'Asia/Oral'), ('Indian/Mauritius', 'Indian/Mauritius'), ('Australia/Currie', 'Australia/Currie'), ('Asia/Thimbu', 'Asia/Thimbu'), ('America/Indiana/Winamac', 'America/Indiana/Winamac'), ('Etc/GMT-3', 'Etc/GMT-3'), ('Australia/Victoria', 'Australia/Victoria'), ('Pacific/Pohnpei', 'Pacific/Pohnpei'), ('WET', 'WET'), ('Pacific/Fakaofo', 'Pacific/Fakaofo'), ('Pacific/Yap', 'Pacific/Yap'), ('Hongkong', 'Hongkong'), ('UCT', 'UCT'), ('PRC', 'PRC'), ('Africa/Juba', 'Africa/Juba'), ('America/Knox_IN', 'America/Knox_IN'), ('Iceland', 'Iceland'), ('America/Indiana/Indianapolis', 'America/Indiana/Indianapolis'), ('Pacific/Truk', 'Pacific/Truk'), ('America/Winnipeg', 'America/Winnipeg'), ('Europe/Astrakhan', 'Europe/Astrakhan'), ('Etc/GMT-1', 'Etc/GMT-1'), ('Asia/Macao', 'Asia/Macao'), ('Asia/Manila', 'Asia/Manila'), ('America/Kentucky/Monticello', 'America/Kentucky/Monticello'), ('Asia/Srednekolymsk', 'Asia/Srednekolymsk'), ('America/North_Dakota/New_Salem', 'America/North_Dakota/New_Salem'), ('Canada/Mountain', 'Canada/Mountain'), ('America/Campo_Grande', 'America/Campo_Grande'), ('MST', 'MST'), ('Africa/Bamako', 'Africa/Bamako'), ('Australia/Adelaide', 'Australia/Adelaide'), ('Etc/GMT', 'Etc/GMT'), ('Pacific/Kiritimati', 'Pacific/Kiritimati'), ('Indian/Christmas', 'Indian/Christmas'), ('Australia/Lindeman', 'Australia/Lindeman'), ('Asia/Yakutsk', 'Asia/Yakutsk'), ('Atlantic/Azores', 'Atlantic/Azores'), ('Asia/Kuala_Lumpur', 'Asia/Kuala_Lumpur'), ('Australia/Sydney', 'Australia/Sydney'), ('Asia/Novosibirsk', 'Asia/Novosibirsk'), ('Asia/Chungking', 'Asia/Chungking'), ('Asia/Jayapura', 'Asia/Jayapura'), ('Europe/Stockholm', 'Europe/Stockholm'), ('Asia/Taipei', 'Asia/Taipei'), ('Europe/Moscow', 'Europe/Moscow'), ('Antarctica/Syowa', 'Antarctica/Syowa'), ('America/Atka', 'America/Atka'), ('Pacific/Bougainville', 'Pacific/Bougainville'), ('Asia/Bangkok', 'Asia/Bangkok'), ('America/Belem', 'America/Belem'), ('Africa/Lubumbashi', 'Africa/Lubumbashi'), ('Africa/Maseru', 'Africa/Maseru'), ('Africa/Asmera', 'Africa/Asmera'), ('America/Moncton', 'America/Moncton'), ('Asia/Chongqing', 'Asia/Chongqing'), ('Asia/Famagusta', 'Asia/Famagusta'), ('Pacific/Tarawa', 'Pacific/Tarawa'), ('America/Swift_Current', 'America/Swift_Current'), ('Africa/Nouakchott', 'Africa/Nouakchott'), ('Europe/Zurich', 'Europe/Zurich'), ('Europe/Gibraltar', 'Europe/Gibraltar'), ('America/Eirunepe', 'America/Eirunepe'), ('Africa/Lome', 'Africa/Lome'), ('Pacific/Efate', 'Pacific/Efate'), ('America/Hermosillo', 'America/Hermosillo'), ('Africa/Porto-Novo', 'Africa/Porto-Novo'), ('Europe/Brussels', 'Europe/Brussels'), ('America/Los_Angeles', 'America/Los_Angeles'), ('Europe/Belfast', 'Europe/Belfast'), ('Africa/Freetown', 'Africa/Freetown'), ('Asia/Pontianak', 'Asia/Pontianak'), ('Africa/Lagos', 'Africa/Lagos'), ('Atlantic/Faroe', 'Atlantic/Faroe'), ('Indian/Mahe', 'Indian/Mahe'), ('Pacific/Ponape', 'Pacific/Ponape'), ('America/Chihuahua', 'America/Chihuahua'), ('Asia/Dubai', 'Asia/Dubai'), ('Asia/Irkutsk', 'Asia/Irkutsk'), ('Indian/Cocos', 'Indian/Cocos'), ('Africa/Tripoli', 'Africa/Tripoli'), ('Europe/Vatican', 'Europe/Vatican'), ('Asia/Amman', 'Asia/Amman'), ('Europe/Volgograd', 'Europe/Volgograd'), ('Etc/GMT-4', 'Etc/GMT-4'), ('America/Jujuy', 'America/Jujuy'), ('America/Vancouver', 'America/Vancouver'), ('Asia/Tehran', 'Asia/Tehran'), ('America/St_Barthelemy', 'America/St_Barthelemy'), ('Asia/Kathmandu', 'Asia/Kathmandu'), ('Atlantic/Reykjavik', 'Atlantic/Reykjavik'), ('Europe/Tallinn', 'Europe/Tallinn'), ('Africa/Ndjamena', 'Africa/Ndjamena'), ('America/Pangnirtung', 'America/Pangnirtung'), ('Etc/GMT-5', 'Etc/GMT-5'), ('Asia/Anadyr', 'Asia/Anadyr'), ('Canada/Newfoundland', 'Canada/Newfoundland'), ('Canada/Yukon', 'Canada/Yukon'), ('America/Toronto', 'America/Toronto'), ('America/Indiana/Marengo', 'America/Indiana/Marengo'), ('GMT+0', 'GMT+0'), ('Europe/Vilnius', 'Europe/Vilnius'), ('America/Nome', 'America/Nome'), ('America/Cancun', 'America/Cancun'), ('US/Michigan', 'US/Michigan'), ('America/Argentina/Ushuaia', 'America/Argentina/Ushuaia'), ('Pacific/Easter', 'Pacific/Easter'), ('America/Argentina/Tucuman', 'America/Argentina/Tucuman'), ('US/Hawaii', 'US/Hawaii'), ('Australia/West', 'Australia/West'), ('Egypt', 'Egypt'), ('America/New_York', 'America/New_York'), ('Asia/Kashgar', 'Asia/Kashgar'), ('America/Bogota', 'America/Bogota'), ('America/Halifax', 'America/Halifax'), ('Kwajalein', 'Kwajalein'), ('America/Atikokan', 'America/Atikokan'), ('Pacific/Wallis', 'Pacific/Wallis'), ('America/Iqaluit', 'America/Iqaluit'), ('Pacific/Tongatapu', 'Pacific/Tongatapu'), ('Pacific/Apia', 'Pacific/Apia'), ('Asia/Damascus', 'Asia/Damascus'), ('Europe/Madrid', 'Europe/Madrid'), ('America/Porto_Acre', 'America/Porto_Acre'), ('Asia/Novokuznetsk', 'Asia/Novokuznetsk'), ('Africa/Brazzaville', 'Africa/Brazzaville'), ('Europe/Amsterdam', 'Europe/Amsterdam'), ('Africa/Mogadishu', 'Africa/Mogadishu'), ('Pacific/Niue', 'Pacific/Niue'), ('Europe/Riga', 'Europe/Riga'), ('America/Juneau', 'America/Juneau'), ('America/Maceio', 'America/Maceio'), ('America/Mexico_City', 'America/Mexico_City'), ('Indian/Maldives', 'Indian/Maldives'), ('Asia/Muscat', 'Asia/Muscat'), ('Asia/Ujung_Pandang', 'Asia/Ujung_Pandang'), ('Mexico/BajaNorte', 'Mexico/BajaNorte'), ('Europe/Warsaw', 'Europe/Warsaw'), ('America/Paramaribo', 'America/Paramaribo'), ('Asia/Yerevan', 'Asia/Yerevan'), ('Asia/Qyzylorda', 'Asia/Qyzylorda'), ('Europe/Kyiv', 'Europe/Kyiv'), ('Antarctica/McMurdo', 'Antarctica/McMurdo'), ('Antarctica/Macquarie', 'Antarctica/Macquarie'), ('America/Nipigon', 'America/Nipigon'), ('America/Monterrey', 'America/Monterrey'), ('Pacific/Kwajalein', 'Pacific/Kwajalein'), ('America/Guatemala', 'America/Guatemala'), ('Etc/GMT+9', 'Etc/GMT+9'), ('America/Sitka', 'America/Sitka'), ('America/Rosario', 'America/Rosario'), ('Asia/Barnaul', 'Asia/Barnaul'), ('America/Guayaquil', 'America/Guayaquil'), ('Etc/GMT-9', 'Etc/GMT-9'), ('America/Marigot', 'America/Marigot'), ('Europe/Prague', 'Europe/Prague'), ('Europe/Malta', 'Europe/Malta'), ('Pacific/Gambier', 'Pacific/Gambier'), ('ROC', 'ROC'), ('Africa/Bissau', 'Africa/Bissau'), ('CST6CDT', 'CST6CDT'), ('GMT0', 'GMT0'), ('Pacific/Funafuti', 'Pacific/Funafuti'), ('Chile/EasterIsland', 'Chile/EasterIsland'), ('Australia/Hobart', 'Australia/Hobart'), ('Navajo', 'Navajo'), ('Asia/Tashkent', 'Asia/Tashkent'), ('Pacific/Pitcairn', 'Pacific/Pitcairn'), ('Asia/Jerusalem', 'Asia/Jerusalem'), ('Africa/Kigali', 'Africa/Kigali'), ('America/Antigua', 'America/Antigua'), ('Canada/Eastern', 'Canada/Eastern'), ('Etc/Zulu', 'Etc/Zulu'), ('America/Regina', 'America/Regina'), ('Etc/GMT+3', 'Etc/GMT+3'), ('Africa/Bangui', 'Africa/Bangui'), ('America/Mazatlan', 'America/Mazatlan'), ('America/Tortola', 'America/Tortola'), ('Indian/Kerguelen', 'Indian/Kerguelen'), ('Europe/Mariehamn', 'Europe/Mariehamn'), ('GB-Eire', 'GB-Eire'), ('Europe/Budapest', 'Europe/Budapest'), ('America/Tegucigalpa', 'America/Tegucigalpa'), ('America/Cayman', 'America/Cayman'), ('Africa/Bujumbura', 'Africa/Bujumbura'), ('Poland', 'Poland'), ('America/Rio_Branco', 'America/Rio_Branco'), ('America/Nuuk', 'America/Nuuk'), ('Etc/GMT-14', 'Etc/GMT-14'), ('Africa/Gaborone', 'Africa/Gaborone'), ('America/St_Kitts', 'America/St_Kitts'), ('Asia/Katmandu', 'Asia/Katmandu'), ('Asia/Dhaka', 'Asia/Dhaka'), ('Antarctica/Mawson', 'Antarctica/Mawson'), ('Europe/Uzhgorod', 'Europe/Uzhgorod'), ('Asia/Harbin', 'Asia/Harbin'), ('America/Ojinaga', 'America/Ojinaga'), ('Africa/Harare', 'Africa/Harare'), ('America/Indianapolis', 'America/Indianapolis'), ('Asia/Almaty', 'Asia/Almaty'), ('Europe/Helsinki', 'Europe/Helsinki'), ('US/Alaska', 'US/Alaska'), ('GMT', 'GMT'), ('EST', 'EST'), ('America/Detroit', 'America/Detroit'), ('Pacific/Honolulu', 'Pacific/Honolulu'), ('America/Argentina/Catamarca', 'America/Argentina/Catamarca'), ('Asia/Vladivostok', 'Asia/Vladivostok'), ('America/Montserrat', 'America/Montserrat'), ('Asia/Rangoon', 'Asia/Rangoon'), ('Asia/Gaza', 'Asia/Gaza'), ('America/St_Vincent', 'America/St_Vincent'), ('Indian/Comoro', 'Indian/Comoro'), ('Asia/Ashgabat', 'Asia/Ashgabat'), ('Atlantic/South_Georgia', 'Atlantic/South_Georgia'), ('Africa/Luanda', 'Africa/Luanda'), ('Mexico/General', 'Mexico/General'), ('MST7MDT', 'MST7MDT'), ('Japan', 'Japan'), ('America/Yellowknife', 'America/Yellowknife'), ('Asia/Tokyo', 'Asia/Tokyo'), ('Africa/El_Aaiun', 'Africa/El_Aaiun'), ('Asia/Tomsk', 'Asia/Tomsk'), ('Europe/Busingen', 'Europe/Busingen'), ('Europe/Kiev', 'Europe/Kiev'), ('US/Indiana-Starke', 'US/Indiana-Starke'), ('America/St_Johns', 'America/St_Johns'), ('America/Goose_Bay', 'America/Goose_Bay'), ('Africa/Abidjan', 'Africa/Abidjan'), ('Europe/Berlin', 'Europe/Berlin'), ('Pacific/Guam', 'Pacific/Guam'), ('America/Scoresbysund', 'America/Scoresbysund'), ('America/Noronha', 'America/Noronha'), ('America/Indiana/Petersburg', 'America/Indiana/Petersburg'), ('Brazil/DeNoronha', 'Brazil/DeNoronha'), ('Pacific/Johnston', 'Pacific/Johnston'), ('Asia/Atyrau', 'Asia/Atyrau'), ('America/Catamarca', 'America/Catamarca'), ('Asia/Tel_Aviv', 'Asia/Tel_Aviv'), ('Zulu', 'Zulu'), ('Africa/Timbuktu', 'Africa/Timbuktu'), ('Australia/Perth', 'Australia/Perth'), ('Europe/Sofia', 'Europe/Sofia'), ('America/Jamaica', 'America/Jamaica'), ('Australia/Melbourne', 'Australia/Melbourne'), ('HST', 'HST'), ('America/Cordoba', 'America/Cordoba'), ('Africa/Sao_Tome', 'Africa/Sao_Tome'), ('America/Tijuana', 'America/Tijuana'), ('Africa/Dakar', 'Africa/Dakar'), ('America/Coral_Harbour', 'America/Coral_Harbour'), ('Europe/Monaco', 'Europe/Monaco'), ('Asia/Baghdad', 'Asia/Baghdad'), ('Asia/Dacca', 'Asia/Dacca'), ('America/Curacao', 'America/Curacao'), ('Pacific/Saipan', 'Pacific/Saipan'), ('Africa/Banjul', 'Africa/Banjul'), ('Etc/UCT', 'Etc/UCT'), ('Australia/Darwin', 'Australia/Darwin'), ('Pacific/Auckland', 'Pacific/Auckland'), ('Europe/Paris', 'Europe/Paris'), ('Africa/Accra', 'Africa/Accra'), ('Antarctica/Palmer', 'Antarctica/Palmer'), ('Europe/Lisbon', 'Europe/Lisbon'), ('Africa/Djibouti', 'Africa/Djibouti'), ('America/Argentina/La_Rioja', 'America/Argentina/La_Rioja'), ('Asia/Saigon', 'Asia/Saigon'), ('America/Denver', 'America/Denver'), ('America/Port-au-Prince', 'America/Port-au-Prince'), ('US/Central', 'US/Central'), ('Asia/Kabul', 'Asia/Kabul'), ('America/Havana', 'America/Havana'), ('Etc/GMT-10', 'Etc/GMT-10'), ('Africa/Lusaka', 'Africa/Lusaka'), ('Africa/Dar_es_Salaam', 'Africa/Dar_es_Salaam'), ('Europe/Samara', 'Europe/Samara'), ('America/Matamoros', 'America/Matamoros'), ('America/Indiana/Tell_City', 'America/Indiana/Tell_City'), ('America/Rankin_Inlet', 'America/Rankin_Inlet'), ('US/Mountain', 'US/Mountain'), ('Etc/GMT-2', 'Etc/GMT-2'), ('Pacific/Wake', 'Pacific/Wake'), ('Europe/Bucharest', 'Europe/Bucharest'), ('Pacific/Palau', 'Pacific/Palau'), ('America/Costa_Rica', 'America/Costa_Rica'), ('Etc/Universal', 'Etc/Universal'), ('America/Ensenada', 'America/Ensenada'), ('America/Puerto_Rico', 'America/Puerto_Rico'), ('Antarctica/Vostok', 'Antarctica/Vostok'), ('Asia/Vientiane', 'Asia/Vientiane'), ('Singapore', 'Singapore'), ('Israel', 'Israel'), ('Asia/Aqtau', 'Asia/Aqtau'), ('America/St_Lucia', 'America/St_Lucia'), ('America/Cambridge_Bay', 'America/Cambridge_Bay'), ('America/Port_of_Spain', 'America/Port_of_Spain'), ('America/Montevideo', 'America/Montevideo'), ('Etc/GMT-11', 'Etc/GMT-11'), ('America/Aruba', 'America/Aruba'), ('Etc/GMT+0', 'Etc/GMT+0'), ('Asia/Omsk', 'Asia/Omsk'), ('America/Argentina/San_Juan', 'America/Argentina/San_Juan'), ('Asia/Ho_Chi_Minh', 'Asia/Ho_Chi_Minh'), ('Europe/Sarajevo', 'Europe/Sarajevo'), ('America/Santarem', 'America/Santarem'), ('US/Aleutian', 'US/Aleutian'), ('Etc/GMT-13', 'Etc/GMT-13'), ('Etc/GMT+10', 'Etc/GMT+10'), ('Australia/North', 'Australia/North'), ('US/Pacific', 'US/Pacific'), ('Pacific/Pago_Pago', 'Pacific/Pago_Pago'), ('Europe/Bratislava', 'Europe/Bratislava'), ('Asia/Yekaterinburg', 'Asia/Yekaterinburg'), ('Africa/Kinshasa', 'Africa/Kinshasa'), ('America/Martinique', 'America/Martinique'), ('America/Indiana/Vincennes', 'America/Indiana/Vincennes'), ('Africa/Mbabane', 'Africa/Mbabane'), ('America/Rainy_River', 'America/Rainy_River'), ('Africa/Khartoum', 'Africa/Khartoum'), ('America/Managua', 'America/Managua'), ('Asia/Riyadh', 'Asia/Riyadh'), ('Asia/Hebron', 'Asia/Hebron'), ('America/Thunder_Bay', 'America/Thunder_Bay'), ('America/Argentina/Rio_Gallegos', 'America/Argentina/Rio_Gallegos'), ('Asia/Macau', 'Asia/Macau'), ('Africa/Nairobi', 'Africa/Nairobi'), ('Asia/Ulaanbaatar', 'Asia/Ulaanbaatar'), ('Pacific/Majuro', 'Pacific/Majuro'), ('Pacific/Norfolk', 'Pacific/Norfolk'), ('America/Dawson_Creek', 'America/Dawson_Creek'), ('Pacific/Tahiti', 'Pacific/Tahiti'), ('Australia/Broken_Hill', 'Australia/Broken_Hill'), ('Africa/Algiers', 'Africa/Algiers'), ('PST8PDT', 'PST8PDT'), ('Europe/Zaporozhye', 'Europe/Zaporozhye'), ('Africa/Windhoek', 'Africa/Windhoek'), ('America/Dawson', 'America/Dawson'), ('America/Cayenne', 'America/Cayenne'), ('Etc/GMT+1', 'Etc/GMT+1'), ('Australia/South', 'Australia/South'), ('America/Nassau', 'America/Nassau'), ('America/Merida', 'America/Merida'), ('Africa/Blantyre', 'Africa/Blantyre'), ('Europe/London', 'Europe/London'), ('Eire', 'Eire'), ('Etc/GMT-8', 'Etc/GMT-8'), ('America/Edmonton', 'America/Edmonton'), ('America/Ciudad_Juarez', 'America/Ciudad_Juarez'), ('Etc/GMT0', 'Etc/GMT0'), ('America/Guadeloupe', 'America/Guadeloupe'), ('Pacific/Kanton', 'Pacific/Kanton'), ('Etc/GMT+4', 'Etc/GMT+4'), ('Asia/Sakhalin', 'Asia/Sakhalin'), ('Australia/Tasmania', 'Australia/Tasmania'), ('Pacific/Noumea', 'Pacific/Noumea'), ('Atlantic/Stanley', 'Atlantic/Stanley'), ('NZ', 'NZ'), ('Asia/Kuwait', 'Asia/Kuwait'), ('Indian/Antananarivo', 'Indian/Antananarivo'), ('Australia/Canberra', 'Australia/Canberra'), ('Asia/Bahrain', 'Asia/Bahrain'), ('Asia/Hong_Kong', 'Asia/Hong_Kong'), ('Mexico/BajaSur', 'Mexico/BajaSur'), ('Asia/Beirut', 'Asia/Beirut'), ('Europe/Jersey', 'Europe/Jersey'), ('Asia/Calcutta', 'Asia/Calcutta'), ('Pacific/Enderbury', 'Pacific/Enderbury'), ('America/Argentina/Jujuy', 'America/Argentina/Jujuy'), ('Portugal', 'Portugal'), ('Europe/Kaliningrad', 'Europe/Kaliningrad'), ('Indian/Chagos', 'Indian/Chagos'), ('America/Argentina/Buenos_Aires', 'America/Argentina/Buenos_Aires'), ('America/Fortaleza', 'America/Fortaleza'), ('US/Eastern', 'US/Eastern'), ('Antarctica/Casey', 'Antarctica/Casey'), ('Etc/GMT-0', 'Etc/GMT-0'), ('Pacific/Nauru', 'Pacific/Nauru'), ('Africa/Ceuta', 'Africa/Ceuta'), ('EET', 'EET'), ('ROK', 'ROK'), ('America/Cuiaba', 'America/Cuiaba')], default='Asia/Kolkata', max_length=50, verbose_name='Time zone'),
        ),
    ]
