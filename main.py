# -*- coding: utf-8 -*-
import requests
import time
import re
import json
from datetime import datetime

# ------------------ TELEGRAM ------------------
TELEGRAM_BOT_TOKEN = "8128477326:AAHYi_0ZPt08uJ520kodW1fE1M7px10urE4"
TELEGRAM_GROUP_ID = "-1003867730992"

processed_ids = set()
# Start mein 0 rakha hai taake bot shuru hote hi pehla check ho sake
last_ksi_check = 0 

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
    "994": "🇦🇿 Azerbaijan", "995": "🇬🇪 Georgia", "996": "🇰🇬 Kyrgyzstan", "998": "UZ Uzbekistan"
}

def get_country(number):
    clean = str(number).replace("+", "").strip()
    for code in sorted(country_codes, key=len, reverse=True):
        if clean.startswith(code):
            return country_codes[code]
    return "🌍 Unknown"

def mask_number(number):
    clean = str(number).replace("+", "").strip()
    if len(clean) > 6:
        return "+" + clean[:4] + "****" + clean[-2:]
    return "+" + clean

def extract_otp(msg):
    text = str(msg)
    imo_match = re.search(r'(?:code\s*(?:is)?\s*[:]?\s*)(\d{4,6})', text, re.IGNORECASE)
    if imo_match:
        return imo_match.group(1)
    hyphen_match = re.search(r'\b\d{3}-\d{3}\b', text)
    if hyphen_match:
        return hyphen_match.group(0)
    general_match = re.search(r'\b\d{4,8}\b', text)
    if general_match:
        return general_match.group(0)
    return None

def detect_service(msg, sender=""):
    text = f"{msg} {sender}".lower()
    if "imo" in text:
        return "IMO"
    elif "whatsapp" in text or "wa" in text:
        return "WhatsApp"
    elif "telegram" in text or "tg" in text:
        return "Telegram"
    elif "truecaller" in text:
        return "Truecaller"
    elif "viber" in text:
        return "Viber"
    elif "facebook" in text:
        return "Facebook"
    elif "google" in text:
        return "Google"
    return sender if sender else "SMS Service"

def format_message(phone, otp, message, service_name):
    clean_msg = message.replace("\\n", "\n").replace("nn", "\n").replace("nNever", "\nNever").replace("nDO NOT", "\nDO NOT")
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
{clean_msg}
</blockquote>
"""

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

# ------------------ FETCHERS ------------------
def fetch_flex():
    try:
        url = "http://51.77.216.195/crapi/mait/viewstats"
        params = {"token": "Q1NVSkNBUzRfU5GCSWqIV311gVSEa4JCX5FjeWaTbYppY26AXnFlZQ"}
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            return r.json().get("data", [])
    except:
        pass
    return []

def fetch_pscall():
    try:
        url = "https://pscall.net/api/v1/messages"
        params = {"token": "6Atb1miXwRIA1Rby1AASRADNy95KlIoKZ-KdwdGn-3E", "limit": 50}
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list):
                return data
            for key in ["messages", "data"]:
                if key in data and isinstance(data[key], list):
                    return data[key]
    except:
        pass
    return []

def fetch_ksi():
    try:
        url = "https://ksiiprn.com/api/v1/iprn/messages"
        headers = {
            "Authorization": "Bearer sk_live_K9jJQFD3xxlIkgb6mS9O6h1xZ06Ow1aGfBa8jIiO",
            "Accept": "application/json"
        }
        r = requests.get(url, headers=headers, timeout=10)
        print(f"📡 [KSI Status]: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            items = data.get("data", []) if isinstance(data, dict) else data
            print(f"📥 [KSI] Total Messages Received: {len(items)}")
            return items
        elif r.status_code == 429:
            print("⚠️ KSI Rate limit: Waiting full 65s window...")
    except Exception as e:
        print("❌ KSI Error:", e)
    return []

def process_and_send(entry, panel_name):
    msg = str(entry.get("message") or entry.get("content") or entry.get("text") or entry.get("sms") or "")
    phone = str(entry.get("number") or entry.get("num") or entry.get("to") or entry.get("phone") or "")
    sender = str(entry.get("source") or entry.get("cli") or entry.get("from") or entry.get("sender") or "")
    date_val = str(entry.get("received_at") or entry.get("dt") or entry.get("time") or entry.get("created_at") or "")

    if not phone or not msg:
        return

    otp = extract_otp(msg) or str(entry.get("code") or "")
    if not otp:
        return

    uid = f"{phone}-{otp}-{date_val}"
    if uid in processed_ids:
        return

    service = detect_service(msg, sender)
    final_msg = format_message(phone, otp, msg, service)

    if send_telegram(final_msg):
        print(f"[{panel_name}] FORWARDED: {otp} ({service}) to Telegram ✅")
        processed_ids.add(uid)

print("🚀 BOT RUNNING: PSCall, Flex SMS, and KSI IPRN")

while True:
    # 1. Flex SMS (Fast Check - har 2 second)
    for row in fetch_flex():
        process_and_send(row, "Flex SMS")

    # 2. PSCall Panel (Fast Check - har 2 second)
    for row in fetch_pscall():
        process_and_send(row, "PSCall")

    # 3. KSI IPRN Panel (Strict 65-second rate limit safety)
    now = time.time()
    if (now - last_ksi_check) >= 65 or last_ksi_check == 0:
        last_ksi_check = now
        for row in fetch_ksi():
            process_and_send(row, "KSI IPRN")

    time.sleep(2)
