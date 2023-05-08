flightDict = [
#1
    {
        'regex': 'may bay',
        'POS': 'FLIGHT-N'
    },
    {
        'regex': 'nao',
        'POS': 'QDET'
    },
    {
        'regex': 'den',
        'POS': ['FLIGHT_END-V', 'TO-P']
    },
    {
        'regex': 'thanh pho',
        'POS': 'CITY-N'
    },
    {
        'regex': 'hue',
        'POS': 'CITY-NAME'
    },
    {
        'regex': 'luc',
        'POS': 'AT-P'
    },
    {
        'regex': '\d\d:\d\dhr',
        'POS': 'FLIGHT_TIME-N'
    },
#2
    {
        'regex': 'bay',
        'POS': 'FLIGHT-V'
    },
    {
        'regex': 'tu',
        'POS': 'FROM-P'
    },
    {
        'regex': 'da nang',
        'POS': 'CITY-NAME'
    },
    {
        'regex': 'ho chi minh',
        'POS': 'CITY-NAME'
    },
    {
        'regex': 'mat',
        'POS': 'LAST-P'
    },
    {
        'regex': 'gio',
        'POS': 'HOUR-N'
    },
    {
        'regex': '\d',
        'POS': 'FLIGHT_TIME_DURATION-N'
    },
#3
    {
        'regex': 'hay cho biet',
        'POS': 'QDET'
    },
    {
        'regex': 'ma hieu',
        'POS': 'FLIGHT-N'
    },
    {
        'regex': 'cac',
        'POS': 'PLURAL-DET'
    },
    {
        'regex': 'ha canh',
        'POS': 'FLIGHT_END-V'
    },
    {
        'regex': 'o',
        'POS': 'IN-P'
    },
#4
    {
        'regex': 'xuat phat',
        'POS': 'FLIGHT_BEGIN-V'
    },
    {
        'regex': 'may',
        'POS': 'QDET'
    },
#5
    {
        'regex': 'ha noi',
        'POS': 'CITY-NAME'
    },
#6
    {
        'regex': 'co',
        'POS': 'YES-WH'
    },
    {
        'regex': 'khong',
        'POS': 'NO-WH'
    },
    {
        'regex': '(vn|vj)\d',
        'POS': 'FLIGHT-NAME'
    },
#7
    {
        'regex': 'thoi gian',
        'POS': 'TIME-N'
    },
    {
        'regex': 'khanh hoa',
        'POS': 'CITY-NAME'
    },
#8
    {
        'regex': 'hai phong',
        'POS': 'CITY-NAME'
    },
#9
    {
        'regex': 'cua',
        'POS': 'POSS-P'
    },
    {
        'regex': 'hang hang khong',
        'POS': 'BRAND-N'
    },
    {
        'regex': 'vietjet air|vietnam airlines',
        'POS': 'BRAND-NAME'
    },
    {
        'regex': 'nhung',
        'POS': 'PLURAL-DET'
    },
    {
        'regex': '\?',
        'POS': 'PUNC'
    },
]