# Generated by Django 4.2.6 on 2023-10-13 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "creme_core",
            "0008_remove_attachments_account_remove_attachments_case_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="time_zone",
            field=models.CharField(
                choices=[
                    ("America/Rankin_Inlet", "America/Rankin_Inlet"),
                    ("Africa/Freetown", "Africa/Freetown"),
                    ("America/Coral_Harbour", "America/Coral_Harbour"),
                    ("Europe/Budapest", "Europe/Budapest"),
                    ("Pacific/Kwajalein", "Pacific/Kwajalein"),
                    ("Europe/Saratov", "Europe/Saratov"),
                    ("America/Metlakatla", "America/Metlakatla"),
                    ("Etc/GMT+10", "Etc/GMT+10"),
                    ("Africa/Ceuta", "Africa/Ceuta"),
                    ("Australia/North", "Australia/North"),
                    ("Asia/Pyongyang", "Asia/Pyongyang"),
                    ("America/Port-au-Prince", "America/Port-au-Prince"),
                    ("Europe/Oslo", "Europe/Oslo"),
                    ("CET", "CET"),
                    ("Asia/Beirut", "Asia/Beirut"),
                    ("America/Punta_Arenas", "America/Punta_Arenas"),
                    ("Australia/Queensland", "Australia/Queensland"),
                    ("Europe/Chisinau", "Europe/Chisinau"),
                    ("GB", "GB"),
                    ("America/Paramaribo", "America/Paramaribo"),
                    ("GMT", "GMT"),
                    ("PST8PDT", "PST8PDT"),
                    ("Europe/Athens", "Europe/Athens"),
                    ("America/Bogota", "America/Bogota"),
                    ("Europe/Amsterdam", "Europe/Amsterdam"),
                    ("America/Winnipeg", "America/Winnipeg"),
                    ("America/Catamarca", "America/Catamarca"),
                    ("Europe/Luxembourg", "Europe/Luxembourg"),
                    ("Pacific/Wake", "Pacific/Wake"),
                    ("Asia/Kabul", "Asia/Kabul"),
                    ("Asia/Thimphu", "Asia/Thimphu"),
                    ("Etc/GMT-0", "Etc/GMT-0"),
                    ("Canada/Pacific", "Canada/Pacific"),
                    ("America/Buenos_Aires", "America/Buenos_Aires"),
                    ("Africa/Bujumbura", "Africa/Bujumbura"),
                    ("Africa/Lubumbashi", "Africa/Lubumbashi"),
                    ("Asia/Dubai", "Asia/Dubai"),
                    ("America/Port_of_Spain", "America/Port_of_Spain"),
                    ("America/Anchorage", "America/Anchorage"),
                    ("Etc/GMT+4", "Etc/GMT+4"),
                    ("America/Ojinaga", "America/Ojinaga"),
                    ("Australia/Eucla", "Australia/Eucla"),
                    ("America/Guatemala", "America/Guatemala"),
                    ("Antarctica/DumontDUrville", "Antarctica/DumontDUrville"),
                    ("US/Mountain", "US/Mountain"),
                    ("America/Santa_Isabel", "America/Santa_Isabel"),
                    ("Asia/Ashgabat", "Asia/Ashgabat"),
                    ("Asia/Baku", "Asia/Baku"),
                    ("EET", "EET"),
                    ("America/Nome", "America/Nome"),
                    ("America/Hermosillo", "America/Hermosillo"),
                    ("America/Cuiaba", "America/Cuiaba"),
                    ("Etc/GMT-13", "Etc/GMT-13"),
                    ("Europe/Bratislava", "Europe/Bratislava"),
                    ("America/Cayman", "America/Cayman"),
                    ("CST6CDT", "CST6CDT"),
                    ("Europe/Skopje", "Europe/Skopje"),
                    ("Africa/Lome", "Africa/Lome"),
                    ("Asia/Tokyo", "Asia/Tokyo"),
                    ("America/Panama", "America/Panama"),
                    ("Asia/Sakhalin", "Asia/Sakhalin"),
                    ("America/Cambridge_Bay", "America/Cambridge_Bay"),
                    ("Japan", "Japan"),
                    ("US/Michigan", "US/Michigan"),
                    ("Cuba", "Cuba"),
                    ("America/Sitka", "America/Sitka"),
                    ("America/Barbados", "America/Barbados"),
                    ("Etc/GMT+6", "Etc/GMT+6"),
                    ("Factory", "Factory"),
                    ("Asia/Bishkek", "Asia/Bishkek"),
                    (
                        "America/Argentina/Rio_Gallegos",
                        "America/Argentina/Rio_Gallegos",
                    ),
                    ("Europe/Vienna", "Europe/Vienna"),
                    ("America/Indiana/Petersburg", "America/Indiana/Petersburg"),
                    ("Europe/Volgograd", "Europe/Volgograd"),
                    ("Europe/Podgorica", "Europe/Podgorica"),
                    ("GB-Eire", "GB-Eire"),
                    ("Pacific/Kosrae", "Pacific/Kosrae"),
                    ("America/Dawson_Creek", "America/Dawson_Creek"),
                    ("Pacific/Johnston", "Pacific/Johnston"),
                    ("Indian/Chagos", "Indian/Chagos"),
                    ("Europe/Prague", "Europe/Prague"),
                    ("Asia/Vientiane", "Asia/Vientiane"),
                    ("GMT0", "GMT0"),
                    ("Asia/Seoul", "Asia/Seoul"),
                    ("America/Fort_Nelson", "America/Fort_Nelson"),
                    ("America/Boise", "America/Boise"),
                    ("Portugal", "Portugal"),
                    ("America/Maceio", "America/Maceio"),
                    ("America/Fortaleza", "America/Fortaleza"),
                    ("Mexico/BajaSur", "Mexico/BajaSur"),
                    ("America/Ciudad_Juarez", "America/Ciudad_Juarez"),
                    ("Asia/Kashgar", "Asia/Kashgar"),
                    ("America/Puerto_Rico", "America/Puerto_Rico"),
                    ("Asia/Choibalsan", "Asia/Choibalsan"),
                    ("Antarctica/McMurdo", "Antarctica/McMurdo"),
                    ("Asia/Pontianak", "Asia/Pontianak"),
                    ("America/Nassau", "America/Nassau"),
                    ("Canada/Newfoundland", "Canada/Newfoundland"),
                    ("America/Chicago", "America/Chicago"),
                    ("Etc/GMT0", "Etc/GMT0"),
                    ("Asia/Nicosia", "Asia/Nicosia"),
                    ("Asia/Anadyr", "Asia/Anadyr"),
                    ("America/Bahia", "America/Bahia"),
                    ("America/Sao_Paulo", "America/Sao_Paulo"),
                    ("Australia/Adelaide", "Australia/Adelaide"),
                    ("Australia/ACT", "Australia/ACT"),
                    ("Eire", "Eire"),
                    ("Africa/Malabo", "Africa/Malabo"),
                    ("Asia/Qatar", "Asia/Qatar"),
                    ("Europe/Simferopol", "Europe/Simferopol"),
                    ("Asia/Tomsk", "Asia/Tomsk"),
                    ("America/Argentina/Tucuman", "America/Argentina/Tucuman"),
                    ("EST5EDT", "EST5EDT"),
                    ("Africa/Blantyre", "Africa/Blantyre"),
                    ("Pacific/Saipan", "Pacific/Saipan"),
                    ("Pacific/Wallis", "Pacific/Wallis"),
                    ("Antarctica/South_Pole", "Antarctica/South_Pole"),
                    ("Pacific/Tarawa", "Pacific/Tarawa"),
                    ("Europe/Monaco", "Europe/Monaco"),
                    ("Asia/Bangkok", "Asia/Bangkok"),
                    ("Canada/Atlantic", "Canada/Atlantic"),
                    ("America/Grenada", "America/Grenada"),
                    ("America/Atikokan", "America/Atikokan"),
                    ("Africa/Djibouti", "Africa/Djibouti"),
                    ("MST7MDT", "MST7MDT"),
                    ("Pacific/Chatham", "Pacific/Chatham"),
                    ("America/Asuncion", "America/Asuncion"),
                    ("America/Mendoza", "America/Mendoza"),
                    ("Africa/Libreville", "Africa/Libreville"),
                    ("Africa/Cairo", "Africa/Cairo"),
                    ("America/Goose_Bay", "America/Goose_Bay"),
                    ("Africa/Casablanca", "Africa/Casablanca"),
                    ("America/Edmonton", "America/Edmonton"),
                    ("America/Montreal", "America/Montreal"),
                    ("Canada/Central", "Canada/Central"),
                    ("Etc/GMT+5", "Etc/GMT+5"),
                    ("Australia/Tasmania", "Australia/Tasmania"),
                    ("US/Aleutian", "US/Aleutian"),
                    ("Atlantic/Faroe", "Atlantic/Faroe"),
                    ("America/Montserrat", "America/Montserrat"),
                    ("Australia/Sydney", "Australia/Sydney"),
                    ("Asia/Novokuznetsk", "Asia/Novokuznetsk"),
                    ("Africa/Lusaka", "Africa/Lusaka"),
                    ("Asia/Bahrain", "Asia/Bahrain"),
                    ("Africa/Mogadishu", "Africa/Mogadishu"),
                    ("America/Yellowknife", "America/Yellowknife"),
                    ("Brazil/West", "Brazil/West"),
                    ("Europe/Istanbul", "Europe/Istanbul"),
                    ("America/Montevideo", "America/Montevideo"),
                    ("Asia/Almaty", "Asia/Almaty"),
                    ("Atlantic/Reykjavik", "Atlantic/Reykjavik"),
                    ("Asia/Qostanay", "Asia/Qostanay"),
                    ("America/Costa_Rica", "America/Costa_Rica"),
                    ("Africa/Gaborone", "Africa/Gaborone"),
                    ("America/Godthab", "America/Godthab"),
                    ("Pacific/Kanton", "Pacific/Kanton"),
                    ("America/Thule", "America/Thule"),
                    ("America/Argentina/Jujuy", "America/Argentina/Jujuy"),
                    ("Antarctica/Mawson", "Antarctica/Mawson"),
                    ("Africa/Harare", "Africa/Harare"),
                    ("America/Shiprock", "America/Shiprock"),
                    ("Iran", "Iran"),
                    ("Africa/Johannesburg", "Africa/Johannesburg"),
                    ("Europe/Copenhagen", "Europe/Copenhagen"),
                    ("Asia/Brunei", "Asia/Brunei"),
                    ("Asia/Chongqing", "Asia/Chongqing"),
                    ("America/Knox_IN", "America/Knox_IN"),
                    ("America/Thunder_Bay", "America/Thunder_Bay"),
                    ("Antarctica/Vostok", "Antarctica/Vostok"),
                    ("Asia/Saigon", "Asia/Saigon"),
                    ("Asia/Oral", "Asia/Oral"),
                    ("Etc/GMT+3", "Etc/GMT+3"),
                    ("NZ-CHAT", "NZ-CHAT"),
                    ("PRC", "PRC"),
                    ("Asia/Srednekolymsk", "Asia/Srednekolymsk"),
                    ("GMT+0", "GMT+0"),
                    ("America/Havana", "America/Havana"),
                    ("Africa/Dar_es_Salaam", "Africa/Dar_es_Salaam"),
                    ("Europe/Berlin", "Europe/Berlin"),
                    ("America/Recife", "America/Recife"),
                    ("Canada/Saskatchewan", "Canada/Saskatchewan"),
                    ("Europe/Paris", "Europe/Paris"),
                    ("Asia/Muscat", "Asia/Muscat"),
                    ("Asia/Vladivostok", "Asia/Vladivostok"),
                    ("Asia/Istanbul", "Asia/Istanbul"),
                    ("Asia/Taipei", "Asia/Taipei"),
                    ("America/Caracas", "America/Caracas"),
                    ("America/Vancouver", "America/Vancouver"),
                    ("America/Juneau", "America/Juneau"),
                    ("Europe/Gibraltar", "Europe/Gibraltar"),
                    ("Europe/Madrid", "Europe/Madrid"),
                    ("America/Argentina/Ushuaia", "America/Argentina/Ushuaia"),
                    ("US/Samoa", "US/Samoa"),
                    ("Europe/Stockholm", "Europe/Stockholm"),
                    ("America/Argentina/Salta", "America/Argentina/Salta"),
                    ("Africa/Nairobi", "Africa/Nairobi"),
                    ("America/Marigot", "America/Marigot"),
                    (
                        "America/Argentina/Buenos_Aires",
                        "America/Argentina/Buenos_Aires",
                    ),
                    ("America/Menominee", "America/Menominee"),
                    ("NZ", "NZ"),
                    ("America/Indiana/Vevay", "America/Indiana/Vevay"),
                    ("Australia/Yancowinna", "Australia/Yancowinna"),
                    ("Asia/Urumqi", "Asia/Urumqi"),
                    ("America/Managua", "America/Managua"),
                    ("Europe/Malta", "Europe/Malta"),
                    ("America/Fort_Wayne", "America/Fort_Wayne"),
                    ("Etc/GMT", "Etc/GMT"),
                    ("Indian/Mauritius", "Indian/Mauritius"),
                    ("Africa/Ouagadougou", "Africa/Ouagadougou"),
                    ("America/Belize", "America/Belize"),
                    ("Europe/Bucharest", "Europe/Bucharest"),
                    ("America/Halifax", "America/Halifax"),
                    ("Pacific/Noumea", "Pacific/Noumea"),
                    ("Europe/Minsk", "Europe/Minsk"),
                    ("Mexico/General", "Mexico/General"),
                    ("US/Hawaii", "US/Hawaii"),
                    ("America/Monterrey", "America/Monterrey"),
                    ("America/Argentina/Mendoza", "America/Argentina/Mendoza"),
                    ("Atlantic/Madeira", "Atlantic/Madeira"),
                    ("Europe/Ljubljana", "Europe/Ljubljana"),
                    ("America/Santarem", "America/Santarem"),
                    ("Asia/Riyadh", "Asia/Riyadh"),
                    ("Brazil/DeNoronha", "Brazil/DeNoronha"),
                    ("Etc/UTC", "Etc/UTC"),
                    ("Canada/Eastern", "Canada/Eastern"),
                    ("America/Swift_Current", "America/Swift_Current"),
                    ("Asia/Shanghai", "Asia/Shanghai"),
                    ("America/Indianapolis", "America/Indianapolis"),
                    ("Asia/Barnaul", "Asia/Barnaul"),
                    ("Asia/Ujung_Pandang", "Asia/Ujung_Pandang"),
                    ("America/Tijuana", "America/Tijuana"),
                    ("Europe/Belfast", "Europe/Belfast"),
                    ("Pacific/Port_Moresby", "Pacific/Port_Moresby"),
                    ("Poland", "Poland"),
                    ("Europe/Brussels", "Europe/Brussels"),
                    ("America/Belem", "America/Belem"),
                    ("America/Resolute", "America/Resolute"),
                    ("America/Porto_Velho", "America/Porto_Velho"),
                    ("ROK", "ROK"),
                    ("Asia/Dacca", "Asia/Dacca"),
                    ("Pacific/Yap", "Pacific/Yap"),
                    ("Asia/Thimbu", "Asia/Thimbu"),
                    ("Africa/Luanda", "Africa/Luanda"),
                    ("Asia/Karachi", "Asia/Karachi"),
                    ("Indian/Christmas", "Indian/Christmas"),
                    ("Pacific/Auckland", "Pacific/Auckland"),
                    ("America/Detroit", "America/Detroit"),
                    ("America/Argentina/La_Rioja", "America/Argentina/La_Rioja"),
                    ("Canada/Yukon", "Canada/Yukon"),
                    ("MST", "MST"),
                    ("America/Aruba", "America/Aruba"),
                    ("America/Rosario", "America/Rosario"),
                    ("Indian/Maldives", "Indian/Maldives"),
                    ("Europe/San_Marino", "Europe/San_Marino"),
                    ("Australia/Melbourne", "Australia/Melbourne"),
                    ("Asia/Calcutta", "Asia/Calcutta"),
                    ("Atlantic/Bermuda", "Atlantic/Bermuda"),
                    ("Africa/Monrovia", "Africa/Monrovia"),
                    ("Pacific/Honolulu", "Pacific/Honolulu"),
                    ("HST", "HST"),
                    ("Europe/Mariehamn", "Europe/Mariehamn"),
                    ("UTC", "UTC"),
                    ("Asia/Phnom_Penh", "Asia/Phnom_Penh"),
                    ("Arctic/Longyearbyen", "Arctic/Longyearbyen"),
                    ("Europe/Warsaw", "Europe/Warsaw"),
                    ("America/Dominica", "America/Dominica"),
                    ("Pacific/Niue", "Pacific/Niue"),
                    ("America/Santo_Domingo", "America/Santo_Domingo"),
                    ("Asia/Ulan_Bator", "Asia/Ulan_Bator"),
                    ("Etc/GMT+9", "Etc/GMT+9"),
                    ("Africa/Ndjamena", "Africa/Ndjamena"),
                    ("America/Jujuy", "America/Jujuy"),
                    ("Asia/Yekaterinburg", "Asia/Yekaterinburg"),
                    ("Asia/Baghdad", "Asia/Baghdad"),
                    ("Pacific/Midway", "Pacific/Midway"),
                    ("Pacific/Funafuti", "Pacific/Funafuti"),
                    ("America/Manaus", "America/Manaus"),
                    ("Pacific/Nauru", "Pacific/Nauru"),
                    ("Etc/GMT+11", "Etc/GMT+11"),
                    ("Europe/Rome", "Europe/Rome"),
                    ("Asia/Aqtau", "Asia/Aqtau"),
                    ("Australia/South", "Australia/South"),
                    ("MET", "MET"),
                    ("Africa/El_Aaiun", "Africa/El_Aaiun"),
                    ("Africa/Asmara", "Africa/Asmara"),
                    ("Europe/Zurich", "Europe/Zurich"),
                    ("Pacific/Majuro", "Pacific/Majuro"),
                    ("America/St_Johns", "America/St_Johns"),
                    ("Asia/Jayapura", "Asia/Jayapura"),
                    ("Asia/Gaza", "Asia/Gaza"),
                    ("Asia/Ust-Nera", "Asia/Ust-Nera"),
                    ("Etc/Greenwich", "Etc/Greenwich"),
                    ("Asia/Dili", "Asia/Dili"),
                    ("Pacific/Fakaofo", "Pacific/Fakaofo"),
                    ("America/Grand_Turk", "America/Grand_Turk"),
                    ("Africa/Kampala", "Africa/Kampala"),
                    ("America/Tortola", "America/Tortola"),
                    ("America/Rio_Branco", "America/Rio_Branco"),
                    ("Europe/Nicosia", "Europe/Nicosia"),
                    ("Antarctica/Troll", "Antarctica/Troll"),
                    ("US/Arizona", "US/Arizona"),
                    ("America/Kentucky/Monticello", "America/Kentucky/Monticello"),
                    ("Pacific/Rarotonga", "Pacific/Rarotonga"),
                    ("Asia/Magadan", "Asia/Magadan"),
                    ("America/Lima", "America/Lima"),
                    ("America/Nuuk", "America/Nuuk"),
                    ("Asia/Khandyga", "Asia/Khandyga"),
                    ("America/Kralendijk", "America/Kralendijk"),
                    ("Africa/Tripoli", "Africa/Tripoli"),
                    ("America/Merida", "America/Merida"),
                    ("Africa/Nouakchott", "Africa/Nouakchott"),
                    ("Asia/Macao", "Asia/Macao"),
                    ("US/Alaska", "US/Alaska"),
                    ("Etc/GMT-8", "Etc/GMT-8"),
                    ("America/Kentucky/Louisville", "America/Kentucky/Louisville"),
                    ("Indian/Kerguelen", "Indian/Kerguelen"),
                    ("America/North_Dakota/Beulah", "America/North_Dakota/Beulah"),
                    ("UCT", "UCT"),
                    ("America/Danmarkshavn", "America/Danmarkshavn"),
                    ("Pacific/Tongatapu", "Pacific/Tongatapu"),
                    ("Mexico/BajaNorte", "Mexico/BajaNorte"),
                    ("America/Indiana/Knox", "America/Indiana/Knox"),
                    ("Asia/Singapore", "Asia/Singapore"),
                    ("America/Iqaluit", "America/Iqaluit"),
                    ("Pacific/Galapagos", "Pacific/Galapagos"),
                    ("Australia/Victoria", "Australia/Victoria"),
                    ("Europe/Guernsey", "Europe/Guernsey"),
                    ("US/Eastern", "US/Eastern"),
                    ("Africa/Lagos", "Africa/Lagos"),
                    ("Africa/Algiers", "Africa/Algiers"),
                    ("Etc/GMT-2", "Etc/GMT-2"),
                    ("Europe/Helsinki", "Europe/Helsinki"),
                    ("America/St_Vincent", "America/St_Vincent"),
                    ("Africa/Sao_Tome", "Africa/Sao_Tome"),
                    ("Etc/GMT-7", "Etc/GMT-7"),
                    ("Asia/Hovd", "Asia/Hovd"),
                    ("America/Inuvik", "America/Inuvik"),
                    ("Europe/Kaliningrad", "Europe/Kaliningrad"),
                    ("Africa/Conakry", "Africa/Conakry"),
                    ("America/Argentina/Cordoba", "America/Argentina/Cordoba"),
                    ("Europe/Tirane", "Europe/Tirane"),
                    ("Africa/Khartoum", "Africa/Khartoum"),
                    ("Europe/Ulyanovsk", "Europe/Ulyanovsk"),
                    ("Indian/Reunion", "Indian/Reunion"),
                    ("Pacific/Easter", "Pacific/Easter"),
                    ("Pacific/Chuuk", "Pacific/Chuuk"),
                    ("Pacific/Truk", "Pacific/Truk"),
                    ("Asia/Hong_Kong", "Asia/Hong_Kong"),
                    ("Chile/EasterIsland", "Chile/EasterIsland"),
                    ("Asia/Damascus", "Asia/Damascus"),
                    ("America/Porto_Acre", "America/Porto_Acre"),
                    ("Etc/GMT-4", "Etc/GMT-4"),
                    ("Asia/Kuwait", "Asia/Kuwait"),
                    ("America/Noronha", "America/Noronha"),
                    ("Europe/Riga", "Europe/Riga"),
                    ("America/Guayaquil", "America/Guayaquil"),
                    ("W-SU", "W-SU"),
                    ("Europe/Vilnius", "Europe/Vilnius"),
                    ("America/Rainy_River", "America/Rainy_River"),
                    ("Europe/Samara", "Europe/Samara"),
                    ("America/Toronto", "America/Toronto"),
                    ("America/St_Thomas", "America/St_Thomas"),
                    ("America/Lower_Princes", "America/Lower_Princes"),
                    ("Asia/Ulaanbaatar", "Asia/Ulaanbaatar"),
                    ("America/Boa_Vista", "America/Boa_Vista"),
                    ("Etc/GMT-5", "Etc/GMT-5"),
                    ("Australia/Brisbane", "Australia/Brisbane"),
                    ("America/Pangnirtung", "America/Pangnirtung"),
                    ("Pacific/Enderbury", "Pacific/Enderbury"),
                    ("Navajo", "Navajo"),
                    ("Etc/GMT+1", "Etc/GMT+1"),
                    ("Asia/Kuching", "Asia/Kuching"),
                    ("America/Cancun", "America/Cancun"),
                    ("US/Central", "US/Central"),
                    ("America/Ensenada", "America/Ensenada"),
                    ("America/Jamaica", "America/Jamaica"),
                    ("Africa/Bangui", "Africa/Bangui"),
                    ("America/Denver", "America/Denver"),
                    ("Pacific/Guam", "Pacific/Guam"),
                    ("America/Indiana/Vincennes", "America/Indiana/Vincennes"),
                    ("Asia/Kolkata", "Asia/Kolkata"),
                    ("Atlantic/Stanley", "Atlantic/Stanley"),
                    ("Etc/GMT-9", "Etc/GMT-9"),
                    ("Atlantic/Jan_Mayen", "Atlantic/Jan_Mayen"),
                    ("Asia/Chungking", "Asia/Chungking"),
                    ("Europe/Zagreb", "Europe/Zagreb"),
                    ("Greenwich", "Greenwich"),
                    ("America/Los_Angeles", "America/Los_Angeles"),
                    ("America/Regina", "America/Regina"),
                    ("Africa/Asmera", "Africa/Asmera"),
                    ("Asia/Irkutsk", "Asia/Irkutsk"),
                    ("Etc/GMT-6", "Etc/GMT-6"),
                    ("Asia/Aqtobe", "Asia/Aqtobe"),
                    ("Africa/Bissau", "Africa/Bissau"),
                    ("Singapore", "Singapore"),
                    ("America/Martinique", "America/Martinique"),
                    ("America/Nipigon", "America/Nipigon"),
                    ("EST", "EST"),
                    ("Pacific/Bougainville", "Pacific/Bougainville"),
                    ("America/El_Salvador", "America/El_Salvador"),
                    ("Australia/Canberra", "Australia/Canberra"),
                    ("Etc/Zulu", "Etc/Zulu"),
                    ("US/East-Indiana", "US/East-Indiana"),
                    ("Africa/Tunis", "Africa/Tunis"),
                    ("America/Araguaina", "America/Araguaina"),
                    ("Africa/Maputo", "Africa/Maputo"),
                    ("Asia/Amman", "Asia/Amman"),
                    ("Africa/Bamako", "Africa/Bamako"),
                    ("Pacific/Ponape", "Pacific/Ponape"),
                    ("Pacific/Gambier", "Pacific/Gambier"),
                    ("Africa/Banjul", "Africa/Banjul"),
                    ("Africa/Windhoek", "Africa/Windhoek"),
                    ("Pacific/Fiji", "Pacific/Fiji"),
                    ("Europe/Moscow", "Europe/Moscow"),
                    ("Antarctica/Macquarie", "Antarctica/Macquarie"),
                    ("Etc/GMT-1", "Etc/GMT-1"),
                    ("Antarctica/Davis", "Antarctica/Davis"),
                    ("Pacific/Efate", "Pacific/Efate"),
                    ("Europe/Andorra", "Europe/Andorra"),
                    ("America/La_Paz", "America/La_Paz"),
                    ("America/Argentina/San_Juan", "America/Argentina/San_Juan"),
                    ("Etc/GMT+8", "Etc/GMT+8"),
                    ("Pacific/Marquesas", "Pacific/Marquesas"),
                    ("America/Creston", "America/Creston"),
                    (
                        "America/Argentina/ComodRivadavia",
                        "America/Argentina/ComodRivadavia",
                    ),
                    ("America/Tegucigalpa", "America/Tegucigalpa"),
                    ("Europe/Zaporozhye", "Europe/Zaporozhye"),
                    ("Etc/UCT", "Etc/UCT"),
                    ("Zulu", "Zulu"),
                    ("Asia/Ashkhabad", "Asia/Ashkhabad"),
                    ("Asia/Harbin", "Asia/Harbin"),
                    ("Antarctica/Rothera", "Antarctica/Rothera"),
                    ("Asia/Ho_Chi_Minh", "Asia/Ho_Chi_Minh"),
                    ("America/Guyana", "America/Guyana"),
                    ("Atlantic/St_Helena", "Atlantic/St_Helena"),
                    ("Asia/Atyrau", "Asia/Atyrau"),
                    ("Asia/Tel_Aviv", "Asia/Tel_Aviv"),
                    ("Australia/Currie", "Australia/Currie"),
                    ("Asia/Tashkent", "Asia/Tashkent"),
                    ("Etc/Universal", "Etc/Universal"),
                    ("Asia/Kamchatka", "Asia/Kamchatka"),
                    ("America/Campo_Grande", "America/Campo_Grande"),
                    ("Turkey", "Turkey"),
                    ("GMT-0", "GMT-0"),
                    ("Europe/Isle_of_Man", "Europe/Isle_of_Man"),
                    ("Asia/Samarkand", "Asia/Samarkand"),
                    ("America/Indiana/Marengo", "America/Indiana/Marengo"),
                    ("Asia/Kuala_Lumpur", "Asia/Kuala_Lumpur"),
                    ("Atlantic/Canary", "Atlantic/Canary"),
                    ("Asia/Tehran", "Asia/Tehran"),
                    ("Europe/Kirov", "Europe/Kirov"),
                    ("America/Cordoba", "America/Cordoba"),
                    ("Africa/Mbabane", "Africa/Mbabane"),
                    ("Pacific/Pohnpei", "Pacific/Pohnpei"),
                    ("Australia/Lord_Howe", "Australia/Lord_Howe"),
                    ("Atlantic/Cape_Verde", "Atlantic/Cape_Verde"),
                    ("Europe/Kyiv", "Europe/Kyiv"),
                    ("Hongkong", "Hongkong"),
                    ("America/Miquelon", "America/Miquelon"),
                    ("Europe/Tallinn", "Europe/Tallinn"),
                    ("Africa/Brazzaville", "Africa/Brazzaville"),
                    ("Europe/Kiev", "Europe/Kiev"),
                    ("Australia/Broken_Hill", "Australia/Broken_Hill"),
                    ("Asia/Macau", "Asia/Macau"),
                    ("Asia/Kathmandu", "Asia/Kathmandu"),
                    (
                        "America/North_Dakota/New_Salem",
                        "America/North_Dakota/New_Salem",
                    ),
                    ("Etc/GMT+7", "Etc/GMT+7"),
                    ("Pacific/Palau", "Pacific/Palau"),
                    ("Libya", "Libya"),
                    ("Asia/Rangoon", "Asia/Rangoon"),
                    ("America/Eirunepe", "America/Eirunepe"),
                    ("Europe/Sofia", "Europe/Sofia"),
                    ("Asia/Famagusta", "Asia/Famagusta"),
                    ("Pacific/Pitcairn", "Pacific/Pitcairn"),
                    ("America/Bahia_Banderas", "America/Bahia_Banderas"),
                    ("America/Indiana/Indianapolis", "America/Indiana/Indianapolis"),
                    ("America/Blanc-Sablon", "America/Blanc-Sablon"),
                    ("Etc/GMT-10", "Etc/GMT-10"),
                    ("Australia/LHI", "Australia/LHI"),
                    ("Indian/Mahe", "Indian/Mahe"),
                    ("Brazil/East", "Brazil/East"),
                    ("Asia/Dhaka", "Asia/Dhaka"),
                    ("Asia/Colombo", "Asia/Colombo"),
                    ("Jamaica", "Jamaica"),
                    ("Asia/Yangon", "Asia/Yangon"),
                    ("Asia/Jerusalem", "Asia/Jerusalem"),
                    ("Australia/Perth", "Australia/Perth"),
                    ("Chile/Continental", "Chile/Continental"),
                    ("Asia/Manila", "Asia/Manila"),
                    ("Africa/Kigali", "Africa/Kigali"),
                    ("Atlantic/Faeroe", "Atlantic/Faeroe"),
                    ("Asia/Yerevan", "Asia/Yerevan"),
                    ("America/Moncton", "America/Moncton"),
                    ("Antarctica/Palmer", "Antarctica/Palmer"),
                    ("America/St_Barthelemy", "America/St_Barthelemy"),
                    ("US/Indiana-Starke", "US/Indiana-Starke"),
                    ("Europe/Vaduz", "Europe/Vaduz"),
                    ("Pacific/Guadalcanal", "Pacific/Guadalcanal"),
                    ("Etc/GMT+2", "Etc/GMT+2"),
                    ("Europe/Uzhgorod", "Europe/Uzhgorod"),
                    ("Europe/Tiraspol", "Europe/Tiraspol"),
                    ("Africa/Abidjan", "Africa/Abidjan"),
                    ("Canada/Mountain", "Canada/Mountain"),
                    ("Brazil/Acre", "Brazil/Acre"),
                    ("Australia/Lindeman", "Australia/Lindeman"),
                    ("Africa/Kinshasa", "Africa/Kinshasa"),
                    ("America/North_Dakota/Center", "America/North_Dakota/Center"),
                    ("Africa/Maseru", "Africa/Maseru"),
                    ("Europe/Lisbon", "Europe/Lisbon"),
                    ("America/New_York", "America/New_York"),
                    ("America/Louisville", "America/Louisville"),
                    ("Africa/Douala", "Africa/Douala"),
                    ("Asia/Krasnoyarsk", "Asia/Krasnoyarsk"),
                    ("America/Phoenix", "America/Phoenix"),
                    ("America/Atka", "America/Atka"),
                    ("Indian/Comoro", "Indian/Comoro"),
                    ("Asia/Makassar", "Asia/Makassar"),
                    ("Asia/Yakutsk", "Asia/Yakutsk"),
                    ("Israel", "Israel"),
                    ("Europe/Astrakhan", "Europe/Astrakhan"),
                    ("America/Argentina/Catamarca", "America/Argentina/Catamarca"),
                    ("WET", "WET"),
                    ("America/Glace_Bay", "America/Glace_Bay"),
                    ("America/Whitehorse", "America/Whitehorse"),
                    ("Indian/Antananarivo", "Indian/Antananarivo"),
                    ("Europe/Jersey", "Europe/Jersey"),
                    ("America/St_Kitts", "America/St_Kitts"),
                    ("ROC", "ROC"),
                    ("America/Argentina/San_Luis", "America/Argentina/San_Luis"),
                    ("America/Yakutat", "America/Yakutat"),
                    ("Antarctica/Syowa", "Antarctica/Syowa"),
                    ("America/Mazatlan", "America/Mazatlan"),
                    ("Pacific/Kiritimati", "Pacific/Kiritimati"),
                    ("Africa/Porto-Novo", "Africa/Porto-Novo"),
                    ("Europe/Vatican", "Europe/Vatican"),
                    ("Africa/Niamey", "Africa/Niamey"),
                    ("Asia/Omsk", "Asia/Omsk"),
                    ("America/Indiana/Tell_City", "America/Indiana/Tell_City"),
                    ("Africa/Timbuktu", "Africa/Timbuktu"),
                    ("Africa/Addis_Ababa", "Africa/Addis_Ababa"),
                    ("America/Mexico_City", "America/Mexico_City"),
                    ("Indian/Cocos", "Indian/Cocos"),
                    ("Etc/GMT-12", "Etc/GMT-12"),
                    ("Kwajalein", "Kwajalein"),
                    ("America/Curacao", "America/Curacao"),
                    ("Australia/Darwin", "Australia/Darwin"),
                    ("Indian/Mayotte", "Indian/Mayotte"),
                    ("Atlantic/Azores", "Atlantic/Azores"),
                    ("Asia/Chita", "Asia/Chita"),
                    ("Australia/NSW", "Australia/NSW"),
                    ("America/Dawson", "America/Dawson"),
                    ("Egypt", "Egypt"),
                    ("Iceland", "Iceland"),
                    ("Asia/Katmandu", "Asia/Katmandu"),
                    ("Antarctica/Casey", "Antarctica/Casey"),
                    ("Africa/Dakar", "Africa/Dakar"),
                    ("Asia/Jakarta", "Asia/Jakarta"),
                    ("America/Indiana/Winamac", "America/Indiana/Winamac"),
                    ("America/Scoresbysund", "America/Scoresbysund"),
                    ("Africa/Juba", "Africa/Juba"),
                    ("Asia/Hebron", "Asia/Hebron"),
                    ("Pacific/Pago_Pago", "Pacific/Pago_Pago"),
                    ("US/Pacific", "US/Pacific"),
                    ("Europe/London", "Europe/London"),
                    ("America/Chihuahua", "America/Chihuahua"),
                    ("America/Antigua", "America/Antigua"),
                    ("America/Cayenne", "America/Cayenne"),
                    ("Etc/GMT+12", "Etc/GMT+12"),
                    ("America/Anguilla", "America/Anguilla"),
                    ("America/Matamoros", "America/Matamoros"),
                    ("Pacific/Norfolk", "Pacific/Norfolk"),
                    ("Asia/Qyzylorda", "Asia/Qyzylorda"),
                    ("Etc/GMT-11", "Etc/GMT-11"),
                    ("Pacific/Apia", "Pacific/Apia"),
                    ("Asia/Tbilisi", "Asia/Tbilisi"),
                    ("Europe/Dublin", "Europe/Dublin"),
                    ("America/Virgin", "America/Virgin"),
                    ("Africa/Accra", "Africa/Accra"),
                    ("Australia/West", "Australia/West"),
                    ("America/St_Lucia", "America/St_Lucia"),
                    ("Atlantic/South_Georgia", "Atlantic/South_Georgia"),
                    ("Asia/Novosibirsk", "Asia/Novosibirsk"),
                    ("Etc/GMT-3", "Etc/GMT-3"),
                    ("Asia/Aden", "Asia/Aden"),
                    ("Pacific/Samoa", "Pacific/Samoa"),
                    ("America/Adak", "America/Adak"),
                    ("America/Santiago", "America/Santiago"),
                    ("Australia/Hobart", "Australia/Hobart"),
                    ("Asia/Dushanbe", "Asia/Dushanbe"),
                    ("Europe/Busingen", "Europe/Busingen"),
                    ("Europe/Sarajevo", "Europe/Sarajevo"),
                    ("Europe/Belgrade", "Europe/Belgrade"),
                    ("America/Guadeloupe", "America/Guadeloupe"),
                    ("Pacific/Tahiti", "Pacific/Tahiti"),
                    ("Etc/GMT-14", "Etc/GMT-14"),
                    ("Etc/GMT+0", "Etc/GMT+0"),
                    ("Universal", "Universal"),
                ],
                default="Asia/Kolkata",
                max_length=50,
                verbose_name="Time zone",
            ),
        ),
    ]
