# Generated by Django 4.2.6 on 2023-10-17 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creme_core', '0037_alter_user_time_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='time_zone',
            field=models.CharField(choices=[('Africa/Nouakchott', 'Africa/Nouakchott'), ('America/Martinique', 'America/Martinique'), ('America/Costa_Rica', 'America/Costa_Rica'), ('PST8PDT', 'PST8PDT'), ('Asia/Damascus', 'Asia/Damascus'), ('HST', 'HST'), ('America/St_Johns', 'America/St_Johns'), ('America/Scoresbysund', 'America/Scoresbysund'), ('Etc/UCT', 'Etc/UCT'), ('PRC', 'PRC'), ('Africa/Freetown', 'Africa/Freetown'), ('Atlantic/Jan_Mayen', 'Atlantic/Jan_Mayen'), ('America/Swift_Current', 'America/Swift_Current'), ('America/Indiana/Knox', 'America/Indiana/Knox'), ('Europe/Stockholm', 'Europe/Stockholm'), ('Kwajalein', 'Kwajalein'), ('Factory', 'Factory'), ('Europe/Zagreb', 'Europe/Zagreb'), ('Europe/Tallinn', 'Europe/Tallinn'), ('Europe/Oslo', 'Europe/Oslo'), ('Antarctica/Palmer', 'Antarctica/Palmer'), ('US/Central', 'US/Central'), ('Atlantic/Faeroe', 'Atlantic/Faeroe'), ('Asia/Yangon', 'Asia/Yangon'), ('Africa/Ouagadougou', 'Africa/Ouagadougou'), ('America/Mexico_City', 'America/Mexico_City'), ('Pacific/Saipan', 'Pacific/Saipan'), ('Atlantic/Azores', 'Atlantic/Azores'), ('America/Argentina/Buenos_Aires', 'America/Argentina/Buenos_Aires'), ('Egypt', 'Egypt'), ('Antarctica/Vostok', 'Antarctica/Vostok'), ('Etc/GMT-13', 'Etc/GMT-13'), ('Etc/GMT-2', 'Etc/GMT-2'), ('Chile/Continental', 'Chile/Continental'), ('America/Jujuy', 'America/Jujuy'), ('Europe/Isle_of_Man', 'Europe/Isle_of_Man'), ('Australia/West', 'Australia/West'), ('America/Porto_Acre', 'America/Porto_Acre'), ('America/Maceio', 'America/Maceio'), ('America/Chicago', 'America/Chicago'), ('Pacific/Ponape', 'Pacific/Ponape'), ('America/Glace_Bay', 'America/Glace_Bay'), ('America/Shiprock', 'America/Shiprock'), ('US/East-Indiana', 'US/East-Indiana'), ('America/Indiana/Vincennes', 'America/Indiana/Vincennes'), ('Asia/Tokyo', 'Asia/Tokyo'), ('Pacific/Guam', 'Pacific/Guam'), ('Poland', 'Poland'), ('America/Nassau', 'America/Nassau'), ('Etc/GMT+1', 'Etc/GMT+1'), ('Asia/Ujung_Pandang', 'Asia/Ujung_Pandang'), ('Australia/Brisbane', 'Australia/Brisbane'), ('Australia/Hobart', 'Australia/Hobart'), ('Australia/Melbourne', 'Australia/Melbourne'), ('Antarctica/McMurdo', 'Antarctica/McMurdo'), ('America/Thunder_Bay', 'America/Thunder_Bay'), ('Etc/GMT-0', 'Etc/GMT-0'), ('Asia/Taipei', 'Asia/Taipei'), ('Asia/Dhaka', 'Asia/Dhaka'), ('Australia/Adelaide', 'Australia/Adelaide'), ('Asia/Amman', 'Asia/Amman'), ('Etc/Zulu', 'Etc/Zulu'), ('America/St_Lucia', 'America/St_Lucia'), ('Europe/Brussels', 'Europe/Brussels'), ('Africa/Harare', 'Africa/Harare'), ('Australia/Victoria', 'Australia/Victoria'), ('Etc/GMT+3', 'Etc/GMT+3'), ('America/Anchorage', 'America/Anchorage'), ('Africa/Asmara', 'Africa/Asmara'), ('Australia/North', 'Australia/North'), ('Pacific/Gambier', 'Pacific/Gambier'), ('Pacific/Pago_Pago', 'Pacific/Pago_Pago'), ('Asia/Saigon', 'Asia/Saigon'), ('Atlantic/Canary', 'Atlantic/Canary'), ('Etc/GMT-1', 'Etc/GMT-1'), ('Africa/Johannesburg', 'Africa/Johannesburg'), ('Asia/Anadyr', 'Asia/Anadyr'), ('Europe/Madrid', 'Europe/Madrid'), ('Iran', 'Iran'), ('Antarctica/Rothera', 'Antarctica/Rothera'), ('Atlantic/Stanley', 'Atlantic/Stanley'), ('America/Argentina/Rio_Gallegos', 'America/Argentina/Rio_Gallegos'), ('Atlantic/Bermuda', 'Atlantic/Bermuda'), ('Asia/Katmandu', 'Asia/Katmandu'), ('Portugal', 'Portugal'), ('America/Buenos_Aires', 'America/Buenos_Aires'), ('Asia/Bahrain', 'Asia/Bahrain'), ('America/Metlakatla', 'America/Metlakatla'), ('Australia/Broken_Hill', 'Australia/Broken_Hill'), ('America/Los_Angeles', 'America/Los_Angeles'), ('America/Regina', 'America/Regina'), ('Africa/Asmera', 'Africa/Asmera'), ('Libya', 'Libya'), ('America/Argentina/Jujuy', 'America/Argentina/Jujuy'), ('Australia/South', 'Australia/South'), ('America/Barbados', 'America/Barbados'), ('GMT-0', 'GMT-0'), ('GMT0', 'GMT0'), ('Asia/Khandyga', 'Asia/Khandyga'), ('America/Bogota', 'America/Bogota'), ('America/St_Thomas', 'America/St_Thomas'), ('America/Hermosillo', 'America/Hermosillo'), ('America/Atikokan', 'America/Atikokan'), ('Australia/LHI', 'Australia/LHI'), ('America/Blanc-Sablon', 'America/Blanc-Sablon'), ('Asia/Kuala_Lumpur', 'Asia/Kuala_Lumpur'), ('Australia/Lindeman', 'Australia/Lindeman'), ('Asia/Ashgabat', 'Asia/Ashgabat'), ('Antarctica/Macquarie', 'Antarctica/Macquarie'), ('Asia/Muscat', 'Asia/Muscat'), ('Pacific/Kwajalein', 'Pacific/Kwajalein'), ('Europe/Lisbon', 'Europe/Lisbon'), ('Etc/Universal', 'Etc/Universal'), ('America/Indiana/Indianapolis', 'America/Indiana/Indianapolis'), ('Europe/Budapest', 'Europe/Budapest'), ('Europe/Chisinau', 'Europe/Chisinau'), ('Africa/Casablanca', 'Africa/Casablanca'), ('Atlantic/Reykjavik', 'Atlantic/Reykjavik'), ('America/Coral_Harbour', 'America/Coral_Harbour'), ('Asia/Chongqing', 'Asia/Chongqing'), ('America/Caracas', 'America/Caracas'), ('Iceland', 'Iceland'), ('Asia/Aqtau', 'Asia/Aqtau'), ('Indian/Mahe', 'Indian/Mahe'), ('Asia/Dubai', 'Asia/Dubai'), ('Europe/Simferopol', 'Europe/Simferopol'), ('Asia/Harbin', 'Asia/Harbin'), ('Europe/Riga', 'Europe/Riga'), ('America/Indiana/Winamac', 'America/Indiana/Winamac'), ('Pacific/Noumea', 'Pacific/Noumea'), ('Asia/Rangoon', 'Asia/Rangoon'), ('Europe/Belfast', 'Europe/Belfast'), ('America/Merida', 'America/Merida'), ('Canada/Central', 'Canada/Central'), ('America/Phoenix', 'America/Phoenix'), ('Europe/Luxembourg', 'Europe/Luxembourg'), ('NZ', 'NZ'), ('Australia/Lord_Howe', 'Australia/Lord_Howe'), ('America/Manaus', 'America/Manaus'), ('Atlantic/St_Helena', 'Atlantic/St_Helena'), ('America/El_Salvador', 'America/El_Salvador'), ('America/Guatemala', 'America/Guatemala'), ('US/Alaska', 'US/Alaska'), ('EST5EDT', 'EST5EDT'), ('America/Dawson_Creek', 'America/Dawson_Creek'), ('Etc/GMT-9', 'Etc/GMT-9'), ('Jamaica', 'Jamaica'), ('Asia/Pyongyang', 'Asia/Pyongyang'), ('America/Ensenada', 'America/Ensenada'), ('Asia/Irkutsk', 'Asia/Irkutsk'), ('Asia/Shanghai', 'Asia/Shanghai'), ('Atlantic/Faroe', 'Atlantic/Faroe'), ('US/Samoa', 'US/Samoa'), ('Pacific/Apia', 'Pacific/Apia'), ('Asia/Sakhalin', 'Asia/Sakhalin'), ('Europe/Saratov', 'Europe/Saratov'), ('America/Tijuana', 'America/Tijuana'), ('America/Matamoros', 'America/Matamoros'), ('America/La_Paz', 'America/La_Paz'), ('Africa/Malabo', 'Africa/Malabo'), ('America/St_Barthelemy', 'America/St_Barthelemy'), ('America/Argentina/Catamarca', 'America/Argentina/Catamarca'), ('Japan', 'Japan'), ('America/Monterrey', 'America/Monterrey'), ('Asia/Atyrau', 'Asia/Atyrau'), ('Indian/Maldives', 'Indian/Maldives'), ('Europe/Malta', 'Europe/Malta'), ('Australia/ACT', 'Australia/ACT'), ('Asia/Novosibirsk', 'Asia/Novosibirsk'), ('Europe/Busingen', 'Europe/Busingen'), ('America/Rosario', 'America/Rosario'), ('US/Pacific', 'US/Pacific'), ('Europe/Bratislava', 'Europe/Bratislava'), ('America/Argentina/Ushuaia', 'America/Argentina/Ushuaia'), ('Etc/GMT-3', 'Etc/GMT-3'), ('Indian/Mayotte', 'Indian/Mayotte'), ('Asia/Istanbul', 'Asia/Istanbul'), ('US/Mountain', 'US/Mountain'), ('Europe/Copenhagen', 'Europe/Copenhagen'), ('Asia/Krasnoyarsk', 'Asia/Krasnoyarsk'), ('Pacific/Samoa', 'Pacific/Samoa'), ('America/Argentina/San_Juan', 'America/Argentina/San_Juan'), ('Asia/Vladivostok', 'Asia/Vladivostok'), ('Greenwich', 'Greenwich'), ('Africa/Lubumbashi', 'Africa/Lubumbashi'), ('Africa/Ndjamena', 'Africa/Ndjamena'), ('GB', 'GB'), ('Pacific/Yap', 'Pacific/Yap'), ('Indian/Cocos', 'Indian/Cocos'), ('Pacific/Chuuk', 'Pacific/Chuuk'), ('Asia/Bangkok', 'Asia/Bangkok'), ('Asia/Jerusalem', 'Asia/Jerusalem'), ('Pacific/Wallis', 'Pacific/Wallis'), ('America/Aruba', 'America/Aruba'), ('Asia/Yakutsk', 'Asia/Yakutsk'), ('Asia/Macau', 'Asia/Macau'), ('America/Indiana/Vevay', 'America/Indiana/Vevay'), ('Pacific/Galapagos', 'Pacific/Galapagos'), ('Africa/Gaborone', 'Africa/Gaborone'), ('Europe/Zaporozhye', 'Europe/Zaporozhye'), ('America/Cordoba', 'America/Cordoba'), ('Etc/GMT+11', 'Etc/GMT+11'), ('Pacific/Port_Moresby', 'Pacific/Port_Moresby'), ('Asia/Phnom_Penh', 'Asia/Phnom_Penh'), ('Australia/Tasmania', 'Australia/Tasmania'), ('America/Santiago', 'America/Santiago'), ('America/Boise', 'America/Boise'), ('Asia/Calcutta', 'Asia/Calcutta'), ('Asia/Ho_Chi_Minh', 'Asia/Ho_Chi_Minh'), ('GMT', 'GMT'), ('Pacific/Johnston', 'Pacific/Johnston'), ('Australia/Eucla', 'Australia/Eucla'), ('MST7MDT', 'MST7MDT'), ('America/Atka', 'America/Atka'), ('Pacific/Pohnpei', 'Pacific/Pohnpei'), ('Zulu', 'Zulu'), ('Asia/Gaza', 'Asia/Gaza'), ('Pacific/Enderbury', 'Pacific/Enderbury'), ('Africa/Sao_Tome', 'Africa/Sao_Tome'), ('Brazil/West', 'Brazil/West'), ('Africa/Kampala', 'Africa/Kampala'), ('Etc/GMT+8', 'Etc/GMT+8'), ('America/Marigot', 'America/Marigot'), ('Antarctica/Casey', 'Antarctica/Casey'), ('Europe/Tirane', 'Europe/Tirane'), ('Europe/Andorra', 'Europe/Andorra'), ('Australia/NSW', 'Australia/NSW'), ('Asia/Yerevan', 'Asia/Yerevan'), ('Europe/Skopje', 'Europe/Skopje'), ('America/Moncton', 'America/Moncton'), ('America/Jamaica', 'America/Jamaica'), ('America/Nipigon', 'America/Nipigon'), ('Africa/Abidjan', 'Africa/Abidjan'), ('Asia/Ust-Nera', 'Asia/Ust-Nera'), ('ROK', 'ROK'), ('Asia/Yekaterinburg', 'Asia/Yekaterinburg'), ('America/Rankin_Inlet', 'America/Rankin_Inlet'), ('America/Fortaleza', 'America/Fortaleza'), ('Africa/Windhoek', 'Africa/Windhoek'), ('Asia/Qyzylorda', 'Asia/Qyzylorda'), ('Europe/Istanbul', 'Europe/Istanbul'), ('CST6CDT', 'CST6CDT'), ('Universal', 'Universal'), ('Europe/Sofia', 'Europe/Sofia'), ('Europe/Mariehamn', 'Europe/Mariehamn'), ('Asia/Makassar', 'Asia/Makassar'), ('America/Nome', 'America/Nome'), ('America/Asuncion', 'America/Asuncion'), ('Asia/Famagusta', 'Asia/Famagusta'), ('America/Cambridge_Bay', 'America/Cambridge_Bay'), ('Pacific/Niue', 'Pacific/Niue'), ('America/Sao_Paulo', 'America/Sao_Paulo'), ('Canada/Atlantic', 'Canada/Atlantic'), ('Antarctica/Mawson', 'Antarctica/Mawson'), ('Africa/Khartoum', 'Africa/Khartoum'), ('Asia/Vientiane', 'Asia/Vientiane'), ('Atlantic/Cape_Verde', 'Atlantic/Cape_Verde'), ('America/Puerto_Rico', 'America/Puerto_Rico'), ('America/Bahia', 'America/Bahia'), ('US/Aleutian', 'US/Aleutian'), ('America/Mazatlan', 'America/Mazatlan'), ('Australia/Perth', 'Australia/Perth'), ('Africa/Dar_es_Salaam', 'Africa/Dar_es_Salaam'), ('Antarctica/Troll', 'Antarctica/Troll'), ('Pacific/Fakaofo', 'Pacific/Fakaofo'), ('Pacific/Chatham', 'Pacific/Chatham'), ('Asia/Hovd', 'Asia/Hovd'), ('Canada/Pacific', 'Canada/Pacific'), ('Europe/Kirov', 'Europe/Kirov'), ('Atlantic/South_Georgia', 'Atlantic/South_Georgia'), ('Asia/Kuching', 'Asia/Kuching'), ('Pacific/Kosrae', 'Pacific/Kosrae'), ('Europe/Vilnius', 'Europe/Vilnius'), ('Asia/Baku', 'Asia/Baku'), ('Africa/Mbabane', 'Africa/Mbabane'), ('Europe/Volgograd', 'Europe/Volgograd'), ('America/Antigua', 'America/Antigua'), ('Asia/Tehran', 'Asia/Tehran'), ('Etc/GMT-8', 'Etc/GMT-8'), ('America/Port-au-Prince', 'America/Port-au-Prince'), ('Africa/Tripoli', 'Africa/Tripoli'), ('EET', 'EET'), ('America/Argentina/Salta', 'America/Argentina/Salta'), ('Asia/Urumqi', 'Asia/Urumqi'), ('America/Inuvik', 'America/Inuvik'), ('Europe/Podgorica', 'Europe/Podgorica'), ('Pacific/Majuro', 'Pacific/Majuro'), ('Africa/Bamako', 'Africa/Bamako'), ('Asia/Dushanbe', 'Asia/Dushanbe'), ('Pacific/Norfolk', 'Pacific/Norfolk'), ('Etc/Greenwich', 'Etc/Greenwich'), ('Etc/GMT-10', 'Etc/GMT-10'), ('America/Danmarkshavn', 'America/Danmarkshavn'), ('Asia/Tomsk', 'Asia/Tomsk'), ('Indian/Mauritius', 'Indian/Mauritius'), ('Pacific/Rarotonga', 'Pacific/Rarotonga'), ('America/Juneau', 'America/Juneau'), ('Asia/Baghdad', 'Asia/Baghdad'), ('America/Cayenne', 'America/Cayenne'), ('Etc/GMT-7', 'Etc/GMT-7'), ('America/Eirunepe', 'America/Eirunepe'), ('Etc/GMT-6', 'Etc/GMT-6'), ('Etc/GMT+9', 'Etc/GMT+9'), ('Europe/Zurich', 'Europe/Zurich'), ('America/Kralendijk', 'America/Kralendijk'), ('Africa/Mogadishu', 'Africa/Mogadishu'), ('Pacific/Pitcairn', 'Pacific/Pitcairn'), ('Africa/Blantyre', 'Africa/Blantyre'), ('America/Punta_Arenas', 'America/Punta_Arenas'), ('Africa/Lagos', 'Africa/Lagos'), ('Australia/Darwin', 'Australia/Darwin'), ('Brazil/Acre', 'Brazil/Acre'), ('Asia/Chita', 'Asia/Chita'), ('America/Recife', 'America/Recife'), ('NZ-CHAT', 'NZ-CHAT'), ('America/Whitehorse', 'America/Whitehorse'), ('Brazil/DeNoronha', 'Brazil/DeNoronha'), ('Mexico/BajaNorte', 'Mexico/BajaNorte'), ('Asia/Kamchatka', 'Asia/Kamchatka'), ('Singapore', 'Singapore'), ('America/Noronha', 'America/Noronha'), ('Australia/Yancowinna', 'Australia/Yancowinna'), ('Asia/Magadan', 'Asia/Magadan'), ('Asia/Choibalsan', 'Asia/Choibalsan'), ('America/Nuuk', 'America/Nuuk'), ('America/Indiana/Tell_City', 'America/Indiana/Tell_City'), ('America/Yakutat', 'America/Yakutat'), ('America/Virgin', 'America/Virgin'), ('America/Louisville', 'America/Louisville'), ('Africa/Lusaka', 'Africa/Lusaka'), ('Africa/Bujumbura', 'Africa/Bujumbura'), ('Pacific/Guadalcanal', 'Pacific/Guadalcanal'), ('America/Goose_Bay', 'America/Goose_Bay'), ('Africa/Brazzaville', 'Africa/Brazzaville'), ('Indian/Reunion', 'Indian/Reunion'), ('America/Porto_Velho', 'America/Porto_Velho'), ('MST', 'MST'), ('GB-Eire', 'GB-Eire'), ('Europe/Dublin', 'Europe/Dublin'), ('Europe/Moscow', 'Europe/Moscow'), ('America/Araguaina', 'America/Araguaina'), ('Atlantic/Madeira', 'Atlantic/Madeira'), ('America/Fort_Nelson', 'America/Fort_Nelson'), ('Asia/Jakarta', 'Asia/Jakarta'), ('America/Sitka', 'America/Sitka'), ('Asia/Ashkhabad', 'Asia/Ashkhabad'), ('America/Argentina/San_Luis', 'America/Argentina/San_Luis'), ('US/Arizona', 'US/Arizona'), ('Asia/Kashgar', 'Asia/Kashgar'), ('Europe/Guernsey', 'Europe/Guernsey'), ('Europe/Kaliningrad', 'Europe/Kaliningrad'), ('Asia/Oral', 'Asia/Oral'), ('Chile/EasterIsland', 'Chile/EasterIsland'), ('America/Santa_Isabel', 'America/Santa_Isabel'), ('W-SU', 'W-SU'), ('US/Michigan', 'US/Michigan'), ('Europe/Prague', 'Europe/Prague'), ('Pacific/Easter', 'Pacific/Easter'), ('Africa/Accra', 'Africa/Accra'), ('Europe/Nicosia', 'Europe/Nicosia'), ('Asia/Hebron', 'Asia/Hebron'), ('Asia/Novokuznetsk', 'Asia/Novokuznetsk'), ('Europe/Astrakhan', 'Europe/Astrakhan'), ('Australia/Canberra', 'Australia/Canberra'), ('Canada/Newfoundland', 'Canada/Newfoundland'), ('Asia/Qostanay', 'Asia/Qostanay'), ('Europe/Paris', 'Europe/Paris'), ('America/Montreal', 'America/Montreal'), ('Europe/Minsk', 'Europe/Minsk'), ('Europe/Uzhgorod', 'Europe/Uzhgorod'), ('Etc/GMT-14', 'Etc/GMT-14'), ('America/Port_of_Spain', 'America/Port_of_Spain'), ('Africa/Niamey', 'Africa/Niamey'), ('America/Montserrat', 'America/Montserrat'), ('America/Havana', 'America/Havana'), ('America/Cuiaba', 'America/Cuiaba'), ('Mexico/General', 'Mexico/General'), ('Asia/Kabul', 'Asia/Kabul'), ('Asia/Barnaul', 'Asia/Barnaul'), ('Asia/Jayapura', 'Asia/Jayapura'), ('Pacific/Midway', 'Pacific/Midway'), ('Africa/Conakry', 'Africa/Conakry'), ('Asia/Nicosia', 'Asia/Nicosia'), ('Africa/Lome', 'Africa/Lome'), ('America/Argentina/Cordoba', 'America/Argentina/Cordoba'), ('Asia/Ulaanbaatar', 'Asia/Ulaanbaatar'), ('US/Eastern', 'US/Eastern'), ('Pacific/Tahiti', 'Pacific/Tahiti'), ('America/Iqaluit', 'America/Iqaluit'), ('Africa/Libreville', 'Africa/Libreville'), ('Indian/Chagos', 'Indian/Chagos'), ('Africa/Maseru', 'Africa/Maseru'), ('Canada/Saskatchewan', 'Canada/Saskatchewan'), ('Asia/Hong_Kong', 'Asia/Hong_Kong'), ('Asia/Aqtobe', 'Asia/Aqtobe'), ('CET', 'CET'), ('Etc/GMT-4', 'Etc/GMT-4'), ('Pacific/Palau', 'Pacific/Palau'), ('Europe/Athens', 'Europe/Athens'), ('WET', 'WET'), ('America/North_Dakota/Beulah', 'America/North_Dakota/Beulah'), ('Africa/Banjul', 'Africa/Banjul'), ('Africa/Maputo', 'Africa/Maputo'), ('Africa/El_Aaiun', 'Africa/El_Aaiun'), ('Pacific/Wake', 'Pacific/Wake'), ('Etc/GMT-5', 'Etc/GMT-5'), ('America/Adak', 'America/Adak'), ('Asia/Chungking', 'Asia/Chungking'), ('Turkey', 'Turkey'), ('America/Yellowknife', 'America/Yellowknife'), ('America/Guayaquil', 'America/Guayaquil'), ('Asia/Bishkek', 'Asia/Bishkek'), ('America/Chihuahua', 'America/Chihuahua'), ('Etc/GMT+5', 'Etc/GMT+5'), ('Asia/Ulan_Bator', 'Asia/Ulan_Bator'), ('Mexico/BajaSur', 'Mexico/BajaSur'), ('Canada/Yukon', 'Canada/Yukon'), ('Etc/UTC', 'Etc/UTC'), ('US/Indiana-Starke', 'US/Indiana-Starke'), ('Europe/Vatican', 'Europe/Vatican'), ('Asia/Thimphu', 'Asia/Thimphu'), ('America/Indiana/Petersburg', 'America/Indiana/Petersburg'), ('Australia/Currie', 'Australia/Currie'), ('Asia/Dacca', 'Asia/Dacca'), ('Africa/Dakar', 'Africa/Dakar'), ('Europe/Bucharest', 'Europe/Bucharest'), ('Asia/Omsk', 'Asia/Omsk'), ('Pacific/Tarawa', 'Pacific/Tarawa'), ('Pacific/Efate', 'Pacific/Efate'), ('Asia/Colombo', 'Asia/Colombo'), ('Asia/Macao', 'Asia/Macao'), ('Pacific/Bougainville', 'Pacific/Bougainville'), ('America/Winnipeg', 'America/Winnipeg'), ('America/Paramaribo', 'America/Paramaribo'), ('Europe/Helsinki', 'Europe/Helsinki'), ('Africa/Tunis', 'Africa/Tunis'), ('America/Creston', 'America/Creston'), ('Brazil/East', 'Brazil/East'), ('America/Rainy_River', 'America/Rainy_River'), ('Africa/Nairobi', 'Africa/Nairobi'), ('Antarctica/Davis', 'Antarctica/Davis'), ('America/Santo_Domingo', 'America/Santo_Domingo'), ('UCT', 'UCT'), ('America/Argentina/Mendoza', 'America/Argentina/Mendoza'), ('Africa/Kigali', 'Africa/Kigali'), ('Pacific/Kanton', 'Pacific/Kanton'), ('Asia/Brunei', 'Asia/Brunei'), ('America/Ojinaga', 'America/Ojinaga'), ('America/Thule', 'America/Thule'), ('Asia/Aden', 'Asia/Aden'), ('Europe/Monaco', 'Europe/Monaco'), ('Asia/Karachi', 'Asia/Karachi'), ('Europe/Rome', 'Europe/Rome'), ('Indian/Comoro', 'Indian/Comoro'), ('Africa/Kinshasa', 'Africa/Kinshasa'), ('UTC', 'UTC'), ('Indian/Christmas', 'Indian/Christmas'), ('America/Denver', 'America/Denver'), ('America/Tortola', 'America/Tortola'), ('America/Lima', 'America/Lima'), ('America/Argentina/Tucuman', 'America/Argentina/Tucuman'), ('Europe/Samara', 'Europe/Samara'), ('Eire', 'Eire'), ('America/Menominee', 'America/Menominee'), ('Pacific/Kiritimati', 'Pacific/Kiritimati'), ('Pacific/Nauru', 'Pacific/Nauru'), ('America/New_York', 'America/New_York'), ('Europe/Warsaw', 'Europe/Warsaw'), ('Africa/Bangui', 'Africa/Bangui'), ('Europe/Jersey', 'Europe/Jersey'), ('America/Dawson', 'America/Dawson'), ('Asia/Singapore', 'Asia/Singapore'), ('America/Resolute', 'America/Resolute'), ('Etc/GMT+0', 'Etc/GMT+0'), ('America/Argentina/La_Rioja', 'America/Argentina/La_Rioja'), ('America/Boa_Vista', 'America/Boa_Vista'), ('Africa/Douala', 'Africa/Douala'), ('Etc/GMT+10', 'Etc/GMT+10'), ('America/St_Kitts', 'America/St_Kitts'), ('America/Kentucky/Louisville', 'America/Kentucky/Louisville'), ('Etc/GMT', 'Etc/GMT'), ('America/Fort_Wayne', 'America/Fort_Wayne'), ('America/St_Vincent', 'America/St_Vincent'), ('America/Guyana', 'America/Guyana'), ('Asia/Thimbu', 'Asia/Thimbu'), ('Europe/Ulyanovsk', 'Europe/Ulyanovsk'), ('Antarctica/South_Pole', 'Antarctica/South_Pole'), ('America/North_Dakota/New_Salem', 'America/North_Dakota/New_Salem'), ('GMT+0', 'GMT+0'), ('Etc/GMT+12', 'Etc/GMT+12'), ('Etc/GMT+6', 'Etc/GMT+6'), ('Australia/Sydney', 'Australia/Sydney'), ('Antarctica/DumontDUrville', 'Antarctica/DumontDUrville'), ('ROC', 'ROC'), ('Etc/GMT+7', 'Etc/GMT+7'), ('US/Hawaii', 'US/Hawaii'), ('Pacific/Marquesas', 'Pacific/Marquesas'), ('Europe/Berlin', 'Europe/Berlin'), ('Europe/Sarajevo', 'Europe/Sarajevo'), ('Asia/Tbilisi', 'Asia/Tbilisi'), ('Europe/Kyiv', 'Europe/Kyiv'), ('America/Godthab', 'America/Godthab'), ('Etc/GMT-12', 'Etc/GMT-12'), ('Israel', 'Israel'), ('Etc/GMT+2', 'Etc/GMT+2'), ('MET', 'MET'), ('America/Ciudad_Juarez', 'America/Ciudad_Juarez'), ('Africa/Cairo', 'Africa/Cairo'), ('America/Edmonton', 'America/Edmonton'), ('America/Belize', 'America/Belize'), ('Asia/Tashkent', 'Asia/Tashkent'), ('America/Managua', 'America/Managua'), ('America/Rio_Branco', 'America/Rio_Branco'), ('Europe/Tiraspol', 'Europe/Tiraspol'), ('America/Catamarca', 'America/Catamarca'), ('America/Anguilla', 'America/Anguilla'), ('America/Cayman', 'America/Cayman'), ('Asia/Dili', 'Asia/Dili'), ('Asia/Riyadh', 'Asia/Riyadh'), ('America/Montevideo', 'America/Montevideo'), ('Asia/Manila', 'Asia/Manila'), ('Indian/Antananarivo', 'Indian/Antananarivo'), ('America/Halifax', 'America/Halifax'), ('America/Campo_Grande', 'America/Campo_Grande'), ('Asia/Kuwait', 'Asia/Kuwait'), ('America/Cancun', 'America/Cancun'), ('Asia/Seoul', 'Asia/Seoul'), ('America/Vancouver', 'America/Vancouver'), ('Antarctica/Syowa', 'Antarctica/Syowa'), ('Africa/Ceuta', 'Africa/Ceuta'), ('Cuba', 'Cuba'), ('Africa/Monrovia', 'Africa/Monrovia'), ('Asia/Almaty', 'Asia/Almaty'), ('Asia/Tel_Aviv', 'Asia/Tel_Aviv'), ('Pacific/Fiji', 'Pacific/Fiji'), ('America/Bahia_Banderas', 'America/Bahia_Banderas'), ('Canada/Mountain', 'Canada/Mountain'), ('Etc/GMT0', 'Etc/GMT0'), ('Europe/Belgrade', 'Europe/Belgrade'), ('Canada/Eastern', 'Canada/Eastern'), ('Europe/Vienna', 'Europe/Vienna'), ('Africa/Bissau', 'Africa/Bissau'), ('America/Guadeloupe', 'America/Guadeloupe'), ('America/North_Dakota/Center', 'America/North_Dakota/Center'), ('Asia/Qatar', 'Asia/Qatar'), ('Africa/Addis_Ababa', 'Africa/Addis_Ababa'), ('Africa/Timbuktu', 'Africa/Timbuktu'), ('Asia/Kolkata', 'Asia/Kolkata'), ('America/Pangnirtung', 'America/Pangnirtung'), ('America/Detroit', 'America/Detroit'), ('America/Knox_IN', 'America/Knox_IN'), ('Pacific/Truk', 'Pacific/Truk'), ('Europe/Ljubljana', 'Europe/Ljubljana'), ('America/Santarem', 'America/Santarem'), ('Africa/Luanda', 'Africa/Luanda'), ('America/Miquelon', 'America/Miquelon'), ('Pacific/Honolulu', 'Pacific/Honolulu'), ('America/Toronto', 'America/Toronto'), ('Europe/Gibraltar', 'Europe/Gibraltar'), ('America/Grenada', 'America/Grenada'), ('Asia/Pontianak', 'Asia/Pontianak'), ('America/Grand_Turk', 'America/Grand_Turk'), ('Asia/Kathmandu', 'Asia/Kathmandu'), ('Etc/GMT-11', 'Etc/GMT-11'), ('America/Indiana/Marengo', 'America/Indiana/Marengo'), ('EST', 'EST'), ('Africa/Djibouti', 'Africa/Djibouti'), ('Europe/London', 'Europe/London'), ('Europe/San_Marino', 'Europe/San_Marino'), ('America/Belem', 'America/Belem'), ('Europe/Amsterdam', 'Europe/Amsterdam'), ('America/Panama', 'America/Panama'), ('Arctic/Longyearbyen', 'Arctic/Longyearbyen'), ('America/Curacao', 'America/Curacao'), ('Europe/Kiev', 'Europe/Kiev'), ('Pacific/Tongatapu', 'Pacific/Tongatapu'), ('Hongkong', 'Hongkong'), ('Africa/Juba', 'Africa/Juba'), ('Indian/Kerguelen', 'Indian/Kerguelen'), ('Asia/Srednekolymsk', 'Asia/Srednekolymsk'), ('Asia/Beirut', 'Asia/Beirut'), ('America/Kentucky/Monticello', 'America/Kentucky/Monticello'), ('Etc/GMT+4', 'Etc/GMT+4'), ('Asia/Samarkand', 'Asia/Samarkand'), ('America/Tegucigalpa', 'America/Tegucigalpa'), ('Pacific/Auckland', 'Pacific/Auckland'), ('Pacific/Funafuti', 'Pacific/Funafuti'), ('Africa/Algiers', 'Africa/Algiers'), ('Europe/Vaduz', 'Europe/Vaduz'), ('Africa/Porto-Novo', 'Africa/Porto-Novo'), ('America/Dominica', 'America/Dominica'), ('America/Mendoza', 'America/Mendoza'), ('America/Lower_Princes', 'America/Lower_Princes'), ('Australia/Queensland', 'Australia/Queensland'), ('America/Indianapolis', 'America/Indianapolis'), ('Navajo', 'Navajo'), ('America/Argentina/ComodRivadavia', 'America/Argentina/ComodRivadavia')], default='Asia/Kolkata', max_length=50, verbose_name='Time zone'),
        ),
    ]