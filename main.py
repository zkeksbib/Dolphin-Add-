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
        "params": {
            "token": "Qk5WSjRSQmZUZZFnaWZxVYpXU4OIlFFiWU5TeohQUGhHjGZpfGhx"
        }
    },
    {
        "name": "Mait Panel",
        "url": "http://51.77.216.195/crapi/mait/viewstats",
        "params": {
            "token": "Q1NVSkNBUzRfU5GCSWqIV311gVSEa4JCX5FjeWaTbYppY26AXnFlZQ"
        }
    },
    {
        "name": "Lamix Panel",
        "url": "http://51.77.216.195/crapi/lamix/viewstats",
        "params": {
            "token": "X4iWgnWXYlNhUYGJZ21PV1mEcEJpZ5RCiGSFSkN0cVw="
        }
    },
    {
        "name": "Konek Panel",
        "url": "http://51.77.216.195/crapi/konek/viewstats",
        "params": {
            "token": "X4iWgnWXYlNhUYGJZ21PV1mEcEJpZ5RCiGSFSkN0cVw="
        }
    },
    {
        "name": "Had Panel",
        "url": "http://147.135.212.197/crapi/had/viewstats",
        "params": {
            "token": "SlNUSDRSQkWAdJKHXJWXilhOU194jphcdI6ZgYOFd2uEjWqJWIFm"
        }
    },
    {
        "name": "PSCall Panel",
        "url": "https://pscall.net/api/v1/messages",
        "params": {
            "token": "6Atb1miXwRIA1Rby1AASRADNy95KlIoKZ-KdwdGn-3E",
            "limit": 100
        }
    },
    {
        "name": "KSI IPRN Panel",
        "url": "https://ksiiprn.com/api/v1/iprn/numbers",
        "headers": {
            "Authorization": "Bearer sk_live_ITtrLHEwN3Cu9eiplmuGgRtFF0vVkgvdxzbhSi4q",
            "Accept": "application/json"
        },
        "params": {}
    }
]

# ------------------ TELEGRAM ------------------
TELEGRAM_BOT_TOKEN = "8779005863:AAHv62VuVd1BsbYqlzEkyB6hYO_UJG8-v1s"
TELEGRAM_GROUP_ID = "-1003867730992"

TARGET_DATE = "2026-09-20"
processed_ids = set()
checked_panels = set()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
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

def detect_service(msg, sender=""):
    combined = f"{msg} {sender}".lower()
    if "telegram" in combined or "tg" in combined:
        return "Telegram"
    elif "whatsapp" in combined or "wa" in combined:
        return "WhatsApp"
    elif "imo" in combined:
        return "IMO"
    elif "viber" in combined:
        return "Viber"
    elif "google" in combined:
        return "Google"
    elif "facebook" in combined:
        return "Facebook"
    return sender if sender else "SMS Service"

def format_message(phone, otp, message, service_name="WhatsApp", msg_time=None):
    message = message.replace("\\n", "\n").replace("nn", "\n")
    masked = mask_number(phone)
    country = get_country(phone)
    pkt_time = msg_time if msg_time else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    pname = panel["name"]
    headers = panel.get("headers", {})
    params = panel.get("params", {})
    
    try:
        res = requests.get(panel["url"], headers=headers, params=params, timeout=10)
        
        if res.status_code == 200:
            if pname not in checked_panels:
                print(f"✅ {pname} Connected - Fetching SMS...")
                checked_panels.add(pname)
        else:
            print(f"⚠️ {pname} Error - HTTP Status {res.status_code}")
            return []
            
        data = res.json()
        
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            for key in ["data", "messages", "rows", "codes", "results"]:
                if key in data and isinstance(data[key], list):
                    return data[key]
            return []
        return []
    except Exception as e:
        print(f"❌ {pname} Connection Failed: {e}")
        return []

print(f"🚀 BOT STARTED - FETCHING CODES FOR {TARGET_DATE}")

# Startup Notification
startup_note = f"🤖 <b>Bot Started</b>\nTarget Date: <code>{TARGET_DATE}</code>\nFetching old codes from today, then switching to real-time mode."
send_telegram(startup_note)

while True:
    for panel in PANELS:
        entries = fetch_sms(panel)
        if not entries or not isinstance(entries, list):
            continue
            
        for entry in entries:
            if not isinstance(entry, dict):
                continue

            msg = entry.get("message") or entry.get("text") or entry.get("sms") or entry.get("rawMessage") or ""
            phone = entry.get("number") or entry.get("to") or entry.get("num") or entry.get("phone") or ""
            sender = entry.get("cli") or entry.get("from") or entry.get("sender") or entry.get("service") or ""
            raw_date = str(entry.get("created_at") or entry.get("dt") or entry.get("dateadded") or entry.get("time") or "")

            if not msg or not phone:
                continue

            # Check: Agar date field mojood ho toh check karega ke message 2026-09-20 ka hi ho
            if raw_date and (TARGET_DATE not in raw_date):
                continue

            uid = f"{phone}-{msg}-{raw_date}"
            if uid in processed_ids:
                continue

            otp = extract_otp(msg) or entry.get("code")
            if not otp:
                processed_ids.add(uid)
                continue

            service_name = detect_service(msg, sender)
            final_msg = format_message(phone, otp, msg, service_name, raw_date if raw_date else None)
            
            if send_telegram(final_msg):
                print(f"[{panel['name']}] OTP: {otp} sent to Telegram ✅")
                time.sleep(0.5)  # Telegram rate-limit bachane ke liye chhota delay

            processed_ids.add(uid)

    time.sleep(3)
