# Generated by Django 4.2.6 on 2023-10-17 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creme_core', '0014_alter_user_time_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='time_zone',
            field=models.CharField(choices=[('Asia/Taipei', 'Asia/Taipei'), ('Europe/Madrid', 'Europe/Madrid'), ('America/Ciudad_Juarez', 'America/Ciudad_Juarez'), ('Etc/GMT+0', 'Etc/GMT+0'), ('Asia/Bahrain', 'Asia/Bahrain'), ('Africa/Mbabane', 'Africa/Mbabane'), ('Etc/GMT-7', 'Etc/GMT-7'), ('Asia/Ho_Chi_Minh', 'Asia/Ho_Chi_Minh'), ('America/Guadeloupe', 'America/Guadeloupe'), ('Asia/Qatar', 'Asia/Qatar'), ('Africa/Nairobi', 'Africa/Nairobi'), ('Asia/Anadyr', 'Asia/Anadyr'), ('America/Rio_Branco', 'America/Rio_Branco'), ('America/Porto_Velho', 'America/Porto_Velho'), ('Etc/UCT', 'Etc/UCT'), ('Asia/Famagusta', 'Asia/Famagusta'), ('CST6CDT', 'CST6CDT'), ('America/Miquelon', 'America/Miquelon'), ('Hongkong', 'Hongkong'), ('Poland', 'Poland'), ('Europe/Nicosia', 'Europe/Nicosia'), ('America/Manaus', 'America/Manaus'), ('Cuba', 'Cuba'), ('Africa/Banjul', 'Africa/Banjul'), ('Asia/Dhaka', 'Asia/Dhaka'), ('Etc/GMT', 'Etc/GMT'), ('America/Fortaleza', 'America/Fortaleza'), ('Australia/Perth', 'Australia/Perth'), ('Etc/GMT+7', 'Etc/GMT+7'), ('Etc/GMT-9', 'Etc/GMT-9'), ('Australia/ACT', 'Australia/ACT'), ('America/Rankin_Inlet', 'America/Rankin_Inlet'), ('Mexico/General', 'Mexico/General'), ('Antarctica/South_Pole', 'Antarctica/South_Pole'), ('Asia/Dushanbe', 'Asia/Dushanbe'), ('Asia/Calcutta', 'Asia/Calcutta'), ('America/Ojinaga', 'America/Ojinaga'), ('Europe/Chisinau', 'Europe/Chisinau'), ('Europe/Amsterdam', 'Europe/Amsterdam'), ('Etc/GMT-14', 'Etc/GMT-14'), ('Africa/Cairo', 'Africa/Cairo'), ('America/Anguilla', 'America/Anguilla'), ('America/Montserrat', 'America/Montserrat'), ('Indian/Mayotte', 'Indian/Mayotte'), ('Africa/Lome', 'Africa/Lome'), ('Africa/Harare', 'Africa/Harare'), ('Europe/Lisbon', 'Europe/Lisbon'), ('Pacific/Fiji', 'Pacific/Fiji'), ('Australia/Hobart', 'Australia/Hobart'), ('US/Michigan', 'US/Michigan'), ('America/Grenada', 'America/Grenada'), ('America/Havana', 'America/Havana'), ('Indian/Antananarivo', 'Indian/Antananarivo'), ('Singapore', 'Singapore'), ('Australia/Victoria', 'Australia/Victoria'), ('America/Argentina/Ushuaia', 'America/Argentina/Ushuaia'), ('US/Aleutian', 'US/Aleutian'), ('America/Sitka', 'America/Sitka'), ('Pacific/Midway', 'Pacific/Midway'), ('America/Coral_Harbour', 'America/Coral_Harbour'), ('America/North_Dakota/Beulah', 'America/North_Dakota/Beulah'), ('America/Atikokan', 'America/Atikokan'), ('Asia/Tomsk', 'Asia/Tomsk'), ('Asia/Makassar', 'Asia/Makassar'), ('HST', 'HST'), ('America/Halifax', 'America/Halifax'), ('US/East-Indiana', 'US/East-Indiana'), ('Antarctica/Casey', 'Antarctica/Casey'), ('Africa/Kinshasa', 'Africa/Kinshasa'), ('America/Indiana/Indianapolis', 'America/Indiana/Indianapolis'), ('Europe/Isle_of_Man', 'Europe/Isle_of_Man'), ('Africa/El_Aaiun', 'Africa/El_Aaiun'), ('Africa/Niamey', 'Africa/Niamey'), ('Australia/West', 'Australia/West'), ('Asia/Harbin', 'Asia/Harbin'), ('Indian/Chagos', 'Indian/Chagos'), ('America/Juneau', 'America/Juneau'), ('Atlantic/Bermuda', 'Atlantic/Bermuda'), ('Asia/Kolkata', 'Asia/Kolkata'), ('Asia/Phnom_Penh', 'Asia/Phnom_Penh'), ('Pacific/Samoa', 'Pacific/Samoa'), ('Canada/Mountain', 'Canada/Mountain'), ('Kwajalein', 'Kwajalein'), ('Europe/Zaporozhye', 'Europe/Zaporozhye'), ('Asia/Kuala_Lumpur', 'Asia/Kuala_Lumpur'), ('Pacific/Kosrae', 'Pacific/Kosrae'), ('Europe/Saratov', 'Europe/Saratov'), ('Asia/Jerusalem', 'Asia/Jerusalem'), ('Europe/Rome', 'Europe/Rome'), ('Asia/Chungking', 'Asia/Chungking'), ('America/Vancouver', 'America/Vancouver'), ('America/Atka', 'America/Atka'), ('Europe/Malta', 'Europe/Malta'), ('Asia/Dili', 'Asia/Dili'), ('America/St_Kitts', 'America/St_Kitts'), ('America/Guayaquil', 'America/Guayaquil'), ('Antarctica/McMurdo', 'Antarctica/McMurdo'), ('Etc/GMT+9', 'Etc/GMT+9'), ('America/Argentina/Jujuy', 'America/Argentina/Jujuy'), ('Portugal', 'Portugal'), ('America/Cambridge_Bay', 'America/Cambridge_Bay'), ('America/Rosario', 'America/Rosario'), ('Europe/Brussels', 'Europe/Brussels'), ('Israel', 'Israel'), ('America/Thule', 'America/Thule'), ('Europe/Tiraspol', 'Europe/Tiraspol'), ('America/Argentina/ComodRivadavia', 'America/Argentina/ComodRivadavia'), ('America/Mendoza', 'America/Mendoza'), ('Etc/GMT-10', 'Etc/GMT-10'), ('Australia/Broken_Hill', 'Australia/Broken_Hill'), ('Atlantic/South_Georgia', 'Atlantic/South_Georgia'), ('America/Goose_Bay', 'America/Goose_Bay'), ('America/Rainy_River', 'America/Rainy_River'), ('Iceland', 'Iceland'), ('Asia/Hebron', 'Asia/Hebron'), ('Europe/San_Marino', 'Europe/San_Marino'), ('Etc/GMT0', 'Etc/GMT0'), ('Etc/GMT-12', 'Etc/GMT-12'), ('US/Mountain', 'US/Mountain'), ('America/Marigot', 'America/Marigot'), ('Pacific/Guam', 'Pacific/Guam'), ('Antarctica/Troll', 'Antarctica/Troll'), ('America/Indiana/Tell_City', 'America/Indiana/Tell_City'), ('Europe/Tirane', 'Europe/Tirane'), ('Asia/Oral', 'Asia/Oral'), ('Europe/Bratislava', 'Europe/Bratislava'), ('GMT0', 'GMT0'), ('Europe/Dublin', 'Europe/Dublin'), ('America/Kralendijk', 'America/Kralendijk'), ('America/Fort_Wayne', 'America/Fort_Wayne'), ('Asia/Jakarta', 'Asia/Jakarta'), ('Zulu', 'Zulu'), ('Africa/Douala', 'Africa/Douala'), ('America/Mazatlan', 'America/Mazatlan'), ('Egypt', 'Egypt'), ('Brazil/West', 'Brazil/West'), ('Australia/Brisbane', 'Australia/Brisbane'), ('America/Cayman', 'America/Cayman'), ('America/Guyana', 'America/Guyana'), ('Pacific/Saipan', 'Pacific/Saipan'), ('Atlantic/Stanley', 'Atlantic/Stanley'), ('Europe/Volgograd', 'Europe/Volgograd'), ('America/North_Dakota/Center', 'America/North_Dakota/Center'), ('America/Yakutat', 'America/Yakutat'), ('America/Catamarca', 'America/Catamarca'), ('Antarctica/Davis', 'Antarctica/Davis'), ('Chile/Continental', 'Chile/Continental'), ('America/Curacao', 'America/Curacao'), ('Asia/Vladivostok', 'Asia/Vladivostok'), ('Asia/Khandyga', 'Asia/Khandyga'), ('Asia/Sakhalin', 'Asia/Sakhalin'), ('Asia/Bishkek', 'Asia/Bishkek'), ('Asia/Kuwait', 'Asia/Kuwait'), ('Pacific/Pitcairn', 'Pacific/Pitcairn'), ('Chile/EasterIsland', 'Chile/EasterIsland'), ('Atlantic/Faeroe', 'Atlantic/Faeroe'), ('US/Indiana-Starke', 'US/Indiana-Starke'), ('America/Bogota', 'America/Bogota'), ('Pacific/Kiritimati', 'Pacific/Kiritimati'), ('Indian/Reunion', 'Indian/Reunion'), ('America/Glace_Bay', 'America/Glace_Bay'), ('US/Eastern', 'US/Eastern'), ('Antarctica/DumontDUrville', 'Antarctica/DumontDUrville'), ('EST5EDT', 'EST5EDT'), ('America/Knox_IN', 'America/Knox_IN'), ('America/Argentina/Rio_Gallegos', 'America/Argentina/Rio_Gallegos'), ('Europe/Copenhagen', 'Europe/Copenhagen'), ('Asia/Muscat', 'Asia/Muscat'), ('America/El_Salvador', 'America/El_Salvador'), ('Europe/Istanbul', 'Europe/Istanbul'), ('Asia/Ashgabat', 'Asia/Ashgabat'), ('America/Danmarkshavn', 'America/Danmarkshavn'), ('Europe/Kaliningrad', 'Europe/Kaliningrad'), ('America/Thunder_Bay', 'America/Thunder_Bay'), ('Asia/Karachi', 'Asia/Karachi'), ('America/Chihuahua', 'America/Chihuahua'), ('EST', 'EST'), ('Asia/Colombo', 'Asia/Colombo'), ('Australia/Adelaide', 'Australia/Adelaide'), ('UTC', 'UTC'), ('Asia/Kashgar', 'Asia/Kashgar'), ('Asia/Shanghai', 'Asia/Shanghai'), ('Africa/Casablanca', 'Africa/Casablanca'), ('Europe/Sarajevo', 'Europe/Sarajevo'), ('America/Regina', 'America/Regina'), ('Europe/Simferopol', 'Europe/Simferopol'), ('Canada/Newfoundland', 'Canada/Newfoundland'), ('Asia/Tel_Aviv', 'Asia/Tel_Aviv'), ('UCT', 'UCT'), ('Indian/Comoro', 'Indian/Comoro'), ('Brazil/East', 'Brazil/East'), ('America/Toronto', 'America/Toronto'), ('Asia/Qostanay', 'Asia/Qostanay'), ('America/Detroit', 'America/Detroit'), ('US/Samoa', 'US/Samoa'), ('America/Anchorage', 'America/Anchorage'), ('Europe/Ulyanovsk', 'Europe/Ulyanovsk'), ('Europe/Jersey', 'Europe/Jersey'), ('Pacific/Truk', 'Pacific/Truk'), ('Asia/Ust-Nera', 'Asia/Ust-Nera'), ('America/Argentina/La_Rioja', 'America/Argentina/La_Rioja'), ('Asia/Magadan', 'Asia/Magadan'), ('America/Shiprock', 'America/Shiprock'), ('America/Lower_Princes', 'America/Lower_Princes'), ('Europe/Astrakhan', 'Europe/Astrakhan'), ('Etc/GMT-5', 'Etc/GMT-5'), ('America/Bahia_Banderas', 'America/Bahia_Banderas'), ('Asia/Istanbul', 'Asia/Istanbul'), ('Europe/Bucharest', 'Europe/Bucharest'), ('America/Argentina/San_Luis', 'America/Argentina/San_Luis'), ('Asia/Qyzylorda', 'Asia/Qyzylorda'), ('GMT', 'GMT'), ('Pacific/Port_Moresby', 'Pacific/Port_Moresby'), ('America/St_Vincent', 'America/St_Vincent'), ('Jamaica', 'Jamaica'), ('CET', 'CET'), ('America/Creston', 'America/Creston'), ('Africa/Luanda', 'Africa/Luanda'), ('Africa/Libreville', 'Africa/Libreville'), ('Asia/Almaty', 'Asia/Almaty'), ('America/Boa_Vista', 'America/Boa_Vista'), ('America/Virgin', 'America/Virgin'), ('Pacific/Yap', 'Pacific/Yap'), ('WET', 'WET'), ('Asia/Riyadh', 'Asia/Riyadh'), ('America/Argentina/Mendoza', 'America/Argentina/Mendoza'), ('Asia/Samarkand', 'Asia/Samarkand'), ('Africa/Brazzaville', 'Africa/Brazzaville'), ('America/Santa_Isabel', 'America/Santa_Isabel'), ('America/North_Dakota/New_Salem', 'America/North_Dakota/New_Salem'), ('Africa/Tunis', 'Africa/Tunis'), ('America/Port_of_Spain', 'America/Port_of_Spain'), ('Etc/GMT+10', 'Etc/GMT+10'), ('America/Antigua', 'America/Antigua'), ('Africa/Gaborone', 'Africa/Gaborone'), ('Asia/Tokyo', 'Asia/Tokyo'), ('Etc/GMT+4', 'Etc/GMT+4'), ('America/Mexico_City', 'America/Mexico_City'), ('Asia/Manila', 'Asia/Manila'), ('Africa/Sao_Tome', 'Africa/Sao_Tome'), ('America/Pangnirtung', 'America/Pangnirtung'), ('Pacific/Norfolk', 'Pacific/Norfolk'), ('Europe/Kiev', 'Europe/Kiev'), ('Pacific/Tongatapu', 'Pacific/Tongatapu'), ('Europe/Paris', 'Europe/Paris'), ('Atlantic/Azores', 'Atlantic/Azores'), ('Pacific/Ponape', 'Pacific/Ponape'), ('Pacific/Wake', 'Pacific/Wake'), ('Asia/Omsk', 'Asia/Omsk'), ('Asia/Aqtau', 'Asia/Aqtau'), ('Europe/Busingen', 'Europe/Busingen'), ('America/St_Lucia', 'America/St_Lucia'), ('Etc/UTC', 'Etc/UTC'), ('Etc/GMT-11', 'Etc/GMT-11'), ('Pacific/Kanton', 'Pacific/Kanton'), ('Pacific/Rarotonga', 'Pacific/Rarotonga'), ('Turkey', 'Turkey'), ('Asia/Ulaanbaatar', 'Asia/Ulaanbaatar'), ('Africa/Maputo', 'Africa/Maputo'), ('Asia/Katmandu', 'Asia/Katmandu'), ('Europe/Guernsey', 'Europe/Guernsey'), ('Pacific/Pago_Pago', 'Pacific/Pago_Pago'), ('America/Jamaica', 'America/Jamaica'), ('Pacific/Tarawa', 'Pacific/Tarawa'), ('America/Argentina/Catamarca', 'America/Argentina/Catamarca'), ('Australia/Canberra', 'Australia/Canberra'), ('Pacific/Wallis', 'Pacific/Wallis'), ('Asia/Pyongyang', 'Asia/Pyongyang'), ('America/Boise', 'America/Boise'), ('Atlantic/Canary', 'Atlantic/Canary'), ('Asia/Macao', 'Asia/Macao'), ('Pacific/Tahiti', 'Pacific/Tahiti'), ('America/Iqaluit', 'America/Iqaluit'), ('America/New_York', 'America/New_York'), ('Africa/Monrovia', 'Africa/Monrovia'), ('Asia/Seoul', 'Asia/Seoul'), ('Africa/Blantyre', 'Africa/Blantyre'), ('Australia/North', 'Australia/North'), ('America/Dominica', 'America/Dominica'), ('Asia/Hong_Kong', 'Asia/Hong_Kong'), ('America/Tortola', 'America/Tortola'), ('Factory', 'Factory'), ('Brazil/Acre', 'Brazil/Acre'), ('Etc/GMT+3', 'Etc/GMT+3'), ('Pacific/Gambier', 'Pacific/Gambier'), ('Asia/Macau', 'Asia/Macau'), ('America/Panama', 'America/Panama'), ('America/Tijuana', 'America/Tijuana'), ('Antarctica/Rothera', 'Antarctica/Rothera'), ('Etc/GMT-13', 'Etc/GMT-13'), ('Europe/Andorra', 'Europe/Andorra'), ('Canada/Eastern', 'Canada/Eastern'), ('America/Montevideo', 'America/Montevideo'), ('Europe/Warsaw', 'Europe/Warsaw'), ('Etc/GMT-2', 'Etc/GMT-2'), ('Africa/Conakry', 'Africa/Conakry'), ('Asia/Ashkhabad', 'Asia/Ashkhabad'), ('Asia/Dacca', 'Asia/Dacca'), ('Africa/Abidjan', 'Africa/Abidjan'), ('America/Costa_Rica', 'America/Costa_Rica'), ('Africa/Kigali', 'Africa/Kigali'), ('Asia/Srednekolymsk', 'Asia/Srednekolymsk'), ('Asia/Atyrau', 'Asia/Atyrau'), ('Australia/Darwin', 'Australia/Darwin'), ('MST', 'MST'), ('Etc/GMT+12', 'Etc/GMT+12'), ('Europe/Uzhgorod', 'Europe/Uzhgorod'), ('America/Hermosillo', 'America/Hermosillo'), ('Europe/Minsk', 'Europe/Minsk'), ('GMT+0', 'GMT+0'), ('America/Indianapolis', 'America/Indianapolis'), ('Europe/Vilnius', 'Europe/Vilnius'), ('Etc/GMT+1', 'Etc/GMT+1'), ('NZ', 'NZ'), ('Africa/Freetown', 'Africa/Freetown'), ('Indian/Mahe', 'Indian/Mahe'), ('America/Argentina/Tucuman', 'America/Argentina/Tucuman'), ('Asia/Beirut', 'Asia/Beirut'), ('GMT-0', 'GMT-0'), ('Asia/Yangon', 'Asia/Yangon'), ('Pacific/Kwajalein', 'Pacific/Kwajalein'), ('Atlantic/Madeira', 'Atlantic/Madeira'), ('Africa/Maseru', 'Africa/Maseru'), ('Europe/London', 'Europe/London'), ('Australia/Lindeman', 'Australia/Lindeman'), ('Etc/GMT+2', 'Etc/GMT+2'), ('Australia/Eucla', 'Australia/Eucla'), ('Africa/Bamako', 'Africa/Bamako'), ('Greenwich', 'Greenwich'), ('America/Louisville', 'America/Louisville'), ('America/Los_Angeles', 'America/Los_Angeles'), ('Europe/Riga', 'Europe/Riga'), ('Pacific/Nauru', 'Pacific/Nauru'), ('America/Indiana/Marengo', 'America/Indiana/Marengo'), ('Africa/Dakar', 'Africa/Dakar'), ('Asia/Ulan_Bator', 'Asia/Ulan_Bator'), ('America/Dawson', 'America/Dawson'), ('Asia/Baku', 'Asia/Baku'), ('Pacific/Guadalcanal', 'Pacific/Guadalcanal'), ('Etc/GMT-4', 'Etc/GMT-4'), ('Africa/Nouakchott', 'Africa/Nouakchott'), ('Etc/GMT-8', 'Etc/GMT-8'), ('PRC', 'PRC'), ('Africa/Lusaka', 'Africa/Lusaka'), ('Asia/Tashkent', 'Asia/Tashkent'), ('Indian/Maldives', 'Indian/Maldives'), ('Etc/GMT-0', 'Etc/GMT-0'), ('Africa/Djibouti', 'Africa/Djibouti'), ('Australia/Sydney', 'Australia/Sydney'), ('America/Nuuk', 'America/Nuuk'), ('Pacific/Palau', 'Pacific/Palau'), ('America/Whitehorse', 'America/Whitehorse'), ('America/Nipigon', 'America/Nipigon'), ('America/Argentina/San_Juan', 'America/Argentina/San_Juan'), ('Antarctica/Macquarie', 'Antarctica/Macquarie'), ('Pacific/Fakaofo', 'Pacific/Fakaofo'), ('EET', 'EET'), ('America/Phoenix', 'America/Phoenix'), ('Etc/GMT-6', 'Etc/GMT-6'), ('W-SU', 'W-SU'), ('America/Porto_Acre', 'America/Porto_Acre'), ('Asia/Rangoon', 'Asia/Rangoon'), ('Indian/Kerguelen', 'Indian/Kerguelen'), ('Europe/Vaduz', 'Europe/Vaduz'), ('America/Noronha', 'America/Noronha'), ('Navajo', 'Navajo'), ('Asia/Kamchatka', 'Asia/Kamchatka'), ('America/Paramaribo', 'America/Paramaribo'), ('Europe/Tallinn', 'Europe/Tallinn'), ('Brazil/DeNoronha', 'Brazil/DeNoronha'), ('America/Tegucigalpa', 'America/Tegucigalpa'), ('Europe/Kyiv', 'Europe/Kyiv'), ('Europe/Sofia', 'Europe/Sofia'), ('Pacific/Majuro', 'Pacific/Majuro'), ('Etc/GMT+8', 'Etc/GMT+8'), ('Atlantic/Reykjavik', 'Atlantic/Reykjavik'), ('Etc/GMT+5', 'Etc/GMT+5'), ('America/Martinique', 'America/Martinique'), ('America/Inuvik', 'America/Inuvik'), ('America/La_Paz', 'America/La_Paz'), ('Asia/Irkutsk', 'Asia/Irkutsk'), ('America/St_Barthelemy', 'America/St_Barthelemy'), ('Europe/Skopje', 'Europe/Skopje'), ('Canada/Saskatchewan', 'Canada/Saskatchewan'), ('Europe/Vatican', 'Europe/Vatican'), ('Asia/Novokuznetsk', 'Asia/Novokuznetsk'), ('Europe/Berlin', 'Europe/Berlin'), ('Australia/Yancowinna', 'Australia/Yancowinna'), ('America/Indiana/Winamac', 'America/Indiana/Winamac'), ('Africa/Lagos', 'Africa/Lagos'), ('NZ-CHAT', 'NZ-CHAT'), ('Etc/Greenwich', 'Etc/Greenwich'), ('Europe/Zurich', 'Europe/Zurich'), ('Africa/Ceuta', 'Africa/Ceuta'), ('America/St_Johns', 'America/St_Johns'), ('America/Campo_Grande', 'America/Campo_Grande'), ('US/Central', 'US/Central'), ('America/Belem', 'America/Belem'), ('America/Argentina/Buenos_Aires', 'America/Argentina/Buenos_Aires'), ('Atlantic/Jan_Mayen', 'Atlantic/Jan_Mayen'), ('Antarctica/Mawson', 'Antarctica/Mawson'), ('Asia/Kuching', 'Asia/Kuching'), ('America/Bahia', 'America/Bahia'), ('Asia/Yerevan', 'Asia/Yerevan'), ('Asia/Yekaterinburg', 'Asia/Yekaterinburg'), ('Pacific/Chuuk', 'Pacific/Chuuk'), ('US/Pacific', 'US/Pacific'), ('America/Lima', 'America/Lima'), ('America/Matamoros', 'America/Matamoros'), ('Africa/Tripoli', 'Africa/Tripoli'), ('America/Santarem', 'America/Santarem'), ('Pacific/Marquesas', 'Pacific/Marquesas'), ('America/Buenos_Aires', 'America/Buenos_Aires'), ('Africa/Khartoum', 'Africa/Khartoum'), ('Asia/Gaza', 'Asia/Gaza'), ('Etc/Universal', 'Etc/Universal'), ('America/Menominee', 'America/Menominee'), ('MST7MDT', 'MST7MDT'), ('Australia/Melbourne', 'Australia/Melbourne'), ('Asia/Ujung_Pandang', 'Asia/Ujung_Pandang'), ('America/Metlakatla', 'America/Metlakatla'), ('Asia/Amman', 'Asia/Amman'), ('Asia/Jayapura', 'Asia/Jayapura'), ('Asia/Brunei', 'Asia/Brunei'), ('Asia/Dubai', 'Asia/Dubai'), ('America/St_Thomas', 'America/St_Thomas'), ('Europe/Athens', 'Europe/Athens'), ('America/Caracas', 'America/Caracas'), ('Atlantic/Faroe', 'Atlantic/Faroe'), ('America/Ensenada', 'America/Ensenada'), ('ROK', 'ROK'), ('Europe/Stockholm', 'Europe/Stockholm'), ('Universal', 'Universal'), ('Europe/Helsinki', 'Europe/Helsinki'), ('Antarctica/Vostok', 'Antarctica/Vostok'), ('America/Recife', 'America/Recife'), ('Europe/Ljubljana', 'Europe/Ljubljana'), ('Europe/Luxembourg', 'Europe/Luxembourg'), ('Australia/South', 'Australia/South'), ('Pacific/Enderbury', 'Pacific/Enderbury'), ('Asia/Kabul', 'Asia/Kabul'), ('Asia/Saigon', 'Asia/Saigon'), ('US/Alaska', 'US/Alaska'), ('America/Fort_Nelson', 'America/Fort_Nelson'), ('Antarctica/Syowa', 'Antarctica/Syowa'), ('America/Cordoba', 'America/Cordoba'), ('America/Moncton', 'America/Moncton'), ('Indian/Christmas', 'Indian/Christmas'), ('Europe/Prague', 'Europe/Prague'), ('America/Montreal', 'America/Montreal'), ('Africa/Ndjamena', 'Africa/Ndjamena'), ('America/Punta_Arenas', 'America/Punta_Arenas'), ('America/Santo_Domingo', 'America/Santo_Domingo'), ('Etc/GMT+6', 'Etc/GMT+6'), ('America/Indiana/Vevay', 'America/Indiana/Vevay'), ('Libya', 'Libya'), ('Africa/Asmara', 'Africa/Asmara'), ('Europe/Podgorica', 'Europe/Podgorica'), ('Africa/Lubumbashi', 'Africa/Lubumbashi'), ('America/Puerto_Rico', 'America/Puerto_Rico'), ('Asia/Vientiane', 'Asia/Vientiane'), ('Asia/Yakutsk', 'Asia/Yakutsk'), ('America/Nassau', 'America/Nassau'), ('Asia/Hovd', 'Asia/Hovd'), ('Asia/Bangkok', 'Asia/Bangkok'), ('Pacific/Noumea', 'Pacific/Noumea'), ('Europe/Samara', 'Europe/Samara'), ('GB-Eire', 'GB-Eire'), ('Asia/Aqtobe', 'Asia/Aqtobe'), ('America/Yellowknife', 'America/Yellowknife'), ('Africa/Mogadishu', 'Africa/Mogadishu'), ('Canada/Pacific', 'Canada/Pacific'), ('America/Eirunepe', 'America/Eirunepe'), ('America/Winnipeg', 'America/Winnipeg'), ('America/Port-au-Prince', 'America/Port-au-Prince'), ('Australia/NSW', 'Australia/NSW'), ('Asia/Urumqi', 'Asia/Urumqi'), ('Indian/Cocos', 'Indian/Cocos'), ('America/Godthab', 'America/Godthab'), ('Asia/Thimbu', 'Asia/Thimbu'), ('Asia/Barnaul', 'Asia/Barnaul'), ('America/Kentucky/Monticello', 'America/Kentucky/Monticello'), ('America/Chicago', 'America/Chicago'), ('America/Blanc-Sablon', 'America/Blanc-Sablon'), ('Africa/Timbuktu', 'Africa/Timbuktu'), ('America/Indiana/Knox', 'America/Indiana/Knox'), ('Iran', 'Iran'), ('America/Grand_Turk', 'America/Grand_Turk'), ('America/Jujuy', 'America/Jujuy'), ('Etc/Zulu', 'Etc/Zulu'), ('Pacific/Apia', 'Pacific/Apia'), ('Pacific/Bougainville', 'Pacific/Bougainville'), ('Atlantic/St_Helena', 'Atlantic/St_Helena'), ('Africa/Addis_Ababa', 'Africa/Addis_Ababa'), ('Africa/Accra', 'Africa/Accra'), ('Asia/Chita', 'Asia/Chita'), ('Asia/Aden', 'Asia/Aden'), ('America/Santiago', 'America/Santiago'), ('Europe/Mariehamn', 'Europe/Mariehamn'), ('Asia/Tbilisi', 'Asia/Tbilisi'), ('Antarctica/Palmer', 'Antarctica/Palmer'), ('Europe/Zagreb', 'Europe/Zagreb'), ('America/Belize', 'America/Belize'), ('ROC', 'ROC'), ('Japan', 'Japan'), ('Africa/Ouagadougou', 'Africa/Ouagadougou'), ('Africa/Bissau', 'Africa/Bissau'), ('America/Resolute', 'America/Resolute'), ('Africa/Malabo', 'Africa/Malabo'), ('Pacific/Funafuti', 'Pacific/Funafuti'), ('Africa/Algiers', 'Africa/Algiers'), ('Pacific/Honolulu', 'Pacific/Honolulu'), ('America/Swift_Current', 'America/Swift_Current'), ('Europe/Belfast', 'Europe/Belfast'), ('Pacific/Auckland', 'Pacific/Auckland'), ('Atlantic/Cape_Verde', 'Atlantic/Cape_Verde'), ('Mexico/BajaSur', 'Mexico/BajaSur'), ('Australia/Currie', 'Australia/Currie'), ('Asia/Thimphu', 'Asia/Thimphu'), ('Asia/Baghdad', 'Asia/Baghdad'), ('US/Hawaii', 'US/Hawaii'), ('America/Argentina/Salta', 'America/Argentina/Salta'), ('America/Maceio', 'America/Maceio'), ('Europe/Vienna', 'Europe/Vienna'), ('Asia/Tehran', 'Asia/Tehran'), ('Australia/Lord_Howe', 'Australia/Lord_Howe'), ('Asia/Krasnoyarsk', 'Asia/Krasnoyarsk'), ('America/Managua', 'America/Managua'), ('America/Cayenne', 'America/Cayenne'), ('Australia/Tasmania', 'Australia/Tasmania'), ('America/Aruba', 'America/Aruba'), ('Europe/Monaco', 'Europe/Monaco'), ('Asia/Singapore', 'Asia/Singapore'), ('Pacific/Efate', 'Pacific/Efate'), ('Africa/Kampala', 'Africa/Kampala'), ('Europe/Belgrade', 'Europe/Belgrade'), ('Asia/Pontianak', 'Asia/Pontianak'), ('Europe/Gibraltar', 'Europe/Gibraltar'), ('Canada/Central', 'Canada/Central'), ('Europe/Oslo', 'Europe/Oslo'), ('Etc/GMT-1', 'Etc/GMT-1'), ('America/Sao_Paulo', 'America/Sao_Paulo'), ('America/Guatemala', 'America/Guatemala'), ('Africa/Juba', 'Africa/Juba'), ('Africa/Bujumbura', 'Africa/Bujumbura'), ('Africa/Johannesburg', 'Africa/Johannesburg'), ('America/Merida', 'America/Merida'), ('America/Araguaina', 'America/Araguaina'), ('Canada/Atlantic', 'Canada/Atlantic'), ('Asia/Nicosia', 'Asia/Nicosia'), ('Australia/Queensland', 'Australia/Queensland'), ('Asia/Chongqing', 'Asia/Chongqing'), ('Pacific/Johnston', 'Pacific/Johnston'), ('US/Arizona', 'US/Arizona'), ('Europe/Kirov', 'Europe/Kirov'), ('PST8PDT', 'PST8PDT'), ('Canada/Yukon', 'Canada/Yukon'), ('America/Barbados', 'America/Barbados'), ('Europe/Moscow', 'Europe/Moscow'), ('GB', 'GB'), ('Pacific/Chatham', 'Pacific/Chatham'), ('Asia/Choibalsan', 'Asia/Choibalsan'), ('America/Indiana/Vincennes', 'America/Indiana/Vincennes'), ('America/Denver', 'America/Denver'), ('Asia/Kathmandu', 'Asia/Kathmandu'), ('America/Argentina/Cordoba', 'America/Argentina/Cordoba'), ('Asia/Novosibirsk', 'Asia/Novosibirsk'), ('America/Dawson_Creek', 'America/Dawson_Creek'), ('Australia/LHI', 'Australia/LHI'), ('Africa/Dar_es_Salaam', 'Africa/Dar_es_Salaam'), ('Indian/Mauritius', 'Indian/Mauritius'), ('Eire', 'Eire'), ('Etc/GMT-3', 'Etc/GMT-3'), ('America/Scoresbysund', 'America/Scoresbysund'), ('Africa/Asmera', 'Africa/Asmera'), ('Mexico/BajaNorte', 'Mexico/BajaNorte'), ('America/Indiana/Petersburg', 'America/Indiana/Petersburg'), ('Pacific/Galapagos', 'Pacific/Galapagos'), ('Arctic/Longyearbyen', 'Arctic/Longyearbyen'), ('MET', 'MET'), ('America/Edmonton', 'America/Edmonton'), ('America/Cancun', 'America/Cancun'), ('Asia/Damascus', 'Asia/Damascus'), ('America/Nome', 'America/Nome'), ('Pacific/Easter', 'Pacific/Easter'), ('America/Asuncion', 'America/Asuncion'), ('Africa/Windhoek', 'Africa/Windhoek'), ('Etc/GMT+11', 'Etc/GMT+11'), ('Pacific/Niue', 'Pacific/Niue'), ('Africa/Bangui', 'Africa/Bangui'), ('Africa/Porto-Novo', 'Africa/Porto-Novo'), ('America/Monterrey', 'America/Monterrey'), ('Europe/Budapest', 'Europe/Budapest'), ('America/Adak', 'America/Adak'), ('Pacific/Pohnpei', 'Pacific/Pohnpei'), ('America/Cuiaba', 'America/Cuiaba'), ('America/Kentucky/Louisville', 'America/Kentucky/Louisville')], default='Asia/Kolkata', max_length=50, verbose_name='Time zone'),
        ),
    ]
