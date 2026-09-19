# -*- coding: utf-8 -*-
import requests
import time
import re
import json
from datetime import datetime

# ------------------ UNIFIED PANELS CONFIG ------------------
PANELS = [
    {
        "name": "Time Panel",
        "url": "http://147.135.212.197/crapi/time/viewstats",
        "headers": {"User-Agent": "Mozilla/5.0"},
        "params": {
            "token": "Qk5WSjRSQmZUZZFnaWZxVYpXU4OIlFFiWU5TeohQUGhHjGZpfGhx", 
            "records": 1000,
            "start_date": "2026-08-10",
            "end_date": "2026-12-31"
        }
    },
    {
        "name": "Mait Panel",
        "url": "http://51.77.216.195/crapi/mait/viewstats",
        "headers": {"User-Agent": "Mozilla/5.0"},
        "params": {
            "token": "Q1NVSkNBUzRfU5GCSWqIV311gVSEa4JCX5FjeWaTbYppY26AXnFlZQ", 
            "records": 1000,
            "start_date": "2026-08-10",
            "end_date": "2026-12-31"
        }
    },
    {
        "name": "Lamix Panel",
        "url": "http://51.77.216.195/crapi/lamix/viewstats",
        "headers": {"User-Agent": "Mozilla/5.0"},
        "params": {
            "token": "X4iWgnWXYlNhUYGJZ21PV1mEcEJpZ5RCiGSFSkN0cVw=", 
            "records": 1000,
            "start_date": "2026-08-10",
            "end_date": "2026-12-31"
        }
    },
    {
        "name": "Konek Panel",
        "url": "http://51.77.216.195/crapi/konek/viewstats",
        "headers": {"User-Agent": "Mozilla/5.0"},
        "params": {
            "token": "X4iWgnWXYlNhUYGJZ21PV1mEcEJpZ5RCiGSFSkN0cVw=", 
            "records": 1000,
            "start_date": "2026-08-10",
            "end_date": "2026-12-31"
        }
    },
    {
        "name": "Had Panel",
        "url": "http://147.135.212.197/crapi/had/viewstats",
        "headers": {"User-Agent": "Mozilla/5.0"},
        "params": {
            "token": "SlNUSDRSQkWAdJKHXJWXilhOU194jphcdI6ZgYOFd2uEjWqJWIFm", 
            "records": 1000,
            "start_date": "2026-08-10",
            "end_date": "2026-12-31"
        }
    },
    {
        "name": "PSCall Panel",
        "url": "https://pscall.net/api/v1/messages",
        "headers": {"User-Agent": "Mozilla/5.0"},
        "params": {
            "token": "6Atb1miXwRIA1Rby1AASRADNy95KlIoKZ-KdwdGn-3E", 
            "start": 0, 
            "length": 500,
            "start_date": "2026-08-10",
            "end_date": "2026-12-31"
        }
    },
    {
        "name": "KSI IPRN Panel",
        "url": "https://ksiiprn.com/api/v1/iprn/numbers",
        "headers": {
            "Authorization": "Bearer sk_live_ITtrLHEwN3Cu9eiplmuGgRtFF0vVkgvdxzbhSi4q",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        },
        "params": {
            "start_date": "2026-08-10",
            "end_date": "2026-12-31"
        }
    }
]

# ------------------ TELEGRAM ------------------
TELEGRAM_BOT_TOKEN = "8128477326:AAHYi_0ZPt08uJ520kodW1fE1M7px10urE4"
TELEGRAM_GROUP_ID = "-1003867730992"

processed_ids = set()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMhttps://pscall.net/api/v1/messagesessage"
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "✈️ Channel", "url": "https://t.me/meThod5527"},
                {"text": "📱 Number Channel", "url": "https://t.me/panthernumbers"}
            ]
        ]
    }
    data = {
        "chat_id": TELEGRAM_GROUP_ID,
        "text": msg,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(keyboard)
    }
    try:
        res = requests.post(url, json=data, timeout=10)
        return res.status_code == 200
    except:
        return False

country_codes = {
    "1": "🇺🇸 USA/Canada", "7": "🇷🇺 Russia", "20": "🇪🇬 Egypt", "27": "🇿🇦 South Africa",
    "30": "🇬🇷 Greece", "31": "🇳🇱 Netherlands", "32": "🇧🇪 Belgium", "33": "🇫🇷 France",
    "34": "🇪🇸 Spain", "36": "🇭🇺 Hungary", "39": "🇮🇹 Italy", "40": "🇷🇴 Romania",
    "41": "🇨🇭 Switzerland", "43": "🇦🇹 Austria", "44": "🇬🇧 United Kingdom", "45": "🇩🇰 Denmark",
    "46": "🇸🇪 Sweden", "47": "🇳🇴 Norway", "48": "🇵🇱 Poland", "49": "🇩🇪 Germany",
    "51": "🇵🇪 Peru", "52": "🇲🇽 Mexico", "53": "🇨🇺 Cuba", "54": "🇦🇷 Argentina",
    "55": "🇧🇷 Brazil", "56": "🇨🇱 Chile", "57": "🇨🇴 Colombia", "58": "🇻🇪 Venezuela",
    "60": "🇲🇾 Malaysia", "61": "🇦🇺 Australia", "62": "🇮🇩 Indonesia", "63": "🇵🇭 Philippines",
    "64": "🇳🇿 New Zealand", "65": "🇸🇬 Singapore", "66": "🇹🇭 Thailand", "81": "🇯🇵 Japan",
    "82": "🇰🇷 South Korea", "84": "🇻🇳 Vietnam", "86": "🇨🇳 China", "90": "🇹🇷 Turkey",
    "91": "🇮🇳 India", "92": "🇵🇰 Pakistan", "93": "🇦🇫 Afghanistan", "94": "🇱🇰 Sri Lanka",
    "95": "🇲🇲 Myanmar", "98": "🇮🇷 Iran", "211": "🇸🇸 South Sudan", "212": "🇲🇦 Morocco",
    "213": "🇩🇿 Algeria", "216": "🇹🇳 Tunisia", "218": "🇱🇾 Libya", "220": "🇬🇲 Gambia",
    "221": "🇸🇳 Senegal", "222": "🇲🇷 Mauritania", "223": "🇲🇱 Mali", "224": "🇬🇳 Guinea",
    "225": "🇨🇮 Ivory Coast", "226": "🇧🇫 Burkina Faso", "227": "🇳🇪 Niger", "228": "🇹🇬 Togo",
    "229": "🇧🇯 Benin", "230": "🇲🇺 Mauritius", "231": "🇱🇷 Liberia", "232": "🇸🇱 Sierra Leone",
    "233": "🇬🇭 Ghana", "234": "🇳🇬 Nigeria", "235": "🇹🇩 Chad", "236": "🇨🇫 Central African Rep",
    "237": "🇨🇲 Cameroon", "238": "🇨🇻 Cape Verde", "239": "🇸🇹 Sao Tome", "240": "🇬🇶 Equatorial Guinea",
    "241": "🇬🇦 Gabon", "242": "🇨🇬 Congo", "243": "🇨🇩 DR Congo", "244": "🇦🇴 Angola",
    "245": "🇬🇼 Guinea-Bissau", "248": "🇸🇨 Seychelles", "249": "🇸🇩 Sudan", "250": "🇷🇼 Rwanda",
    "251": "🇪🇹 Ethiopia", "252": "🇸🇴 Somalia", "253": "🇩🇯 Djibouti", "254": "🇰🇪 Kenya",
    "255": "🇹🇿 Tanzania", "256": "🇺🇬 Uganda", "257": "🇧🇮 Burundi", "258": "🇲🇿 Mozambique",
    "260": "🇿🇲 Zambia", "261": "🇲🇬 Madagascar", "262": "🇷🇪 Reunion", "263": "🇿🇼 Zimbabwe",
    "264": "🇳🇦 Namibia", "265": "🇲🇼 Malawi", "266": "🇱🇸 Lesotho", "267": "🇧🇼 Botswana",
    "268": "🇸🇿 Eswatini", "269": "🇰🇲 Comoros", "290": "🇸🇭 Saint Helena", "291": "🇪🇷 Eritrea",
    "297": "🇦🇼 Aruba", "298": "🇫🇴 Faroe Islands", "299": "🇬🇱 Greenland", "350": "🇬🇮 Gibraltar",
    "351": "🇵🇹 Portugal", "352": "🇱🇺 Luxembourg", "353": "🇮🇪 Ireland", "354": "🇮🇸 Iceland",
    "355": "🇦🇱 Albania", "356": "🇲🇹 Malta", "357": "🇨🇾 Cyprus", "358": "🇫🇮 Finland",
    "359": "🇧🇬 Bulgaria", "370": "🇱🇹 Lithuania", "371": "🇱🇻 Latvia", "372": "🇪🇪 Estonia",
    "373": "🇲🇩 Moldova", "374": "🇦🇲 Armenia", "375": "🇧🇾 Belarus", "376": "🇦🇩 Andorra",
    "377": "🇲🇨 Monaco", "378": "🇸🇲 San Marino", "380": "🇺🇦 Ukraine", "381": "🇷🇸 Serbia",
    "382": "🇲🇪 Montenegro", "383": "🇽🇰 Kosovo", "385": "🇭🇷 Croatia", "386": "🇸🇮 Slovenia",
    "387": "🇧🇦 Bosnia", "389": "🇲🇰 North Macedonia", "420": "🇨🇿 Czech Republic", "421": "🇸🇰 Slovakia",
    "423": "🇱🇮 Liechtenstein", "500": "🇫🇰 Falkland Islands", "501": "🇧🇿 Belize", "502": "🇬🇹 Guatemala",
    "503": "🇸🇻 El Salvador", "504": "🇭🇳 Honduras", "505": "🇳🇮 Nicaragua", "506": "🇨🇷 Costa Rica",
    "507": "🇵🇦 Panama", "509": "🇭🇹 Haiti", "590": "🇬🇵 Guadeloupe", "591": "🇧🇴 Bolivia",
    "592": "🇬🇾 Guyana", "593": "🇪🇨 Ecuador", "594": "🇬🇫 French Guiana", "595": "🇵🇾 Paraguay",
    "596": "🇲🇶 Martinique", "597": "🇸🇷 Suriname", "598": "🇺🇾 Uruguay", "599": "🇨🇼 Curacao",
    "670": "🇹🇱 Timor-Leste", "672": "🇳🇫 Norfolk Island", "673": "🇧🇳 Brunei", "674": "🇳🇷 Nauru",
    "675": "🇵🇬 Papua New Guinea", "676": "🇹🇴 Tonga", "677": "🇸🇧 Solomon Islands", "678": "🇻🇺 Vanuatu",
    "679": "🇫🇯 Fiji", "680": "🇵🇼 Palau", "681": "🇼🇫 Wallis and Futuna", "682": "🇨🇰 Cook Islands",
    "683": "🇳🇺 Niue", "685": "🇼🇸 Samoa", "686": "🇰🇮 Kiribati", "687": "🇳🇨 New Caledonia",
    "688": "🇹🇻 Tuvalu", "689": "🇵🇫 French Polynesia", "690": "🇹🇰 Tokelau", "691": "🇫🇲 Micronesia",
    "692": "🇲🇭 Marshall Islands", "850": "🇰🇵 North Korea", "852": "🇭🇰 Hong Kong",
    "853": "🇲🇴 Macau", "855": "🇰🇭 Cambodia", "856": "🇱🇦 Laos", "880": "🇧🇩 Bangladesh",
    "886": "🇹🇼 Taiwan", "960": "🇲🇻 Maldives", "961": "🇱🇧 Lebanon", "962": "🇯🇴 Jordan",
    "963": "🇸🇾 Syria", "964": "🇮🇶 Iraq", "965": "🇰🇼 Kuwait", "966": "🇸🇦 Saudi Arabia",
    "967": "🇾🇪 Yemen", "968": "🇴🇲 Oman", "970": "🇵🇸 Palestine", "971": "🇦🇪 UAE",
    "972": "🇮🇱 Israel", "973": "🇧🇭 Bahrain", "974": "🇶🇦 Qatar", "975": "🇧🇹 Bhutan",
    "976": "🇲🇳 Mongolia", "977": "🇳🇵 Nepal", "992": "🇹🇯 Tajikistan", "993": "🇹🇲 Turkmenistan",
    "994": "🇦🇿 Azerbaijan", "995": "🇬🇪 Georgia", "996": "🇰🇬 Kyrgyzstan", "998": "🇺🇿 Uzbekistan"
}

def get_country(number):
    number = str(number).replace("+", "").strip()
    for code in sorted(country_codes, key=len, reverse=True):
        if number.startswith(code):
            return country_codes[code]
    return "🌍 Unknown"

def mask_number(number):
    number = str(number).replace("+", "").strip()
    if len(number) > 6:
        return "+" + number[:4] + "****" + number[-2:]
    return "+" + number

def extract_otp(msg):
    match = re.search(r'\b\d{3}-\d{3}\b|\b\d{4,8}\b', msg)
    return match.group(0) if match else None

def format_message(phone, otp, message, service_name="WhatsApp"):
    message = message.replace("\\n", "\n").replace("nn", "\n")
    masked = mask_number(phone)
    country = get_country(phone)
    pkt_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""
<b> New OTP Successfully Received 🎉</b>

<blockquote>🕰 Time: {pkt_time}</blockquote>
<blockquote>🌍 Country: {country}</blockquote>
<blockquote>📞 Number: {masked}</blockquote>
<blockquote>🟢 Service: {service_name}</blockquote>
<blockquote>🔑 OTP: <code>{otp}</code></blockquote>

📩 Full Message:

<blockquote>
{message}
</blockquote>
"""

def fetch_sms(panel):
    try:
        res = requests.get(panel["url"], headers=panel["headers"], params=panel["params"], timeout=10)
        if res.status_code == 429:
            return []
        data = res.json()
        
        if isinstance(data, dict):
            return data.get("data", data.get("rows", data.get("codes", data.get("results", []))))
        elif isinstance(data, list):
            return data
        return []
    except Exception as e:
        print(f"❌ Error in {panel['name']}: {e}")
        return []

print("🚀 BOT STARTED WITH UNIFIED PANELS")

# Send startup test message to Telegram
test_msg = format_message("923001234567", "123456", "🤖 Test Message: Bot started successfully and all panels are active!", "Test Service")
send_telegram(test_msg)

while True:
    for panel in PANELS:
        entries = fetch_sms(panel)
        if not entries or not isinstance(entries, list):
            continue
            
        for entry in entries:
            if not isinstance(entry, dict):
                continue

            msg = entry.get("message") or entry.get("sms") or entry.get("rawMessage") or ""
            phone = entry.get("num") or entry.get("number") or entry.get("phone") or ""
            date = entry.get("dt") or entry.get("dateadded") or entry.get("receivedAt") or entry.get("time") or ""
            service_name = entry.get("sender") or entry.get("service") or "WhatsApp"

            if not msg or not phone:
                continue

            uid = f"{phone}-{msg}-{date}"
            if uid in processed_ids:
                continue

            otp = extract_otp(msg) or entry.get("code")
            if not otp:
                processed_ids.add(uid)
                continue

            final_msg = format_message(phone, otp, msg, service_name)
            if send_telegram(final_msg):
                print(f"[{panel['name']}] SUCCESS: {otp} sent to Telegram ✅")

            processed_ids.add(uid)

    time.sleep(3)


