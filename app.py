# -*- coding: utf-8 -*-
import requests
import time
import re
import json
from datetime import datetime

# ------------------ PANELS CONFIG ------------------
PANELS = [
    {
        "api_url": "http://147.135.212.197/crapi/time/viewstats",
        "token": "Qk5WSjRSQmZUZZFnaWZxVYpXU4OIlFFiWU5TeohQUGhHjGZpfGhx"
    },
    {
        "api_url": "http://51.77.216.195/crapi/mait/viewstats",
        "token": "Q1NVSkNBUzRfU5GCSWqIV311gVSEa4JCX5FjeWaTbYppY26AXnFlZQ"
    },
    {
        "api_url": "http://51.77.216.195/crapi/lamix/viewstats",
        "token": "X4iWgnWXYlNhUYGJZ21PV1mEcEJpZ5RCiGSFSkN0cVw="
    },
    {
        "api_url": "http://51.77.216.195/crapi/konek/viewstats",
        "token": "X4iWgnWXYlNhUYGJZ21PV1mEcEJpZ5RCiGSFSkN0cVw="
    },
    {
        "api_url": "http://147.135.212.197/crapi/had/viewstats",
        "token": "SlNUSDRSQkWAdJKHXJWXilhOU194jphcdI6ZgYOFd2uEjWqJWIFm"
    },
    {
        "api_url": "http://51.83.6.7:20040/dolphin",
        "token": "577f257a64685bf58ae09f2dbe42f538a155081bf1b89bb4c30fa840493b2294"
    },
    {
        "api_url": "http://pscall.net/restapi/smsreport",
        "key": "SVFWRT1SS4RygI6Ag1FQSQ==",
        "params": {
            "start": 0,
            "length": 500
        }
    }
]

# XUP SMS Credentials & Endpoints
XUP_BASE_URL = "http://108.165.233.140"
XUP_LOGIN_URL = XUP_BASE_URL + "/api/auth/login"
XUP_CODES_URL = XUP_BASE_URL + "/api/sms-codes"
XUP_USERNAME = "saboor318"
XUP_PASSWORD = "saboor318"

# ------------------ TELEGRAM ------------------
TELEGRAM_BOT_TOKEN = "8779005863:AAGdhmwCa75Usjd10JJHM8d6eaQ__g_DXNI"
TELEGRAM_GROUP_ID = "-1003867730992"

# ------------------ MEMORY & SESSIONS ------------------
processed_ids = set()
xup_session = requests.Session()
xup_session.headers.update({"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"})

# ------------------ TELEGRAM SEND ------------------
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
        if res.status_code != 200:
            print(f"❌ TELEGRAM API ERROR: Status {res.status_code} - {res.text}")
            return False
        return True
    except Exception as e:
        print(f"❌ TELEGRAM CONNECTION ERROR: {e}")
        return False

# ------------------ GLOBAL COUNTRY DATABASE ------------------
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
    "387": "🇧🇦 Bosnia", "389": "🇲鍵 North Macedonia", "420": "🇨🇿 Czech Republic", "421": "🇸婚 Slovakia",
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

# ------------------ HELPERS ------------------
def mask_number(number):
    number = str(number).replace("+", "").strip()
    if len(number) > 6:
        return "+" + number[:4] + "****" + number[-2:]
    return "+" + number

def extract_otp(msg):
    match = re.search(r'\b\d{3}-\d{3}\b|\b\d{4,8}\b', msg)
    return match.group(0) if match else None

# ------------------ FORMAT MESSAGE ------------------
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

# ------------------ STANDARD PANEL FETCH ------------------
def fetch_sms(panel):
    try:
        params = {}
        if "key" in panel:
            params["key"] = panel["key"]
            if "params" in panel:
                params.update(panel["params"])
        else:
            params["token"] = panel["token"]
            params["records"] = 1000

        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(panel["api_url"], params=params, headers=headers, timeout=10)

        print("\033[95m━━━━━━━━━━━━━━━━━━━\033[0m")
        print(f"\033[92mSUCCESS\033[0m : \033[96mAPI CONNECTED\033[0m")
        print(f"\033[93mPANEL\033[0m : {panel['api_url']}")
        print("\033[95m━━━━━━━━━━━━━━━━━━━\033[0m")

        try:
            data = res.json()
        except:
            return []

        if isinstance(data, dict):
            if "data" in data:
                return data.get("data", [])
            if "rows" in data:
                return data.get("rows", [])
            if "codes" in data:
                return data.get("codes", [])
        elif isinstance(data, list):
            return data

        return []
    except Exception as e:
        print(f"❌ API ERROR ({panel['api_url']}): {e}")
        return []

# ------------------ XUP PANEL LOGIN & FETCH ------------------
def xup_login():
    try:
        payload = {"username": XUP_USERNAME, "password": XUP_PASSWORD}
        resp = xup_session.post(XUP_LOGIN_URL, json=payload, timeout=10)
        return resp.status_code == 200
    except:
        return False

def fetch_xup_sms():
    try:
        res = xup_session.get(XUP_CODES_URL, params={"limit": 100, "page": 1}, timeout=10)
        if res.status_code in [401, 403]:
            if xup_login():
                res = xup_session.get(XUP_CODES_URL, params={"limit": 100, "page": 1}, timeout=10)
            else:
                return []
        
        print("\033[95m━━━━━━━━━━━━━━━━━━━\033[0m")
        print(f"\033[92mSUCCESS\033[0m : \033[96mAPI CONNECTED\033[0m")
        print(f"\033[93mPANEL\033[0m : XUP PANEL")
        print("\033[95m━━━━━━━━━━━━━━━━━━━\033[0m")
        
        return res.json().get("codes", [])
    except Exception as e:
        print(f"❌ XUP API ERROR: {e}")
        return []

# ------------------ START SYSTEM & RUN TEST ------------------
print("🚀 BOT STARTED WITH ALL ACTIVE PANELS")
xup_login()  # Initial login check

# ====== AUTOMATIC TEST SMS ON LAUNCH ======
print("🛠 SENDING TEST SMS TO TELEGRAM GROUP...")
test_phone = "923001234567"
test_otp = "552-786"
test_raw_msg = "Your PANTHER OTP verification code is 552-786. Do not share this code with anyone."
test_service = "PANTHER TEST SERVICE"

test_formatted = format_message(test_phone, test_otp, test_raw_msg, test_service)
if send_telegram(test_formatted):
    print("✅ TEST SMS SENT SUCCESSFULLY TO GROUP!")
else:
    print("❌ TEST SMS FAILED. CHECK BOT PERMISSIONS OR GROUP ID.")
# ==========================================

# ------------------ MASTER ENGINE LOOP ------------------
while True:
    # 1. Process Standard Panels (including Dolphin, Hadi & Konek)
    for panel in PANELS:
        entries = fetch_sms(panel)
        
        # Security check: Agar entries valid list na hon to skip karein
        if not entries or not isinstance(entries, list):
            continue
            
        for entry in entries:
            # Security check: Agar list ke andar data dictionary format me na ho to skip karein
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

            otp = extract_otp(msg)
            if not otp:
                otp = entry.get("code") if entry.get("code") else None

            if not otp:
                processed_ids.add(uid)
                continue

            final_msg = format_message(phone, otp, msg, service_name)
            if send_telegram(final_msg):
                print("\033[95m━━━━━━━━━━━━━━━━━━━\033[0m")
                print(f"\\033[92mSUCCESS\\033[0m : \\033[96m{otp}\\033[0m")
                print(f"\\033[93mSEND TELEGRAM\\033[0m \\033[92m✅\\033[0m")
                print("\033[95m━━━━━━━━━━━━━━━━━━━\033[0m")

            processed_ids.add(uid)

    # 2. Process Unique XUP Panel Separately
    xup_entries = fetch_xup_sms()
    for entry in xup_entries:
        if not isinstance(entry, dict):
            continue

        msg = entry.get("rawMessage") or entry.get("code") or ""
        phone = entry.get("number") or ""
        date = entry.get("receivedAt") or ""
        service_name = entry.get("sender") or "WhatsApp"

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
            print("\033[95m━━━━━━━━━━━━━━━━━━━\033[0m")
            print(f"\\033[92mSUCCESS\\033[0m : \\033[96m{otp}\\033[0m")
            print(f"\\033[93mSEND TELEGRAM (XUP)\\033[0m \\033[92m✅\\033[0m")
            print("\033[95m━━━━━━━━━━━━━━━━━━━\033[0m")

        processed_ids.add(uid)

    time.sleep(3)

