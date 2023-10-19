# Generated by Django 4.2.6 on 2023-10-17 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creme_core', '0017_alter_user_time_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='time_zone',
            field=models.CharField(choices=[('Etc/GMT', 'Etc/GMT'), ('America/Metlakatla', 'America/Metlakatla'), ('Indian/Mahe', 'Indian/Mahe'), ('America/Jamaica', 'America/Jamaica'), ('Europe/Warsaw', 'Europe/Warsaw'), ('Pacific/Palau', 'Pacific/Palau'), ('Africa/Sao_Tome', 'Africa/Sao_Tome'), ('America/Marigot', 'America/Marigot'), ('Asia/Qostanay', 'Asia/Qostanay'), ('Egypt', 'Egypt'), ('Europe/Oslo', 'Europe/Oslo'), ('US/Indiana-Starke', 'US/Indiana-Starke'), ('America/Virgin', 'America/Virgin'), ('America/Bogota', 'America/Bogota'), ('America/St_Vincent', 'America/St_Vincent'), ('Asia/Qyzylorda', 'Asia/Qyzylorda'), ('Asia/Pyongyang', 'Asia/Pyongyang'), ('MET', 'MET'), ('Africa/Banjul', 'Africa/Banjul'), ('Africa/Niamey', 'Africa/Niamey'), ('Pacific/Guam', 'Pacific/Guam'), ('America/Montreal', 'America/Montreal'), ('Europe/Tiraspol', 'Europe/Tiraspol'), ('EET', 'EET'), ('Hongkong', 'Hongkong'), ('Asia/Choibalsan', 'Asia/Choibalsan'), ('America/Vancouver', 'America/Vancouver'), ('Indian/Mauritius', 'Indian/Mauritius'), ('America/Moncton', 'America/Moncton'), ('Asia/Macau', 'Asia/Macau'), ('America/Juneau', 'America/Juneau'), ('Australia/Victoria', 'Australia/Victoria'), ('Asia/Dili', 'Asia/Dili'), ('GB-Eire', 'GB-Eire'), ('Etc/GMT+9', 'Etc/GMT+9'), ('Pacific/Tarawa', 'Pacific/Tarawa'), ('Asia/Jakarta', 'Asia/Jakarta'), ('Europe/Zurich', 'Europe/Zurich'), ('UTC', 'UTC'), ('America/New_York', 'America/New_York'), ('America/Shiprock', 'America/Shiprock'), ('Asia/Ujung_Pandang', 'Asia/Ujung_Pandang'), ('Asia/Srednekolymsk', 'Asia/Srednekolymsk'), ('Asia/Novosibirsk', 'Asia/Novosibirsk'), ('Europe/Dublin', 'Europe/Dublin'), ('America/Havana', 'America/Havana'), ('Africa/Harare', 'Africa/Harare'), ('America/North_Dakota/New_Salem', 'America/North_Dakota/New_Salem'), ('America/Toronto', 'America/Toronto'), ('Asia/Hebron', 'Asia/Hebron'), ('America/Matamoros', 'America/Matamoros'), ('America/Nuuk', 'America/Nuuk'), ('Pacific/Chuuk', 'Pacific/Chuuk'), ('Asia/Thimbu', 'Asia/Thimbu'), ('America/Dominica', 'America/Dominica'), ('Pacific/Funafuti', 'Pacific/Funafuti'), ('PST8PDT', 'PST8PDT'), ('W-SU', 'W-SU'), ('Pacific/Easter', 'Pacific/Easter'), ('UCT', 'UCT'), ('Pacific/Pitcairn', 'Pacific/Pitcairn'), ('Asia/Vientiane', 'Asia/Vientiane'), ('Asia/Kolkata', 'Asia/Kolkata'), ('Europe/London', 'Europe/London'), ('America/Aruba', 'America/Aruba'), ('Europe/Budapest', 'Europe/Budapest'), ('Indian/Chagos', 'Indian/Chagos'), ('Canada/Central', 'Canada/Central'), ('Europe/Bratislava', 'Europe/Bratislava'), ('Australia/Hobart', 'Australia/Hobart'), ('Asia/Rangoon', 'Asia/Rangoon'), ('America/Argentina/Tucuman', 'America/Argentina/Tucuman'), ('Asia/Sakhalin', 'Asia/Sakhalin'), ('US/Alaska', 'US/Alaska'), ('America/Port-au-Prince', 'America/Port-au-Prince'), ('Europe/Sarajevo', 'Europe/Sarajevo'), ('Etc/GMT+4', 'Etc/GMT+4'), ('Asia/Thimphu', 'Asia/Thimphu'), ('Etc/GMT-5', 'Etc/GMT-5'), ('Pacific/Truk', 'Pacific/Truk'), ('America/Nome', 'America/Nome'), ('Asia/Katmandu', 'Asia/Katmandu'), ('Asia/Pontianak', 'Asia/Pontianak'), ('US/Mountain', 'US/Mountain'), ('US/Hawaii', 'US/Hawaii'), ('Iran', 'Iran'), ('America/La_Paz', 'America/La_Paz'), ('Pacific/Chatham', 'Pacific/Chatham'), ('Africa/Nairobi', 'Africa/Nairobi'), ('EST', 'EST'), ('America/Curacao', 'America/Curacao'), ('Pacific/Majuro', 'Pacific/Majuro'), ('Europe/Malta', 'Europe/Malta'), ('Atlantic/Bermuda', 'Atlantic/Bermuda'), ('Europe/Vaduz', 'Europe/Vaduz'), ('America/Eirunepe', 'America/Eirunepe'), ('America/Barbados', 'America/Barbados'), ('Asia/Karachi', 'Asia/Karachi'), ('Asia/Hovd', 'Asia/Hovd'), ('NZ-CHAT', 'NZ-CHAT'), ('America/Yellowknife', 'America/Yellowknife'), ('Antarctica/Rothera', 'Antarctica/Rothera'), ('Europe/Belfast', 'Europe/Belfast'), ('Asia/Krasnoyarsk', 'Asia/Krasnoyarsk'), ('Africa/Djibouti', 'Africa/Djibouti'), ('Antarctica/Palmer', 'Antarctica/Palmer'), ('America/Port_of_Spain', 'America/Port_of_Spain'), ('Asia/Irkutsk', 'Asia/Irkutsk'), ('Indian/Maldives', 'Indian/Maldives'), ('Australia/LHI', 'Australia/LHI'), ('Atlantic/Faroe', 'Atlantic/Faroe'), ('Asia/Dubai', 'Asia/Dubai'), ('Africa/El_Aaiun', 'Africa/El_Aaiun'), ('America/Lower_Princes', 'America/Lower_Princes'), ('Africa/Mogadishu', 'Africa/Mogadishu'), ('America/Yakutat', 'America/Yakutat'), ('America/Creston', 'America/Creston'), ('America/Belem', 'America/Belem'), ('Cuba', 'Cuba'), ('America/Fortaleza', 'America/Fortaleza'), ('Etc/GMT+5', 'Etc/GMT+5'), ('America/Grand_Turk', 'America/Grand_Turk'), ('America/Indianapolis', 'America/Indianapolis'), ('America/Anguilla', 'America/Anguilla'), ('America/Montserrat', 'America/Montserrat'), ('Africa/Malabo', 'Africa/Malabo'), ('Iceland', 'Iceland'), ('America/Miquelon', 'America/Miquelon'), ('Pacific/Gambier', 'Pacific/Gambier'), ('Indian/Christmas', 'Indian/Christmas'), ('Canada/Yukon', 'Canada/Yukon'), ('Brazil/West', 'Brazil/West'), ('America/Catamarca', 'America/Catamarca'), ('Etc/GMT-6', 'Etc/GMT-6'), ('Europe/Madrid', 'Europe/Madrid'), ('Navajo', 'Navajo'), ('America/St_Lucia', 'America/St_Lucia'), ('Antarctica/DumontDUrville', 'Antarctica/DumontDUrville'), ('Europe/Helsinki', 'Europe/Helsinki'), ('Pacific/Midway', 'Pacific/Midway'), ('Etc/GMT+2', 'Etc/GMT+2'), ('Canada/Eastern', 'Canada/Eastern'), ('Asia/Taipei', 'Asia/Taipei'), ('Antarctica/Troll', 'Antarctica/Troll'), ('Etc/GMT-1', 'Etc/GMT-1'), ('Australia/Tasmania', 'Australia/Tasmania'), ('America/Argentina/San_Juan', 'America/Argentina/San_Juan'), ('Pacific/Wake', 'Pacific/Wake'), ('Pacific/Efate', 'Pacific/Efate'), ('Africa/Brazzaville', 'Africa/Brazzaville'), ('Brazil/DeNoronha', 'Brazil/DeNoronha'), ('Asia/Bangkok', 'Asia/Bangkok'), ('Pacific/Fakaofo', 'Pacific/Fakaofo'), ('America/Atikokan', 'America/Atikokan'), ('Asia/Jerusalem', 'Asia/Jerusalem'), ('Etc/GMT-3', 'Etc/GMT-3'), ('America/Kralendijk', 'America/Kralendijk'), ('Pacific/Kiritimati', 'Pacific/Kiritimati'), ('Asia/Qatar', 'Asia/Qatar'), ('Europe/Amsterdam', 'Europe/Amsterdam'), ('Asia/Samarkand', 'Asia/Samarkand'), ('GB', 'GB'), ('Etc/GMT-7', 'Etc/GMT-7'), ('America/Louisville', 'America/Louisville'), ('Africa/Douala', 'Africa/Douala'), ('America/Montevideo', 'America/Montevideo'), ('Europe/Nicosia', 'Europe/Nicosia'), ('Atlantic/Stanley', 'Atlantic/Stanley'), ('Asia/Aqtobe', 'Asia/Aqtobe'), ('Africa/Khartoum', 'Africa/Khartoum'), ('Asia/Seoul', 'Asia/Seoul'), ('Asia/Yerevan', 'Asia/Yerevan'), ('Australia/Yancowinna', 'Australia/Yancowinna'), ('Asia/Baghdad', 'Asia/Baghdad'), ('Asia/Dacca', 'Asia/Dacca'), ('Africa/Tunis', 'Africa/Tunis'), ('Africa/Gaborone', 'Africa/Gaborone'), ('Africa/Ceuta', 'Africa/Ceuta'), ('America/Merida', 'America/Merida'), ('Atlantic/Madeira', 'Atlantic/Madeira'), ('America/Winnipeg', 'America/Winnipeg'), ('Australia/Adelaide', 'Australia/Adelaide'), ('Europe/Bucharest', 'Europe/Bucharest'), ('ROK', 'ROK'), ('Kwajalein', 'Kwajalein'), ('America/St_Thomas', 'America/St_Thomas'), ('Europe/Busingen', 'Europe/Busingen'), ('America/Asuncion', 'America/Asuncion'), ('Asia/Macao', 'Asia/Macao'), ('ROC', 'ROC'), ('Pacific/Kanton', 'Pacific/Kanton'), ('America/Inuvik', 'America/Inuvik'), ('America/Argentina/Catamarca', 'America/Argentina/Catamarca'), ('US/Samoa', 'US/Samoa'), ('US/Eastern', 'US/Eastern'), ('America/Boise', 'America/Boise'), ('America/Pangnirtung', 'America/Pangnirtung'), ('Etc/GMT-13', 'Etc/GMT-13'), ('America/Managua', 'America/Managua'), ('Canada/Saskatchewan', 'Canada/Saskatchewan'), ('America/Atka', 'America/Atka'), ('Pacific/Niue', 'Pacific/Niue'), ('America/Santiago', 'America/Santiago'), ('Africa/Conakry', 'Africa/Conakry'), ('HST', 'HST'), ('Atlantic/Azores', 'Atlantic/Azores'), ('Africa/Bangui', 'Africa/Bangui'), ('Asia/Kuching', 'Asia/Kuching'), ('Asia/Ulaanbaatar', 'Asia/Ulaanbaatar'), ('America/Thule', 'America/Thule'), ('Indian/Cocos', 'Indian/Cocos'), ('CST6CDT', 'CST6CDT'), ('America/Mendoza', 'America/Mendoza'), ('Pacific/Pago_Pago', 'Pacific/Pago_Pago'), ('WET', 'WET'), ('Asia/Bahrain', 'Asia/Bahrain'), ('Japan', 'Japan'), ('America/Jujuy', 'America/Jujuy'), ('Africa/Timbuktu', 'Africa/Timbuktu'), ('Antarctica/Vostok', 'Antarctica/Vostok'), ('Africa/Ndjamena', 'Africa/Ndjamena'), ('Asia/Bishkek', 'Asia/Bishkek'), ('Africa/Lome', 'Africa/Lome'), ('Indian/Antananarivo', 'Indian/Antananarivo'), ('Asia/Kabul', 'Asia/Kabul'), ('Asia/Anadyr', 'Asia/Anadyr'), ('Africa/Tripoli', 'Africa/Tripoli'), ('America/Coral_Harbour', 'America/Coral_Harbour'), ('America/Santarem', 'America/Santarem'), ('Pacific/Samoa', 'Pacific/Samoa'), ('Europe/Tirane', 'Europe/Tirane'), ('Pacific/Johnston', 'Pacific/Johnston'), ('Australia/NSW', 'Australia/NSW'), ('US/Arizona', 'US/Arizona'), ('Jamaica', 'Jamaica'), ('Etc/Greenwich', 'Etc/Greenwich'), ('Etc/GMT+3', 'Etc/GMT+3'), ('Canada/Mountain', 'Canada/Mountain'), ('Africa/Freetown', 'Africa/Freetown'), ('Brazil/East', 'Brazil/East'), ('America/Edmonton', 'America/Edmonton'), ('Europe/Guernsey', 'Europe/Guernsey'), ('Asia/Baku', 'Asia/Baku'), ('America/Phoenix', 'America/Phoenix'), ('America/Argentina/Mendoza', 'America/Argentina/Mendoza'), ('Etc/GMT-2', 'Etc/GMT-2'), ('America/Knox_IN', 'America/Knox_IN'), ('Australia/Sydney', 'Australia/Sydney'), ('Antarctica/Davis', 'Antarctica/Davis'), ('America/Resolute', 'America/Resolute'), ('Africa/Kinshasa', 'Africa/Kinshasa'), ('America/Danmarkshavn', 'America/Danmarkshavn'), ('Africa/Dar_es_Salaam', 'Africa/Dar_es_Salaam'), ('Asia/Ho_Chi_Minh', 'Asia/Ho_Chi_Minh'), ('America/Bahia', 'America/Bahia'), ('America/Kentucky/Louisville', 'America/Kentucky/Louisville'), ('America/Argentina/Rio_Gallegos', 'America/Argentina/Rio_Gallegos'), ('Asia/Saigon', 'Asia/Saigon'), ('Europe/Chisinau', 'Europe/Chisinau'), ('Europe/Jersey', 'Europe/Jersey'), ('Asia/Almaty', 'Asia/Almaty'), ('America/Porto_Velho', 'America/Porto_Velho'), ('America/Fort_Wayne', 'America/Fort_Wayne'), ('Asia/Khandyga', 'Asia/Khandyga'), ('Pacific/Tahiti', 'Pacific/Tahiti'), ('Atlantic/Reykjavik', 'Atlantic/Reykjavik'), ('America/Indiana/Knox', 'America/Indiana/Knox'), ('America/Scoresbysund', 'America/Scoresbysund'), ('Asia/Omsk', 'Asia/Omsk'), ('America/Rankin_Inlet', 'America/Rankin_Inlet'), ('Pacific/Wallis', 'Pacific/Wallis'), ('Australia/North', 'Australia/North'), ('Africa/Windhoek', 'Africa/Windhoek'), ('Asia/Tokyo', 'Asia/Tokyo'), ('America/Indiana/Winamac', 'America/Indiana/Winamac'), ('GMT0', 'GMT0'), ('Indian/Comoro', 'Indian/Comoro'), ('Asia/Kamchatka', 'Asia/Kamchatka'), ('America/Lima', 'America/Lima'), ('Israel', 'Israel'), ('America/Cordoba', 'America/Cordoba'), ('Europe/Kirov', 'Europe/Kirov'), ('Atlantic/Jan_Mayen', 'Atlantic/Jan_Mayen'), ('Antarctica/Syowa', 'Antarctica/Syowa'), ('Europe/Zaporozhye', 'Europe/Zaporozhye'), ('Portugal', 'Portugal'), ('Pacific/Marquesas', 'Pacific/Marquesas'), ('Africa/Addis_Ababa', 'Africa/Addis_Ababa'), ('Australia/Brisbane', 'Australia/Brisbane'), ('Pacific/Kosrae', 'Pacific/Kosrae'), ('America/Guayaquil', 'America/Guayaquil'), ('Europe/Copenhagen', 'Europe/Copenhagen'), ('Arctic/Longyearbyen', 'Arctic/Longyearbyen'), ('Turkey', 'Turkey'), ('America/Argentina/Ushuaia', 'America/Argentina/Ushuaia'), ('Poland', 'Poland'), ('Asia/Singapore', 'Asia/Singapore'), ('US/Michigan', 'US/Michigan'), ('Asia/Tashkent', 'Asia/Tashkent'), ('America/Argentina/ComodRivadavia', 'America/Argentina/ComodRivadavia'), ('Pacific/Bougainville', 'Pacific/Bougainville'), ('Asia/Barnaul', 'Asia/Barnaul'), ('Pacific/Norfolk', 'Pacific/Norfolk'), ('Asia/Famagusta', 'Asia/Famagusta'), ('Europe/Belgrade', 'Europe/Belgrade'), ('Pacific/Apia', 'Pacific/Apia'), ('Europe/Saratov', 'Europe/Saratov'), ('Antarctica/South_Pole', 'Antarctica/South_Pole'), ('Europe/Simferopol', 'Europe/Simferopol'), ('Africa/Accra', 'Africa/Accra'), ('Etc/GMT-11', 'Etc/GMT-11'), ('Australia/Eucla', 'Australia/Eucla'), ('Universal', 'Universal'), ('Indian/Reunion', 'Indian/Reunion'), ('America/Denver', 'America/Denver'), ('Asia/Jayapura', 'Asia/Jayapura'), ('America/St_Johns', 'America/St_Johns'), ('Asia/Amman', 'Asia/Amman'), ('Europe/Skopje', 'Europe/Skopje'), ('America/Guyana', 'America/Guyana'), ('America/Rainy_River', 'America/Rainy_River'), ('America/Los_Angeles', 'America/Los_Angeles'), ('Etc/Zulu', 'Etc/Zulu'), ('America/Guadeloupe', 'America/Guadeloupe'), ('Pacific/Noumea', 'Pacific/Noumea'), ('Mexico/BajaNorte', 'Mexico/BajaNorte'), ('Asia/Colombo', 'Asia/Colombo'), ('Pacific/Ponape', 'Pacific/Ponape'), ('Antarctica/McMurdo', 'Antarctica/McMurdo'), ('Etc/GMT+6', 'Etc/GMT+6'), ('Etc/GMT-12', 'Etc/GMT-12'), ('America/Anchorage', 'America/Anchorage'), ('Pacific/Tongatapu', 'Pacific/Tongatapu'), ('Europe/Kyiv', 'Europe/Kyiv'), ('America/Cayman', 'America/Cayman'), ('Asia/Yekaterinburg', 'Asia/Yekaterinburg'), ('Asia/Ust-Nera', 'Asia/Ust-Nera'), ('Africa/Kampala', 'Africa/Kampala'), ('Etc/GMT-0', 'Etc/GMT-0'), ('America/Glace_Bay', 'America/Glace_Bay'), ('Etc/GMT0', 'Etc/GMT0'), ('Pacific/Guadalcanal', 'Pacific/Guadalcanal'), ('Europe/Zagreb', 'Europe/Zagreb'), ('America/Argentina/Salta', 'America/Argentina/Salta'), ('Mexico/General', 'Mexico/General'), ('Asia/Istanbul', 'Asia/Istanbul'), ('Africa/Bissau', 'Africa/Bissau'), ('Asia/Chongqing', 'Asia/Chongqing'), ('Asia/Muscat', 'Asia/Muscat'), ('Etc/GMT+1', 'Etc/GMT+1'), ('Singapore', 'Singapore'), ('America/Cuiaba', 'America/Cuiaba'), ('Europe/Kiev', 'Europe/Kiev'), ('Europe/Andorra', 'Europe/Andorra'), ('Europe/Monaco', 'Europe/Monaco'), ('Pacific/Yap', 'Pacific/Yap'), ('Asia/Hong_Kong', 'Asia/Hong_Kong'), ('America/Panama', 'America/Panama'), ('Etc/UTC', 'Etc/UTC'), ('America/Blanc-Sablon', 'America/Blanc-Sablon'), ('Asia/Gaza', 'Asia/Gaza'), ('Greenwich', 'Greenwich'), ('Europe/Uzhgorod', 'Europe/Uzhgorod'), ('Australia/Darwin', 'Australia/Darwin'), ('Australia/Melbourne', 'Australia/Melbourne'), ('CET', 'CET'), ('America/Porto_Acre', 'America/Porto_Acre'), ('America/Indiana/Marengo', 'America/Indiana/Marengo'), ('Antarctica/Mawson', 'Antarctica/Mawson'), ('Asia/Ashgabat', 'Asia/Ashgabat'), ('America/El_Salvador', 'America/El_Salvador'), ('Etc/GMT+10', 'Etc/GMT+10'), ('Europe/Ulyanovsk', 'Europe/Ulyanovsk'), ('Africa/Asmara', 'Africa/Asmara'), ('Europe/Paris', 'Europe/Paris'), ('Africa/Casablanca', 'Africa/Casablanca'), ('Europe/Rome', 'Europe/Rome'), ('America/Argentina/Jujuy', 'America/Argentina/Jujuy'), ('Africa/Lubumbashi', 'Africa/Lubumbashi'), ('Africa/Bujumbura', 'Africa/Bujumbura'), ('America/Indiana/Indianapolis', 'America/Indiana/Indianapolis'), ('Africa/Juba', 'Africa/Juba'), ('America/Sitka', 'America/Sitka'), ('America/Indiana/Vincennes', 'America/Indiana/Vincennes'), ('America/Ojinaga', 'America/Ojinaga'), ('Europe/Istanbul', 'Europe/Istanbul'), ('America/Martinique', 'America/Martinique'), ('America/Dawson', 'America/Dawson'), ('Africa/Johannesburg', 'Africa/Johannesburg'), ('Africa/Monrovia', 'Africa/Monrovia'), ('America/Halifax', 'America/Halifax'), ('Europe/Vatican', 'Europe/Vatican'), ('Asia/Brunei', 'Asia/Brunei'), ('Asia/Vladivostok', 'Asia/Vladivostok'), ('Etc/GMT-14', 'Etc/GMT-14'), ('Australia/Perth', 'Australia/Perth'), ('Pacific/Honolulu', 'Pacific/Honolulu'), ('Etc/GMT-9', 'Etc/GMT-9'), ('America/Monterrey', 'America/Monterrey'), ('Asia/Atyrau', 'Asia/Atyrau'), ('Etc/GMT-10', 'Etc/GMT-10'), ('America/Buenos_Aires', 'America/Buenos_Aires'), ('America/Campo_Grande', 'America/Campo_Grande'), ('Africa/Cairo', 'Africa/Cairo'), ('America/Antigua', 'America/Antigua'), ('Indian/Mayotte', 'Indian/Mayotte'), ('America/Hermosillo', 'America/Hermosillo'), ('Europe/Gibraltar', 'Europe/Gibraltar'), ('Africa/Nouakchott', 'Africa/Nouakchott'), ('Africa/Luanda', 'Africa/Luanda'), ('Asia/Kashgar', 'Asia/Kashgar'), ('America/Santo_Domingo', 'America/Santo_Domingo'), ('US/Aleutian', 'US/Aleutian'), ('America/Iqaluit', 'America/Iqaluit'), ('Mexico/BajaSur', 'Mexico/BajaSur'), ('Africa/Abidjan', 'Africa/Abidjan'), ('MST7MDT', 'MST7MDT'), ('Asia/Harbin', 'Asia/Harbin'), ('America/Chihuahua', 'America/Chihuahua'), ('Etc/GMT+0', 'Etc/GMT+0'), ('Australia/Currie', 'Australia/Currie'), ('Asia/Makassar', 'Asia/Makassar'), ('Asia/Ashkhabad', 'Asia/Ashkhabad'), ('Etc/Universal', 'Etc/Universal'), ('America/Fort_Nelson', 'America/Fort_Nelson'), ('Asia/Kuwait', 'Asia/Kuwait'), ('Asia/Urumqi', 'Asia/Urumqi'), ('Australia/Lindeman', 'Australia/Lindeman'), ('Asia/Magadan', 'Asia/Magadan'), ('Africa/Maseru', 'Africa/Maseru'), ('Etc/GMT+8', 'Etc/GMT+8'), ('Canada/Pacific', 'Canada/Pacific'), ('Asia/Kathmandu', 'Asia/Kathmandu'), ('Asia/Ulan_Bator', 'Asia/Ulan_Bator'), ('Asia/Tehran', 'Asia/Tehran'), ('Europe/Athens', 'Europe/Athens'), ('Asia/Beirut', 'Asia/Beirut'), ('America/Boa_Vista', 'America/Boa_Vista'), ('Asia/Calcutta', 'Asia/Calcutta'), ('Chile/Continental', 'Chile/Continental'), ('Asia/Yakutsk', 'Asia/Yakutsk'), ('Pacific/Fiji', 'Pacific/Fiji'), ('Atlantic/Canary', 'Atlantic/Canary'), ('Etc/GMT+12', 'Etc/GMT+12'), ('Chile/EasterIsland', 'Chile/EasterIsland'), ('Europe/Stockholm', 'Europe/Stockholm'), ('Asia/Riyadh', 'Asia/Riyadh'), ('Europe/Mariehamn', 'Europe/Mariehamn'), ('Asia/Tel_Aviv', 'Asia/Tel_Aviv'), ('Australia/Broken_Hill', 'Australia/Broken_Hill'), ('Europe/Sofia', 'Europe/Sofia'), ('America/Ensenada', 'America/Ensenada'), ('Libya', 'Libya'), ('America/Chicago', 'America/Chicago'), ('America/Caracas', 'America/Caracas'), ('America/Ciudad_Juarez', 'America/Ciudad_Juarez'), ('America/Sao_Paulo', 'America/Sao_Paulo'), ('Asia/Chita', 'Asia/Chita'), ('America/Menominee', 'America/Menominee'), ('Atlantic/South_Georgia', 'Atlantic/South_Georgia'), ('America/Tortola', 'America/Tortola'), ('America/Nassau', 'America/Nassau'), ('America/Indiana/Vevay', 'America/Indiana/Vevay'), ('Factory', 'Factory'), ('Etc/UCT', 'Etc/UCT'), ('Africa/Blantyre', 'Africa/Blantyre'), ('America/Punta_Arenas', 'America/Punta_Arenas'), ('Asia/Chungking', 'Asia/Chungking'), ('America/Argentina/La_Rioja', 'America/Argentina/La_Rioja'), ('America/Argentina/Cordoba', 'America/Argentina/Cordoba'), ('PRC', 'PRC'), ('America/Belize', 'America/Belize'), ('GMT+0', 'GMT+0'), ('Asia/Oral', 'Asia/Oral'), ('Europe/Astrakhan', 'Europe/Astrakhan'), ('America/Recife', 'America/Recife'), ('Australia/South', 'Australia/South'), ('Europe/Luxembourg', 'Europe/Luxembourg'), ('Asia/Damascus', 'Asia/Damascus'), ('America/North_Dakota/Center', 'America/North_Dakota/Center'), ('America/Costa_Rica', 'America/Costa_Rica'), ('America/Detroit', 'America/Detroit'), ('Atlantic/St_Helena', 'Atlantic/St_Helena'), ('America/St_Kitts', 'America/St_Kitts'), ('America/Rosario', 'America/Rosario'), ('Africa/Porto-Novo', 'Africa/Porto-Novo'), ('America/Cambridge_Bay', 'America/Cambridge_Bay'), ('Africa/Lagos', 'Africa/Lagos'), ('Australia/Canberra', 'Australia/Canberra'), ('US/Central', 'US/Central'), ('Australia/West', 'Australia/West'), ('Pacific/Kwajalein', 'Pacific/Kwajalein'), ('Africa/Kigali', 'Africa/Kigali'), ('America/Tijuana', 'America/Tijuana'), ('Africa/Ouagadougou', 'Africa/Ouagadougou'), ('America/Cancun', 'America/Cancun'), ('America/North_Dakota/Beulah', 'America/North_Dakota/Beulah'), ('Indian/Kerguelen', 'Indian/Kerguelen'), ('Asia/Shanghai', 'Asia/Shanghai'), ('Europe/Minsk', 'Europe/Minsk'), ('America/Mazatlan', 'America/Mazatlan'), ('Atlantic/Cape_Verde', 'Atlantic/Cape_Verde'), ('America/Indiana/Tell_City', 'America/Indiana/Tell_City'), ('America/Tegucigalpa', 'America/Tegucigalpa'), ('Etc/GMT-8', 'Etc/GMT-8'), ('America/Thunder_Bay', 'America/Thunder_Bay'), ('Canada/Atlantic', 'Canada/Atlantic'), ('Brazil/Acre', 'Brazil/Acre'), ('Africa/Lusaka', 'Africa/Lusaka'), ('Europe/Ljubljana', 'Europe/Ljubljana'), ('Asia/Nicosia', 'Asia/Nicosia'), ('America/Guatemala', 'America/Guatemala'), ('America/Maceio', 'America/Maceio'), ('America/Bahia_Banderas', 'America/Bahia_Banderas'), ('Australia/Queensland', 'Australia/Queensland'), ('America/Mexico_City', 'America/Mexico_City'), ('Europe/Podgorica', 'Europe/Podgorica'), ('Europe/Moscow', 'Europe/Moscow'), ('America/Argentina/Buenos_Aires', 'America/Argentina/Buenos_Aires'), ('Pacific/Port_Moresby', 'Pacific/Port_Moresby'), ('Etc/GMT+11', 'Etc/GMT+11'), ('Africa/Mbabane', 'Africa/Mbabane'), ('Africa/Libreville', 'Africa/Libreville'), ('America/Indiana/Petersburg', 'America/Indiana/Petersburg'), ('Africa/Dakar', 'Africa/Dakar'), ('Asia/Phnom_Penh', 'Asia/Phnom_Penh'), ('Asia/Yangon', 'Asia/Yangon'), ('US/Pacific', 'US/Pacific'), ('America/Manaus', 'America/Manaus'), ('Pacific/Enderbury', 'Pacific/Enderbury'), ('Australia/ACT', 'Australia/ACT'), ('Europe/Lisbon', 'Europe/Lisbon'), ('GMT-0', 'GMT-0'), ('Africa/Maputo', 'Africa/Maputo'), ('Europe/Kaliningrad', 'Europe/Kaliningrad'), ('Pacific/Nauru', 'Pacific/Nauru'), ('America/Argentina/San_Luis', 'America/Argentina/San_Luis'), ('America/Whitehorse', 'America/Whitehorse'), ('Africa/Bamako', 'Africa/Bamako'), ('Europe/Volgograd', 'Europe/Volgograd'), ('Pacific/Saipan', 'Pacific/Saipan'), ('Asia/Tbilisi', 'Asia/Tbilisi'), ('America/Cayenne', 'America/Cayenne'), ('Europe/Berlin', 'Europe/Berlin'), ('America/Araguaina', 'America/Araguaina'), ('NZ', 'NZ'), ('Antarctica/Casey', 'Antarctica/Casey'), ('Europe/Riga', 'Europe/Riga'), ('America/Nipigon', 'America/Nipigon'), ('Canada/Newfoundland', 'Canada/Newfoundland'), ('Africa/Algiers', 'Africa/Algiers'), ('Europe/Prague', 'Europe/Prague'), ('America/Rio_Branco', 'America/Rio_Branco'), ('America/Puerto_Rico', 'America/Puerto_Rico'), ('Australia/Lord_Howe', 'Australia/Lord_Howe'), ('Europe/Tallinn', 'Europe/Tallinn'), ('Europe/Vienna', 'Europe/Vienna'), ('Asia/Dushanbe', 'Asia/Dushanbe'), ('America/Grenada', 'America/Grenada'), ('America/Goose_Bay', 'America/Goose_Bay'), ('Asia/Manila', 'Asia/Manila'), ('Asia/Dhaka', 'Asia/Dhaka'), ('GMT', 'GMT'), ('Europe/Samara', 'Europe/Samara'), ('Europe/Isle_of_Man', 'Europe/Isle_of_Man'), ('America/Noronha', 'America/Noronha'), ('Asia/Aden', 'Asia/Aden'), ('US/East-Indiana', 'US/East-Indiana'), ('Europe/San_Marino', 'Europe/San_Marino'), ('America/Regina', 'America/Regina'), ('America/Kentucky/Monticello', 'America/Kentucky/Monticello'), ('Asia/Aqtau', 'Asia/Aqtau'), ('Zulu', 'Zulu'), ('MST', 'MST'), ('Asia/Novokuznetsk', 'Asia/Novokuznetsk'), ('America/Santa_Isabel', 'America/Santa_Isabel'), ('Pacific/Rarotonga', 'Pacific/Rarotonga'), ('EST5EDT', 'EST5EDT'), ('Etc/GMT-4', 'Etc/GMT-4'), ('Etc/GMT+7', 'Etc/GMT+7'), ('Europe/Vilnius', 'Europe/Vilnius'), ('Asia/Tomsk', 'Asia/Tomsk'), ('Pacific/Pohnpei', 'Pacific/Pohnpei'), ('Pacific/Auckland', 'Pacific/Auckland'), ('America/Dawson_Creek', 'America/Dawson_Creek'), ('Africa/Asmera', 'Africa/Asmera'), ('America/Adak', 'America/Adak'), ('America/Paramaribo', 'America/Paramaribo'), ('America/St_Barthelemy', 'America/St_Barthelemy'), ('Pacific/Galapagos', 'Pacific/Galapagos'), ('Eire', 'Eire'), ('Antarctica/Macquarie', 'Antarctica/Macquarie'), ('America/Godthab', 'America/Godthab'), ('Europe/Brussels', 'Europe/Brussels'), ('Atlantic/Faeroe', 'Atlantic/Faeroe'), ('America/Swift_Current', 'America/Swift_Current'), ('Asia/Kuala_Lumpur', 'Asia/Kuala_Lumpur')], default='Asia/Kolkata', max_length=50, verbose_name='Time zone'),
        ),
    ]
