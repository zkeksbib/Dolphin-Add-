# -*- coding: utf-8 -*-
import requests
import time
import re
import json

# ------------------ PANELS CONFIG ------------------
PANELS = [
    {
        "name": "MAIT Flex",
        "api_url": "http://51.77.216.195/crapi/mait/viewstats",
        "token": "Q1NVSkNBUzRfU5GCSWqIV311gVSEa4JCX5FjeWaTbYppY26AXnFlZQ"
    },
    {
        "name": "CRAPI Time",
        "api_url": "http://147.135.212.197/crapi/time/viewstats",
        "token": "Qk5WSjRSQmZUZZFnaWZxVYpXU4OIlFFiWU5TeohQUGhHjGZpfGhx"
    },
    {
        "name": "Lamix",
        "api_url": "http://51.77.216.195/crapi/lamix/viewstats",
        "token": "X4iWgnWXYlNhUYGJZ21PV1mEcEJpZ5RCiGSFSkN0cVw="
    },
    {
        "name": "Konek",
        "api_url": "http://51.77.216.195/crapi/konek/viewstats",
        "token": "X4iWgnWXYlNhUYGJZ21PV1mEcEJpZ5RCiGSFSkN0cVw="
    },
    {
        "name": "Hadi",
        "api_url": "http://147.135.212.197/crapi/had/viewstats",
        "token": "SlNUSDRSQkWAdJKHXJWXilhOU194jphcdI6ZgYOFd2uEjWqJWIFm"
    },
    {
        "name": "PSCall",
        "api_url": "http://pscall.net/restapi/smsreport",
        "key": "SVFWRT1SS4RygI6Ag1FQSQ==",
        "params": {
            "start": 0,
            "length": 500
        }
    }
]

# ------------------ TELEGRAM CONFIG ------------------
TELEGRAM_BOT_TOKEN = "8128477326:AAH-NmzFoEh8hEQT8rO4kzpZRbBHYa9vdNo"
TELEGRAM_GROUP_ID = "-1003867730992"

# ------------------ MEMORY ------------------
processed_ids = set()

# ------------------ COMPLETE GLOBAL COUNTRY DATABASE ------------------
country_db = {
    "1": {"flag": "🇺🇸", "iso": "US"}, "7": {"flag": "🇷🇺", "iso": "RU"},
    "20": {"flag": "🇪🇬", "iso": "EG"}, "27": {"flag": "🇿🇦", "iso": "ZA"},
    "30": {"flag": "🇬🇷", "iso": "GR"}, "31": {"flag": "🇳🇱", "iso": "NL"},
    "32": {"flag": "🇧🇪", "iso": "BE"}, "33": {"flag": "🇫🇷", "iso": "FR"},
    "34": {"flag": "🇪🇸", "iso": "ES"}, "36": {"flag": "🇭🇺", "iso": "HU"},
    "39": {"flag": "🇮🇹", "iso": "IT"}, "40": {"flag": "🇷🇴", "iso": "RO"},
    "41": {"flag": "🇨🇭", "iso": "CH"}, "43": {"flag": "🇦🇹", "iso": "AT"},
    "44": {"flag": "🇬🇧", "iso": "UK"}, "45": {"flag": "🇩🇰", "iso": "DK"},
    "46": {"flag": "🇸🇪", "iso": "SE"}, "47": {"flag": "🇳🇴", "iso": "NO"},
    "48": {"flag": "🇵🇱", "iso": "PL"}, "49": {"flag": "🇩🇪", "iso": "DE"},
    "51": {"flag": "🇵🇪", "iso": "PE"}, "52": {"flag": "🇲🇽", "iso": "MX"},
    "53": {"flag": "🇨🇺", "iso": "CU"}, "54": {"flag": "🇦🇷", "iso": "AR"},
    "55": {"flag": "🇧🇷", "iso": "BR"}, "56": {"flag": "🇨🇱", "iso": "CL"},
    "57": {"flag": "🇨🇴", "iso": "CO"}, "58": {"flag": "🇻🇪", "iso": "VE"},
    "60": {"flag": "🇲🇾", "iso": "MY"}, "61": {"flag": "🇦🇺", "iso": "AU"},
    "62": {"flag": "🇮🇩", "iso": "ID"}, "63": {"flag": "🇵🇭", "iso": "PH"},
    "64": {"flag": "🇳🇿", "iso": "NZ"}, "65": {"flag": "🇸🇬", "iso": "SG"},
    "66": {"flag": "🇹🇭", "iso": "TH"}, "81": {"flag": "🇯🇵", "iso": "JP"},
    "82": {"flag": "🇰🇷", "iso": "KR"}, "84": {"flag": "🇻🇳", "iso": "VN"},
    "86": {"flag": "🇨🇳", "iso": "CN"}, "90": {"flag": "🇹🇷", "iso": "TR"},
    "91": {"flag": "🇮🇳", "iso": "IN"}, "92": {"flag": "🇵🇰", "iso": "PK"},
    "93": {"flag": "🇦🇫", "iso": "AF"}, "94": {"flag": "🇱🇰", "iso": "LK"},
    "95": {"flag": "🇲🇲", "iso": "MM"}, "98": {"flag": "🇮🇷", "iso": "IR"},
    "212": {"flag": "🇲🇦", "iso": "MA"}, "213": {"flag": "🇩🇿", "iso": "DZ"},
    "216": {"flag": "🇹🇳", "iso": "TN"}, "218": {"flag": "🇱🇾", "iso": "LY"},
    "220": {"flag": "🇬🇲", "iso": "GM"}, "221": {"flag": "🇸🇳", "iso": "SN"},
    "222": {"flag": "🇲🇷", "iso": "MR"}, "223": {"flag": "🇲🇱", "iso": "ML"},
    "224": {"flag": "🇬🇳", "iso": "GN"}, "225": {"flag": "🇨🇮", "iso": "CI"},
    "226": {"flag": "🇧🇫", "iso": "BF"}, "227": {"flag": "🇳🇪", "iso": "NE"},
    "228": {"flag": "🇹🇬", "iso": "TG"}, "229": {"flag": "🇧🇯", "iso": "BJ"},
    "230": {"flag": "🇲🇺", "iso": "MU"}, "231": {"flag": "🇱🇷", "iso": "LR"},
    "232": {"flag": "🇸🇱", "iso": "SL"}, "233": {"flag": "🇬🇭", "iso": "GH"},
    "234": {"flag": "🇳🇬", "iso": "NG"}, "235": {"flag": "🇹🇩", "iso": "TD"},
    "236": {"flag": "🇨🇫", "iso": "CF"}, "237": {"flag": "🇨🇲", "iso": "CM"},
    "238": {"flag": "🇨🇻", "iso": "CV"}, "239": {"flag": "🇸🇹", "iso": "ST"},
    "240": {"flag": "🇬🇶", "iso": "GQ"}, "241": {"flag": "🇬🇦", "iso": "GA"},
    "242": {"flag": "🇨🇬", "iso": "CG"}, "243": {"flag": "🇨🇩", "iso": "CD"},
    "244": {"flag": "🇦🇴", "iso": "AO"}, "245": {"flag": "🇬🇼", "iso": "GW"},
    "248": {"flag": "🇸🇨", "iso": "SC"}, "249": {"flag": "🇸🇩", "iso": "SD"},
    "250": {"flag": "🇷🇼", "iso": "RW"}, "251": {"flag": "🇪🇹", "iso": "ET"},
    "252": {"flag": "🇸🇴", "iso": "SO"}, "253": {"flag": "🇩🇯", "iso": "DJ"},
    "254": {"flag": "🇰🇪", "iso": "KE"}, "255": {"flag": "🇹🇿", "iso": "TZ"},
    "256": {"flag": "🇺🇬", "iso": "UG"}, "257": {"flag": "🇧🇮", "iso": "BI"},
    "258": {"flag": "🇲🇿", "iso": "MZ"}, "260": {"flag": "🇿🇲", "iso": "ZM"},
    "261": {"flag": "🇲🇬", "iso": "MG"}, "263": {"flag": "🇿🇼", "iso": "ZW"},
    "264": {"flag": "🇳🇦", "iso": "NA"}, "265": {"flag": "🇲🇼", "iso": "MW"},
    "266": {"flag": "🇱🇸", "iso": "LS"}, "267": {"flag": "🇧🇼", "iso": "BW"},
    "268": {"flag": "🇸🇿", "iso": "SZ"}, "269": {"flag": "🇰🇲", "iso": "KM"},
    "290": {"flag": "🇸🇭", "iso": "SH"}, "291": {"flag": "🇪🇷", "iso": "ER"},
    "297": {"flag": "🇦🇼", "iso": "AW"}, "298": {"flag": "🇫🇴", "iso": "FO"},
    "299": {"flag": "🇬🇱", "iso": "GL"}, "350": {"flag": "🇬🇮", "iso": "GI"},
    "351": {"flag": "🇵🇹", "iso": "PT"}, "352": {"flag": "🇱🇺", "iso": "LU"},
    "353": {"flag": "🇮🇪", "iso": "IE"}, "354": {"flag": "🇮🇸", "iso": "IS"},
    "355": {"flag": "🇦🇱", "iso": "AL"}, "356": {"flag": "🇲🇹", "iso": "MT"},
    "357": {"flag": "🇨🇾", "iso": "CY"}, "358": {"flag": "🇫🇮", "iso": "FI"},
    "359": {"flag": "🇧🇬", "iso": "BG"}, "370": {"flag": "🇱🇹", "iso": "LT"},
    "371": {"flag": "🇱🇻", "iso": "LV"}, "372": {"flag": "🇪🇪", "iso": "EE"},
    "373": {"flag": "🇲🇩", "iso": "MD"}, "374": {"flag": "🇦🇲", "iso": "AM"},
    "375": {"flag": "🇧🇾", "iso": "BY"}, "376": {"flag": "🇦🇩", "iso": "AD"},
    "377": {"flag": "🇲🇨", "iso": "MC"}, "378": {"flag": "🇸🇲", "iso": "SM"},
    "380": {"flag": "🇺🇦", "iso": "UA"}, "381": {"flag": "🇷🇸", "iso": "RS"},
    "382": {"flag": "🇲🇪", "iso": "ME"}, "383": {"flag": "🇽🇰", "iso": "XK"},
    "385": {"flag": "🇭🇷", "iso": "HR"}, "386": {"flag": "🇸🇮", "iso": "SI"},
    "387": {"flag": "🇧🇦", "iso": "BA"}, "389": {"flag": "🇲🇰", "iso": "MK"},
    "420": {"flag": "🇨🇿", "iso": "CZ"}, "421": {"flag": "🇸🇰", "iso": "SK"},
    "423": {"flag": "🇱🇮", "iso": "LI"}, "501": {"flag": "🇧🇿", "iso": "BZ"},
    "502": {"flag": "🇬🇹", "iso": "GT"}, "503": {"flag": "🇸🇻", "iso": "SV"},
    "504": {"flag": "🇭🇳", "iso": "HN"}, "505": {"flag": "🇳🇮", "iso": "NI"},
    "506": {"flag": "🇨🇷", "iso": "CR"}, "507": {"flag": "🇵🇦", "iso": "PA"},
    "509": {"flag": "🇭🇹", "iso": "HT"}, "590": {"flag": "🇬🇵", "iso": "GP"},
    "591": {"flag": "🇧🇴", "iso": "BO"}, "592": {"flag": "🇬🇾", "iso": "GY"},
    "593": {"flag": "🇪🇨", "iso": "EC"}, "594": {"flag": "🇬🇫", "iso": "GF"},
    "595": {"flag": "🇵🇾", "iso": "PY"}, "596": {"flag": "🇲🇶", "iso": "MQ"},
    "597": {"flag": "🇸🇷", "iso": "SR"}, "598": {"flag": "🇺🇾", "iso": "UY"},
    "599": {"flag": "🇨🇼", "iso": "CW"}, "670": {"flag": "🇹🇱", "iso": "TL"},
    "673": {"flag": "🇧🇳", "iso": "BN"}, "674": {"flag": "🇳🇷", "iso": "NR"},
    "675": {"flag": "🇵🇬", "iso": "PG"}, "676": {"flag": "🇹🇴", "iso": "TO"},
    "677": {"flag": "🇸🇧", "iso": "SB"}, "678": {"flag": "🇻🇺", "iso": "VU"},
    "679": {"flag": "🇫🇯", "iso": "FJ"}, "680": {"flag": "🇵🇼", "iso": "PW"},
    "682": {"flag": "🇨🇰", "iso": "CK"}, "685": {"flag": "🇼🇸", "iso": "WS"},
    "687": {"flag": "🇳🇨", "iso": "NC"}, "689": {"flag": "🇵🇫", "iso": "PF"},
    "850": {"flag": "🇰🇵", "iso": "KP"}, "852": {"flag": "🇭🇰", "iso": "HK"},
    "853": {"flag": "🇲🇴", "iso": "MO"}, "855": {"flag": "🇰🇭", "iso": "KH"},
    "856": {"flag": "🇱🇦", "iso": "LA"}, "880": {"flag": "🇧🇩", "iso": "BD"},
    "886": {"flag": "🇹🇼", "iso": "TW"}, "960": {"flag": "🇲🇻", "iso": "MV"},
    "961": {"flag": "🇱🇧", "iso": "LB"}, "962": {"flag": "🇯🇴", "iso": "JO"},
    "963": {"flag": "🇸🇾", "iso": "SY"}, "964": {"flag": "🇮🇶", "iso": "IQ"},
    "965": {"flag": "🇰🇼", "iso": "KW"}, "966": {"flag": "🇸🇦", "iso": "SA"},
    "967": {"flag": "🇾🇪", "iso": "YE"}, "968": {"flag": "🇴🇲", "iso": "OM"},
    "970": {"flag": "🇵🇸", "iso": "PS"}, "971": {"flag": "🇦🇪", "iso": "AE"},
    "972": {"flag": "🇮🇱", "iso": "IL"}, "973": {"flag": "🇧🇭", "iso": "BH"},
    "974": {"flag": "🇶🇦", "iso": "QA"}, "975": {"flag": "🇧🇹", "iso": "BT"},
    "976": {"flag": "🇲🇳", "iso": "MN"}, "977": {"flag": "🇳🇵", "iso": "NP"},
    "992": {"flag": "🇹🇯", "iso": "TJ"}, "993": {"flag": "🇹🇲", "iso": "TM"},
    "994": {"flag": "🇦🇿", "iso": "AZ"}, "995": {"flag": "🇬🇪", "iso": "GE"},
    "996": {"flag": "🇰🇬", "iso": "KG"}, "998": {"flag": "🇺🇿", "iso": "UZ"}
}

def get_country_info(number):
    clean_num = str(number).replace("+", "").strip()
    for code in sorted(country_db, key=len, reverse=True):
        if clean_num.startswith(code):
            return code, country_db[code]
    return "", {"flag": "🌍", "iso": "GLOBAL"}

# ------------------ NUMBER FORMATTING ------------------
def custom_mask_number(number):
    clean_num = str(number).replace("+", "").strip()
    code, _ = get_country_info(number)
    
    if code and len(clean_num) > len(code) + 2:
        front_digits = clean_num[:len(code) + 2]
        back_digits = clean_num[-4:]
        return f"+{front_digits}-ALPHA-{back_digits}"
    elif len(clean_num) >= 7:
        return f"+{clean_num[:4]}-ALPHA-{clean_num[-4:]}"
    return f"+{clean_num}"

def extract_otp(msg):
    if not msg:
        return None
    match = re.search(r'\b\d{3}-\d{3}\b|\b\d{4,8}\b', str(msg))
    return match.group(0) if match else None

# ------------------ CUSTOM FORMAT MESSAGE ------------------
def format_message(phone, otp, message, service_name=""):
    message = str(message).replace("\\n", "\n")
    masked_phone = custom_mask_number(phone)
    _, info = get_country_info(phone)
    
    flag = info["flag"]
    iso = info["iso"]

    return f"""{flag} ┃  #{iso} {masked_phone}
🔑 OTP: {otp}

💬 {message}
🔑 OTP: {otp}"""

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
        return res.status_code == 200
    except Exception as e:
        print(f"❌ TELEGRAM CONNECTION ERROR: {e}")
        return False

# ------------------ PARSER ------------------
def parse_entry_fields(entry):
    msg = (entry.get("message") or entry.get("sms") or entry.get("rawMessage") or 
           entry.get("full_message") or entry.get("text") or entry.get("content") or "")
    
    phone = (entry.get("num") or entry.get("number") or entry.get("phone") or 
             entry.get("msisdn") or entry.get("mobile") or "")
    
    date = (entry.get("dt") or entry.get("dateadded") or entry.get("receivedAt") or 
            entry.get("time") or entry.get("created_at") or "")
    
    service = (entry.get("sender") or entry.get("service") or entry.get("app") or 
               entry.get("title") or "")

    direct_otp = (entry.get("code") or entry.get("otp") or entry.get("pincode") or 
                  entry.get("passcode"))
    
    return str(msg), str(phone), str(date), str(service), direct_otp

# ------------------ PANEL FETCHERS ------------------
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

        try:
            data = res.json()
        except:
            return []

        if isinstance(data, dict):
            for k in ["data", "rows", "codes", "logs", "messages", "result"]:
                if k in data and isinstance(data[k], list):
                    return data[k]
        elif isinstance(data, list):
            return data

        return []
    except Exception as e:
        print(f"❌ API ERROR ({panel.get('name', panel['api_url'])}): {e}")
        return []

# ------------------ START SYSTEM ------------------
print("🚀 BOT STARTED (CLEANED: DOLPHIN & XUP REMOVED)")

# ------------------ MASTER ENGINE LOOP ------------------
while True:
    for panel in PANELS:
        panel_name = panel.get("name", "Standard Panel")
        entries = fetch_sms(panel)
        
        for entry in entries:
            msg, phone, date, service_name, direct_otp = parse_entry_fields(entry)

            if not msg or not phone:
                continue

            uid = f"{phone}-{msg}-{date}"
            if uid in processed_ids:
                continue

            otp = extract_otp(msg) or direct_otp

            if not otp:
                processed_ids.add(uid)
                continue

            final_msg = format_message(phone, otp, msg, service_name)
            if send_telegram(final_msg):
                print(f"SUCCESS ({panel_name}) : {otp}")

            processed_ids.add(uid)

    time.sleep(3)
    