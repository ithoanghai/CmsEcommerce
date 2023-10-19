# Generated by Django 4.2.6 on 2023-10-17 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creme_core', '0036_alter_user_time_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='time_zone',
            field=models.CharField(choices=[('Asia/Thimbu', 'Asia/Thimbu'), ('Asia/Dushanbe', 'Asia/Dushanbe'), ('Africa/Kigali', 'Africa/Kigali'), ('America/Port_of_Spain', 'America/Port_of_Spain'), ('America/Montreal', 'America/Montreal'), ('America/Araguaina', 'America/Araguaina'), ('Africa/Ceuta', 'Africa/Ceuta'), ('Asia/Khandyga', 'Asia/Khandyga'), ('Pacific/Bougainville', 'Pacific/Bougainville'), ('America/Fort_Nelson', 'America/Fort_Nelson'), ('Europe/Kyiv', 'Europe/Kyiv'), ('America/Antigua', 'America/Antigua'), ('NZ-CHAT', 'NZ-CHAT'), ('Africa/Malabo', 'Africa/Malabo'), ('America/El_Salvador', 'America/El_Salvador'), ('Europe/Vatican', 'Europe/Vatican'), ('US/Samoa', 'US/Samoa'), ('Universal', 'Universal'), ('Asia/Bahrain', 'Asia/Bahrain'), ('Asia/Pyongyang', 'Asia/Pyongyang'), ('Hongkong', 'Hongkong'), ('Asia/Yerevan', 'Asia/Yerevan'), ('America/Eirunepe', 'America/Eirunepe'), ('Etc/GMT+4', 'Etc/GMT+4'), ('Atlantic/Bermuda', 'Atlantic/Bermuda'), ('Africa/Bangui', 'Africa/Bangui'), ('America/Nome', 'America/Nome'), ('Asia/Katmandu', 'Asia/Katmandu'), ('America/St_Vincent', 'America/St_Vincent'), ('Africa/Abidjan', 'Africa/Abidjan'), ('US/Arizona', 'US/Arizona'), ('Europe/Saratov', 'Europe/Saratov'), ('Pacific/Midway', 'Pacific/Midway'), ('America/Argentina/Jujuy', 'America/Argentina/Jujuy'), ('Africa/Bissau', 'Africa/Bissau'), ('Etc/GMT+3', 'Etc/GMT+3'), ('America/St_Lucia', 'America/St_Lucia'), ('America/Anguilla', 'America/Anguilla'), ('Europe/Zagreb', 'Europe/Zagreb'), ('Africa/Ouagadougou', 'Africa/Ouagadougou'), ('Europe/Mariehamn', 'Europe/Mariehamn'), ('Europe/Simferopol', 'Europe/Simferopol'), ('America/Punta_Arenas', 'America/Punta_Arenas'), ('Europe/Dublin', 'Europe/Dublin'), ('Asia/Shanghai', 'Asia/Shanghai'), ('Europe/Belfast', 'Europe/Belfast'), ('Africa/Maseru', 'Africa/Maseru'), ('Europe/Berlin', 'Europe/Berlin'), ('Pacific/Pohnpei', 'Pacific/Pohnpei'), ('Australia/Melbourne', 'Australia/Melbourne'), ('Europe/Busingen', 'Europe/Busingen'), ('Asia/Qyzylorda', 'Asia/Qyzylorda'), ('Etc/GMT-1', 'Etc/GMT-1'), ('Asia/Amman', 'Asia/Amman'), ('Asia/Damascus', 'Asia/Damascus'), ('Iran', 'Iran'), ('Asia/Thimphu', 'Asia/Thimphu'), ('US/Indiana-Starke', 'US/Indiana-Starke'), ('Atlantic/Canary', 'Atlantic/Canary'), ('Australia/Canberra', 'Australia/Canberra'), ('Africa/Harare', 'Africa/Harare'), ('Europe/Bratislava', 'Europe/Bratislava'), ('Indian/Cocos', 'Indian/Cocos'), ('Portugal', 'Portugal'), ('Pacific/Kwajalein', 'Pacific/Kwajalein'), ('Europe/Warsaw', 'Europe/Warsaw'), ('Brazil/Acre', 'Brazil/Acre'), ('America/Montserrat', 'America/Montserrat'), ('Antarctica/McMurdo', 'Antarctica/McMurdo'), ('Asia/Istanbul', 'Asia/Istanbul'), ('Europe/Lisbon', 'Europe/Lisbon'), ('Antarctica/Davis', 'Antarctica/Davis'), ('Etc/GMT+0', 'Etc/GMT+0'), ('America/Santa_Isabel', 'America/Santa_Isabel'), ('Asia/Kuwait', 'Asia/Kuwait'), ('Pacific/Enderbury', 'Pacific/Enderbury'), ('Asia/Colombo', 'Asia/Colombo'), ('Europe/Sofia', 'Europe/Sofia'), ('Europe/Prague', 'Europe/Prague'), ('Arctic/Longyearbyen', 'Arctic/Longyearbyen'), ('Pacific/Guadalcanal', 'Pacific/Guadalcanal'), ('Europe/Riga', 'Europe/Riga'), ('Asia/Yekaterinburg', 'Asia/Yekaterinburg'), ('Europe/San_Marino', 'Europe/San_Marino'), ('Pacific/Tarawa', 'Pacific/Tarawa'), ('America/Belize', 'America/Belize'), ('America/Rio_Branco', 'America/Rio_Branco'), ('Australia/Eucla', 'Australia/Eucla'), ('America/New_York', 'America/New_York'), ('Europe/Zaporozhye', 'Europe/Zaporozhye'), ('Asia/Rangoon', 'Asia/Rangoon'), ('Europe/Athens', 'Europe/Athens'), ('Singapore', 'Singapore'), ('America/Argentina/ComodRivadavia', 'America/Argentina/ComodRivadavia'), ('Europe/Rome', 'Europe/Rome'), ('Pacific/Truk', 'Pacific/Truk'), ('Etc/GMT+8', 'Etc/GMT+8'), ('Pacific/Kiritimati', 'Pacific/Kiritimati'), ('Etc/GMT+1', 'Etc/GMT+1'), ('Africa/Algiers', 'Africa/Algiers'), ('W-SU', 'W-SU'), ('Indian/Chagos', 'Indian/Chagos'), ('America/Cayman', 'America/Cayman'), ('Europe/Guernsey', 'Europe/Guernsey'), ('America/Recife', 'America/Recife'), ('Asia/Choibalsan', 'Asia/Choibalsan'), ('America/Los_Angeles', 'America/Los_Angeles'), ('Europe/Vienna', 'Europe/Vienna'), ('America/Jujuy', 'America/Jujuy'), ('America/Buenos_Aires', 'America/Buenos_Aires'), ('Africa/Johannesburg', 'Africa/Johannesburg'), ('Europe/London', 'Europe/London'), ('UCT', 'UCT'), ('Atlantic/South_Georgia', 'Atlantic/South_Georgia'), ('US/East-Indiana', 'US/East-Indiana'), ('Europe/Monaco', 'Europe/Monaco'), ('Australia/West', 'Australia/West'), ('Etc/GMT+10', 'Etc/GMT+10'), ('Pacific/Kanton', 'Pacific/Kanton'), ('Europe/Tirane', 'Europe/Tirane'), ('America/Chihuahua', 'America/Chihuahua'), ('America/Detroit', 'America/Detroit'), ('America/Goose_Bay', 'America/Goose_Bay'), ('Asia/Kuala_Lumpur', 'Asia/Kuala_Lumpur'), ('Europe/Podgorica', 'Europe/Podgorica'), ('Mexico/BajaNorte', 'Mexico/BajaNorte'), ('Pacific/Saipan', 'Pacific/Saipan'), ('Asia/Dacca', 'Asia/Dacca'), ('Pacific/Fakaofo', 'Pacific/Fakaofo'), ('PRC', 'PRC'), ('Pacific/Easter', 'Pacific/Easter'), ('America/Yakutat', 'America/Yakutat'), ('Asia/Tehran', 'Asia/Tehran'), ('Australia/Adelaide', 'Australia/Adelaide'), ('Turkey', 'Turkey'), ('Indian/Mayotte', 'Indian/Mayotte'), ('Africa/Porto-Novo', 'Africa/Porto-Novo'), ('HST', 'HST'), ('Pacific/Pitcairn', 'Pacific/Pitcairn'), ('Asia/Aqtau', 'Asia/Aqtau'), ('Europe/Bucharest', 'Europe/Bucharest'), ('America/Jamaica', 'America/Jamaica'), ('Asia/Yakutsk', 'Asia/Yakutsk'), ('Asia/Anadyr', 'Asia/Anadyr'), ('Atlantic/St_Helena', 'Atlantic/St_Helena'), ('Indian/Kerguelen', 'Indian/Kerguelen'), ('Asia/Oral', 'Asia/Oral'), ('Etc/GMT-0', 'Etc/GMT-0'), ('Europe/Paris', 'Europe/Paris'), ('UTC', 'UTC'), ('Pacific/Palau', 'Pacific/Palau'), ('Asia/Qatar', 'Asia/Qatar'), ('Etc/GMT-12', 'Etc/GMT-12'), ('Etc/Greenwich', 'Etc/Greenwich'), ('Asia/Yangon', 'Asia/Yangon'), ('Asia/Jakarta', 'Asia/Jakarta'), ('Asia/Chita', 'Asia/Chita'), ('Asia/Kashgar', 'Asia/Kashgar'), ('America/Argentina/San_Luis', 'America/Argentina/San_Luis'), ('America/Paramaribo', 'America/Paramaribo'), ('Asia/Brunei', 'Asia/Brunei'), ('Brazil/East', 'Brazil/East'), ('Pacific/Kosrae', 'Pacific/Kosrae'), ('Pacific/Pago_Pago', 'Pacific/Pago_Pago'), ('Asia/Bangkok', 'Asia/Bangkok'), ('Asia/Beirut', 'Asia/Beirut'), ('CST6CDT', 'CST6CDT'), ('Etc/UTC', 'Etc/UTC'), ('Australia/Queensland', 'Australia/Queensland'), ('Pacific/Gambier', 'Pacific/Gambier'), ('Europe/Isle_of_Man', 'Europe/Isle_of_Man'), ('Pacific/Rarotonga', 'Pacific/Rarotonga'), ('Asia/Vladivostok', 'Asia/Vladivostok'), ('America/Monterrey', 'America/Monterrey'), ('Asia/Hebron', 'Asia/Hebron'), ('America/Scoresbysund', 'America/Scoresbysund'), ('America/Dawson_Creek', 'America/Dawson_Creek'), ('America/Pangnirtung', 'America/Pangnirtung'), ('America/North_Dakota/Center', 'America/North_Dakota/Center'), ('America/Santo_Domingo', 'America/Santo_Domingo'), ('Asia/Saigon', 'Asia/Saigon'), ('Antarctica/Casey', 'Antarctica/Casey'), ('America/Halifax', 'America/Halifax'), ('America/Argentina/Catamarca', 'America/Argentina/Catamarca'), ('Etc/GMT+9', 'Etc/GMT+9'), ('Chile/EasterIsland', 'Chile/EasterIsland'), ('Asia/Riyadh', 'Asia/Riyadh'), ('Antarctica/Vostok', 'Antarctica/Vostok'), ('Asia/Calcutta', 'Asia/Calcutta'), ('Africa/Asmera', 'Africa/Asmera'), ('America/Boa_Vista', 'America/Boa_Vista'), ('Antarctica/Palmer', 'Antarctica/Palmer'), ('Europe/Luxembourg', 'Europe/Luxembourg'), ('Africa/Dakar', 'Africa/Dakar'), ('Australia/Darwin', 'Australia/Darwin'), ('America/Danmarkshavn', 'America/Danmarkshavn'), ('Asia/Sakhalin', 'Asia/Sakhalin'), ('America/Argentina/La_Rioja', 'America/Argentina/La_Rioja'), ('America/Manaus', 'America/Manaus'), ('EST', 'EST'), ('Asia/Ho_Chi_Minh', 'Asia/Ho_Chi_Minh'), ('US/Eastern', 'US/Eastern'), ('Africa/Douala', 'Africa/Douala'), ('Pacific/Honolulu', 'Pacific/Honolulu'), ('Canada/Pacific', 'Canada/Pacific'), ('America/Porto_Velho', 'America/Porto_Velho'), ('Indian/Antananarivo', 'Indian/Antananarivo'), ('America/Thule', 'America/Thule'), ('Africa/Mogadishu', 'Africa/Mogadishu'), ('Europe/Copenhagen', 'Europe/Copenhagen'), ('Asia/Kabul', 'Asia/Kabul'), ('Asia/Gaza', 'Asia/Gaza'), ('Africa/Lusaka', 'Africa/Lusaka'), ('Asia/Jayapura', 'Asia/Jayapura'), ('America/Phoenix', 'America/Phoenix'), ('America/Boise', 'America/Boise'), ('America/Kentucky/Monticello', 'America/Kentucky/Monticello'), ('America/Havana', 'America/Havana'), ('Europe/Minsk', 'Europe/Minsk'), ('Africa/Lagos', 'Africa/Lagos'), ('Asia/Seoul', 'Asia/Seoul'), ('America/Argentina/Salta', 'America/Argentina/Salta'), ('Africa/Dar_es_Salaam', 'Africa/Dar_es_Salaam'), ('Europe/Kaliningrad', 'Europe/Kaliningrad'), ('Navajo', 'Navajo'), ('America/Maceio', 'America/Maceio'), ('Greenwich', 'Greenwich'), ('America/Blanc-Sablon', 'America/Blanc-Sablon'), ('America/Ciudad_Juarez', 'America/Ciudad_Juarez'), ('America/Curacao', 'America/Curacao'), ('GMT+0', 'GMT+0'), ('Africa/Asmara', 'Africa/Asmara'), ('America/Creston', 'America/Creston'), ('Asia/Tokyo', 'Asia/Tokyo'), ('Europe/Sarajevo', 'Europe/Sarajevo'), ('Canada/Atlantic', 'Canada/Atlantic'), ('America/Rosario', 'America/Rosario'), ('America/Thunder_Bay', 'America/Thunder_Bay'), ('Atlantic/Faeroe', 'Atlantic/Faeroe'), ('America/Virgin', 'America/Virgin'), ('Etc/GMT-5', 'Etc/GMT-5'), ('Europe/Volgograd', 'Europe/Volgograd'), ('Europe/Kiev', 'Europe/Kiev'), ('America/Nipigon', 'America/Nipigon'), ('America/Ojinaga', 'America/Ojinaga'), ('America/Lower_Princes', 'America/Lower_Princes'), ('Asia/Karachi', 'Asia/Karachi'), ('Europe/Madrid', 'Europe/Madrid'), ('Africa/Brazzaville', 'Africa/Brazzaville'), ('Pacific/Johnston', 'Pacific/Johnston'), ('US/Hawaii', 'US/Hawaii'), ('Australia/Tasmania', 'Australia/Tasmania'), ('America/Argentina/Rio_Gallegos', 'America/Argentina/Rio_Gallegos'), ('America/Inuvik', 'America/Inuvik'), ('Mexico/BajaSur', 'Mexico/BajaSur'), ('Asia/Phnom_Penh', 'Asia/Phnom_Penh'), ('Australia/South', 'Australia/South'), ('America/Sitka', 'America/Sitka'), ('Asia/Dili', 'Asia/Dili'), ('Asia/Singapore', 'Asia/Singapore'), ('America/Knox_IN', 'America/Knox_IN'), ('Europe/Chisinau', 'Europe/Chisinau'), ('Kwajalein', 'Kwajalein'), ('Asia/Famagusta', 'Asia/Famagusta'), ('America/Fortaleza', 'America/Fortaleza'), ('GB-Eire', 'GB-Eire'), ('Etc/GMT-2', 'Etc/GMT-2'), ('Africa/Luanda', 'Africa/Luanda'), ('Europe/Tallinn', 'Europe/Tallinn'), ('Pacific/Tongatapu', 'Pacific/Tongatapu'), ('Asia/Ulan_Bator', 'Asia/Ulan_Bator'), ('America/Grand_Turk', 'America/Grand_Turk'), ('America/Anchorage', 'America/Anchorage'), ('Asia/Samarkand', 'Asia/Samarkand'), ('Atlantic/Cape_Verde', 'Atlantic/Cape_Verde'), ('Asia/Atyrau', 'Asia/Atyrau'), ('Indian/Maldives', 'Indian/Maldives'), ('America/Managua', 'America/Managua'), ('Asia/Dhaka', 'Asia/Dhaka'), ('Etc/GMT+12', 'Etc/GMT+12'), ('Asia/Barnaul', 'Asia/Barnaul'), ('America/Indiana/Knox', 'America/Indiana/Knox'), ('America/Argentina/Ushuaia', 'America/Argentina/Ushuaia'), ('Etc/GMT-8', 'Etc/GMT-8'), ('America/Tijuana', 'America/Tijuana'), ('America/Puerto_Rico', 'America/Puerto_Rico'), ('America/Indiana/Vincennes', 'America/Indiana/Vincennes'), ('Africa/Timbuktu', 'Africa/Timbuktu'), ('Europe/Kirov', 'Europe/Kirov'), ('America/Santiago', 'America/Santiago'), ('Europe/Samara', 'Europe/Samara'), ('Pacific/Marquesas', 'Pacific/Marquesas'), ('America/Vancouver', 'America/Vancouver'), ('America/Costa_Rica', 'America/Costa_Rica'), ('America/Whitehorse', 'America/Whitehorse'), ('Asia/Ashgabat', 'Asia/Ashgabat'), ('Atlantic/Faroe', 'Atlantic/Faroe'), ('America/Cambridge_Bay', 'America/Cambridge_Bay'), ('Asia/Almaty', 'Asia/Almaty'), ('Canada/Central', 'Canada/Central'), ('Antarctica/South_Pole', 'Antarctica/South_Pole'), ('Africa/Lome', 'Africa/Lome'), ('Europe/Zurich', 'Europe/Zurich'), ('America/Noronha', 'America/Noronha'), ('America/Guayaquil', 'America/Guayaquil'), ('America/Montevideo', 'America/Montevideo'), ('Asia/Krasnoyarsk', 'Asia/Krasnoyarsk'), ('Europe/Astrakhan', 'Europe/Astrakhan'), ('America/Indiana/Tell_City', 'America/Indiana/Tell_City'), ('America/Guyana', 'America/Guyana'), ('Etc/GMT0', 'Etc/GMT0'), ('Pacific/Samoa', 'Pacific/Samoa'), ('Atlantic/Azores', 'Atlantic/Azores'), ('Africa/Nouakchott', 'Africa/Nouakchott'), ('Europe/Moscow', 'Europe/Moscow'), ('America/Mazatlan', 'America/Mazatlan'), ('Asia/Macao', 'Asia/Macao'), ('MST7MDT', 'MST7MDT'), ('America/Campo_Grande', 'America/Campo_Grande'), ('Africa/Freetown', 'Africa/Freetown'), ('Africa/Kinshasa', 'Africa/Kinshasa'), ('America/Juneau', 'America/Juneau'), ('Europe/Amsterdam', 'Europe/Amsterdam'), ('Africa/Djibouti', 'Africa/Djibouti'), ('Europe/Ljubljana', 'Europe/Ljubljana'), ('America/Moncton', 'America/Moncton'), ('Europe/Belgrade', 'Europe/Belgrade'), ('America/Toronto', 'America/Toronto'), ('America/Catamarca', 'America/Catamarca'), ('Pacific/Ponape', 'Pacific/Ponape'), ('Etc/GMT-14', 'Etc/GMT-14'), ('Africa/Mbabane', 'Africa/Mbabane'), ('Pacific/Apia', 'Pacific/Apia'), ('Africa/Monrovia', 'Africa/Monrovia'), ('ROC', 'ROC'), ('Pacific/Norfolk', 'Pacific/Norfolk'), ('Africa/Tunis', 'Africa/Tunis'), ('America/Sao_Paulo', 'America/Sao_Paulo'), ('America/Argentina/Buenos_Aires', 'America/Argentina/Buenos_Aires'), ('Pacific/Galapagos', 'Pacific/Galapagos'), ('Australia/Lindeman', 'Australia/Lindeman'), ('Etc/GMT-4', 'Etc/GMT-4'), ('Asia/Irkutsk', 'Asia/Irkutsk'), ('America/Hermosillo', 'America/Hermosillo'), ('America/Kralendijk', 'America/Kralendijk'), ('Europe/Ulyanovsk', 'Europe/Ulyanovsk'), ('Europe/Oslo', 'Europe/Oslo'), ('Australia/Broken_Hill', 'Australia/Broken_Hill'), ('Europe/Uzhgorod', 'Europe/Uzhgorod'), ('GB', 'GB'), ('America/Cayenne', 'America/Cayenne'), ('America/St_Barthelemy', 'America/St_Barthelemy'), ('MST', 'MST'), ('Europe/Vilnius', 'Europe/Vilnius'), ('Europe/Vaduz', 'Europe/Vaduz'), ('Atlantic/Reykjavik', 'Atlantic/Reykjavik'), ('Indian/Comoro', 'Indian/Comoro'), ('Australia/Brisbane', 'Australia/Brisbane'), ('Asia/Baku', 'Asia/Baku'), ('Pacific/Auckland', 'Pacific/Auckland'), ('Asia/Makassar', 'Asia/Makassar'), ('Brazil/West', 'Brazil/West'), ('Canada/Yukon', 'Canada/Yukon'), ('Asia/Novokuznetsk', 'Asia/Novokuznetsk'), ('Australia/North', 'Australia/North'), ('Asia/Tashkent', 'Asia/Tashkent'), ('PST8PDT', 'PST8PDT'), ('America/Dominica', 'America/Dominica'), ('Indian/Mauritius', 'Indian/Mauritius'), ('Asia/Chongqing', 'Asia/Chongqing'), ('Iceland', 'Iceland'), ('Antarctica/Syowa', 'Antarctica/Syowa'), ('America/Louisville', 'America/Louisville'), ('America/Cuiaba', 'America/Cuiaba'), ('Etc/GMT+7', 'Etc/GMT+7'), ('America/Santarem', 'America/Santarem'), ('Canada/Mountain', 'Canada/Mountain'), ('America/Denver', 'America/Denver'), ('Etc/UCT', 'Etc/UCT'), ('Antarctica/Macquarie', 'Antarctica/Macquarie'), ('Antarctica/Rothera', 'Antarctica/Rothera'), ('Europe/Tiraspol', 'Europe/Tiraspol'), ('Asia/Urumqi', 'Asia/Urumqi'), ('Europe/Helsinki', 'Europe/Helsinki'), ('America/North_Dakota/New_Salem', 'America/North_Dakota/New_Salem'), ('America/Iqaluit', 'America/Iqaluit'), ('America/Port-au-Prince', 'America/Port-au-Prince'), ('America/Mexico_City', 'America/Mexico_City'), ('MET', 'MET'), ('Zulu', 'Zulu'), ('Asia/Hovd', 'Asia/Hovd'), ('Factory', 'Factory'), ('America/Guadeloupe', 'America/Guadeloupe'), ('America/North_Dakota/Beulah', 'America/North_Dakota/Beulah'), ('Africa/Cairo', 'Africa/Cairo'), ('Asia/Tbilisi', 'Asia/Tbilisi'), ('America/Panama', 'America/Panama'), ('Indian/Mahe', 'Indian/Mahe'), ('Europe/Nicosia', 'Europe/Nicosia'), ('America/Argentina/San_Juan', 'America/Argentina/San_Juan'), ('Canada/Eastern', 'Canada/Eastern'), ('America/St_Thomas', 'America/St_Thomas'), ('CET', 'CET'), ('US/Alaska', 'US/Alaska'), ('EET', 'EET'), ('Egypt', 'Egypt'), ('America/Argentina/Tucuman', 'America/Argentina/Tucuman'), ('Etc/GMT+6', 'Etc/GMT+6'), ('Asia/Kathmandu', 'Asia/Kathmandu'), ('Etc/GMT-11', 'Etc/GMT-11'), ('Etc/GMT+5', 'Etc/GMT+5'), ('Japan', 'Japan'), ('Europe/Skopje', 'Europe/Skopje'), ('Etc/GMT-3', 'Etc/GMT-3'), ('America/Rankin_Inlet', 'America/Rankin_Inlet'), ('America/Cordoba', 'America/Cordoba'), ('Pacific/Tahiti', 'Pacific/Tahiti'), ('Africa/El_Aaiun', 'Africa/El_Aaiun'), ('Asia/Kuching', 'Asia/Kuching'), ('Mexico/General', 'Mexico/General'), ('America/Caracas', 'America/Caracas'), ('America/St_Kitts', 'America/St_Kitts'), ('Atlantic/Jan_Mayen', 'Atlantic/Jan_Mayen'), ('America/Tortola', 'America/Tortola'), ('America/Bahia_Banderas', 'America/Bahia_Banderas'), ('Africa/Gaborone', 'Africa/Gaborone'), ('Africa/Bamako', 'Africa/Bamako'), ('Asia/Magadan', 'Asia/Magadan'), ('Etc/GMT-13', 'Etc/GMT-13'), ('Asia/Ujung_Pandang', 'Asia/Ujung_Pandang'), ('Australia/Yancowinna', 'Australia/Yancowinna'), ('Etc/GMT-10', 'Etc/GMT-10'), ('Asia/Vientiane', 'Asia/Vientiane'), ('America/Winnipeg', 'America/Winnipeg'), ('Asia/Qostanay', 'Asia/Qostanay'), ('Australia/Sydney', 'Australia/Sydney'), ('Africa/Sao_Tome', 'Africa/Sao_Tome'), ('America/Godthab', 'America/Godthab'), ('US/Central', 'US/Central'), ('GMT-0', 'GMT-0'), ('America/Nassau', 'America/Nassau'), ('Europe/Jersey', 'Europe/Jersey'), ('America/Ensenada', 'America/Ensenada'), ('Etc/Zulu', 'Etc/Zulu'), ('America/Belem', 'America/Belem'), ('Asia/Baghdad', 'Asia/Baghdad'), ('Africa/Bujumbura', 'Africa/Bujumbura'), ('America/Chicago', 'America/Chicago'), ('Asia/Tel_Aviv', 'Asia/Tel_Aviv'), ('America/Edmonton', 'America/Edmonton'), ('Africa/Blantyre', 'Africa/Blantyre'), ('America/Regina', 'America/Regina'), ('Asia/Taipei', 'Asia/Taipei'), ('Brazil/DeNoronha', 'Brazil/DeNoronha'), ('Etc/GMT+2', 'Etc/GMT+2'), ('Africa/Nairobi', 'Africa/Nairobi'), ('America/Adak', 'America/Adak'), ('Australia/NSW', 'Australia/NSW'), ('Australia/Perth', 'Australia/Perth'), ('Indian/Reunion', 'Indian/Reunion'), ('US/Aleutian', 'US/Aleutian'), ('America/Resolute', 'America/Resolute'), ('America/Coral_Harbour', 'America/Coral_Harbour'), ('Asia/Ust-Nera', 'Asia/Ust-Nera'), ('Chile/Continental', 'Chile/Continental'), ('America/Atikokan', 'America/Atikokan'), ('America/Indiana/Vevay', 'America/Indiana/Vevay'), ('America/Argentina/Mendoza', 'America/Argentina/Mendoza'), ('Etc/Universal', 'Etc/Universal'), ('Africa/Accra', 'Africa/Accra'), ('Asia/Chungking', 'Asia/Chungking'), ('Africa/Tripoli', 'Africa/Tripoli'), ('Asia/Nicosia', 'Asia/Nicosia'), ('America/Indiana/Petersburg', 'America/Indiana/Petersburg'), ('Pacific/Majuro', 'Pacific/Majuro'), ('America/Cancun', 'America/Cancun'), ('America/Argentina/Cordoba', 'America/Argentina/Cordoba'), ('GMT', 'GMT'), ('Asia/Omsk', 'Asia/Omsk'), ('Atlantic/Madeira', 'Atlantic/Madeira'), ('Pacific/Port_Moresby', 'Pacific/Port_Moresby'), ('America/Bogota', 'America/Bogota'), ('Australia/Currie', 'Australia/Currie'), ('Eire', 'Eire'), ('America/Merida', 'America/Merida'), ('NZ', 'NZ'), ('US/Michigan', 'US/Michigan'), ('Etc/GMT-9', 'Etc/GMT-9'), ('Pacific/Fiji', 'Pacific/Fiji'), ('Europe/Gibraltar', 'Europe/Gibraltar'), ('Antarctica/Mawson', 'Antarctica/Mawson'), ('ROK', 'ROK'), ('Asia/Macau', 'Asia/Macau'), ('Africa/Addis_Ababa', 'Africa/Addis_Ababa'), ('Africa/Banjul', 'Africa/Banjul'), ('America/Grenada', 'America/Grenada'), ('Pacific/Wallis', 'Pacific/Wallis'), ('Africa/Kampala', 'Africa/Kampala'), ('America/Marigot', 'America/Marigot'), ('America/Aruba', 'America/Aruba'), ('Africa/Casablanca', 'Africa/Casablanca'), ('Asia/Aden', 'Asia/Aden'), ('America/Barbados', 'America/Barbados'), ('America/Swift_Current', 'America/Swift_Current'), ('Pacific/Yap', 'Pacific/Yap'), ('Pacific/Chatham', 'Pacific/Chatham'), ('EST5EDT', 'EST5EDT'), ('Europe/Malta', 'Europe/Malta'), ('Asia/Ulaanbaatar', 'Asia/Ulaanbaatar'), ('America/Matamoros', 'America/Matamoros'), ('GMT0', 'GMT0'), ('America/Asuncion', 'America/Asuncion'), ('America/Fort_Wayne', 'America/Fort_Wayne'), ('America/Indiana/Indianapolis', 'America/Indiana/Indianapolis'), ('Asia/Manila', 'Asia/Manila'), ('Pacific/Efate', 'Pacific/Efate'), ('America/Yellowknife', 'America/Yellowknife'), ('Europe/Andorra', 'Europe/Andorra'), ('America/Rainy_River', 'America/Rainy_River'), ('US/Mountain', 'US/Mountain'), ('Africa/Lubumbashi', 'Africa/Lubumbashi'), ('Africa/Conakry', 'Africa/Conakry'), ('Europe/Stockholm', 'Europe/Stockholm'), ('Australia/LHI', 'Australia/LHI'), ('Etc/GMT-6', 'Etc/GMT-6'), ('WET', 'WET'), ('America/Martinique', 'America/Martinique'), ('Asia/Ashkhabad', 'Asia/Ashkhabad'), ('Africa/Niamey', 'Africa/Niamey'), ('America/Menominee', 'America/Menominee'), ('America/Dawson', 'America/Dawson'), ('America/Guatemala', 'America/Guatemala'), ('Antarctica/Troll', 'Antarctica/Troll'), ('Asia/Srednekolymsk', 'Asia/Srednekolymsk'), ('America/Atka', 'America/Atka'), ('Asia/Harbin', 'Asia/Harbin'), ('Australia/Hobart', 'Australia/Hobart'), ('Canada/Newfoundland', 'Canada/Newfoundland'), ('America/Nuuk', 'America/Nuuk'), ('Europe/Brussels', 'Europe/Brussels'), ('Asia/Tomsk', 'Asia/Tomsk'), ('Africa/Ndjamena', 'Africa/Ndjamena'), ('Etc/GMT+11', 'Etc/GMT+11'), ('Pacific/Nauru', 'Pacific/Nauru'), ('Cuba', 'Cuba'), ('Europe/Istanbul', 'Europe/Istanbul'), ('Asia/Muscat', 'Asia/Muscat'), ('US/Pacific', 'US/Pacific'), ('Asia/Dubai', 'Asia/Dubai'), ('America/Mendoza', 'America/Mendoza'), ('America/Indianapolis', 'America/Indianapolis'), ('Jamaica', 'Jamaica'), ('Pacific/Noumea', 'Pacific/Noumea'), ('Asia/Hong_Kong', 'Asia/Hong_Kong'), ('America/Indiana/Marengo', 'America/Indiana/Marengo'), ('Pacific/Guam', 'Pacific/Guam'), ('Asia/Bishkek', 'Asia/Bishkek'), ('Indian/Christmas', 'Indian/Christmas'), ('America/Miquelon', 'America/Miquelon'), ('Poland', 'Poland'), ('Asia/Pontianak', 'Asia/Pontianak'), ('America/Porto_Acre', 'America/Porto_Acre'), ('America/Lima', 'America/Lima'), ('America/Shiprock', 'America/Shiprock'), ('Australia/Lord_Howe', 'Australia/Lord_Howe'), ('Asia/Kamchatka', 'Asia/Kamchatka'), ('Antarctica/DumontDUrville', 'Antarctica/DumontDUrville'), ('Asia/Kolkata', 'Asia/Kolkata'), ('Pacific/Niue', 'Pacific/Niue'), ('Asia/Novosibirsk', 'Asia/Novosibirsk'), ('America/Kentucky/Louisville', 'America/Kentucky/Louisville'), ('Pacific/Funafuti', 'Pacific/Funafuti'), ('Africa/Juba', 'Africa/Juba'), ('America/St_Johns', 'America/St_Johns'), ('America/La_Paz', 'America/La_Paz'), ('America/Metlakatla', 'America/Metlakatla'), ('Pacific/Chuuk', 'Pacific/Chuuk'), ('Australia/Victoria', 'Australia/Victoria'), ('America/Glace_Bay', 'America/Glace_Bay'), ('Etc/GMT-7', 'Etc/GMT-7'), ('Israel', 'Israel'), ('Atlantic/Stanley', 'Atlantic/Stanley'), ('America/Indiana/Winamac', 'America/Indiana/Winamac'), ('America/Bahia', 'America/Bahia'), ('Africa/Maputo', 'Africa/Maputo'), ('Africa/Windhoek', 'Africa/Windhoek'), ('Australia/ACT', 'Australia/ACT'), ('Pacific/Wake', 'Pacific/Wake'), ('Africa/Khartoum', 'Africa/Khartoum'), ('Asia/Aqtobe', 'Asia/Aqtobe'), ('America/Tegucigalpa', 'America/Tegucigalpa'), ('Canada/Saskatchewan', 'Canada/Saskatchewan'), ('Africa/Libreville', 'Africa/Libreville'), ('Libya', 'Libya'), ('Etc/GMT', 'Etc/GMT'), ('Asia/Jerusalem', 'Asia/Jerusalem'), ('Europe/Budapest', 'Europe/Budapest')], default='Asia/Kolkata', max_length=50, verbose_name='Time zone'),
        ),
    ]
