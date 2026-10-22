"""
Comprehensive Open-Source Inspired Scam, Phishing, Fraud, and Social Engineering Threat Intelligence Database.
Categorized dictionaries covering global + regional cybercrime, banking frauds, lottery/pension scams,
cryptocurrency scams, sextortion/blackmail, tech support, package delivery, and fake government agencies.
"""

SCAM_INTEL_CATEGORIES = {
    "Credential or OTP harvesting": {
        "base_weight": 30,
        "bonus": 6,
        "keywords": [
            "one time password", "one-time password", "verification code", "security code",
            "share your otp", "send otp", "enter otp", "provide otp", "forward otp", "read otp",
            "otp expired", "resend otp", "otp requested", "otp verification", "sms otp",
            "cvv", "cvv2", "cvc", "security number", "3-digit code", "3 digit code",
            "atm pin", "enter pin", "card pin", "secret pin", "mpin", "tpin", "upi pin",
            "debit pin", "complete your debit pin", "enter your pin", "dc pin", "confrim your dc pin",
            "confrim", "confirm your dc pin", "confirm pin", "verify your pin", "pin",
            "regain access", "access your account", "restore after authentication", "authentication information",
            "seed phrase", "recovery phrase", "private key", "secret phrase", "wallet key",
            "secret code", "master password", "passcode", "backup code", "2fa code", "mfa code",
            "authenticator code", "share your password", "enter your password", "confirm your password",
            "update your password", "reset password link", "re-enter password", "type your password",
            "login credentials", "internet banking credentials", "netbanking password"
        ]
    },

    "Banking & Personal Data Harvesting": {
        "base_weight": 28,
        "bonus": 5,
        "keywords": [
            "share your bank", "bank account number", "bank account details", "bank details",
            "account details", "account number", "savings account", "current account",
            "share your details", "send your details", "provide your details", "submit your details",
            "enter your details", "fill your details", "update your details", "verify your details",
            "upi id", "upi-id", "vpa", "bhim upi", "google pay number", "phonepe number", "paytm number",
            "atm details", "atm card", "debit card number", "credit card number", "card details",
            "card number", "expiry date", "valid thru", "cardholder name", "name on card", "debit card",
            "aadhaar", "aadhar", "uidai", "pan card", "pan number", "pan details", "link pan",
            "passport number", "driving licence", "driver license", "voter id", "ssn", "social security",
            "social security number", "tax id", "tin number", "national id", "ifsc code", "ifsc",
            "branch code", "routing number", "swift code", "sort code", "iban", "bic"
        ]
    },

    "Urgency, Coercion & Pressure Tactics": {
        "base_weight": 18,
        "bonus": 4,
        "keywords": [
            "urgent", "immediately", "act now", "right now", "right away", "within 24", "within 48",
            "within 12 hours", "within 2 hours", "last warning", "final warning", "expires today",
            "limited time", "do not ignore", "final notice", "last chance", "time is running out",
            "before it expires", "action required", "mandatory action", "respond immediately",
            "asap", "hurry", "don't delay", "as soon as possible", "without delay", "must be done today",
            "your time is limited", "deadline", "expiring soon", "immediate action", "fail to respond",
            "otherwise your", "legal proceedings", "arrest warrant", "police complaint",
            "at earliest convenience", "actions here", "wygasa", "wygasa za",
            "expires tonight", "expiring tonight"
        ]
    },

    "Account Suspension & Security Threat": {
        "base_weight": 26,
        "bonus": 5,
        "keywords": [
            "account suspended", "account has been suspended", "account has been locked", "account locked",
            "account blocked", "account restricted", "account deactivated", "account closed", "account on hold",
            "card is locked", "card has been locked", "card locked", "card blocked", "services stopped",
            "sim blocked", "sim deactivated", "electricity disconnected", "power cut today",
            "verify your account", "confirm your account", "unusual activity", "suspicious activity",
            "unauthorized access", "unrecognized login", "identity verification", "verify your identity",
            "your account will be", "account has been", "account is at risk", "security alert",
            "security warning", "fraud alert", "someone tried to", "compromised", "hacked",
            "unauthorized transaction", "device registered", "suspicious sign-in", "unusual sign-in",
            "block ho jayega", "account band ho jayega", "aaj block", "citi alert", "wells fargo",
            "profile locked", "locked your debit", "temporarily blocked", "card has been disabled",
            "card disabled", "on hold", "bank alert", "unusual attempt", "account access has been limited",
            "limited your access", "access has been limited", "limited access", "temporarily frozen",
            "frozen your account", "due to unusual activity", "fraudulent activity", "mobile number has changed",
            "if this was not you", "expired identity information", "terminated the use of", "citi_service",
            "protect sms code", "unlock your account", "rinnovo", "procedere al rinnovo",
            "compte bancaire", "cuenta bancaria", "konto gesperrt", "verification requise"
        ]
    },

    "Prize, Lottery, Bonus & Reward Lures": {
        "base_weight": 26,
        "bonus": 5,
        "keywords": [
            "you have won", "you have been selected", "you are selected", "congratulations",
            "congrats", "winner", "lucky winner", "lucky customer", "lucky draw", "lottery",
            "kbc lottery", "kaun banega crorepati", "claim prize", "claim your", "claim reward",
            "prize money", "reward money", "bonus amount", "gift card", "gift voucher", "free gift",
            "you are going to get", "you will receive", "you will get", "going to receive",
            "eligible for", "entitled to", "annual customer", "valuable customer", "valued customer",
            "special customer", "loyal customer", "most valuable", "selected for a reward",
            "won a prize", "scratch card", "cash prize", "jackpot", "unclaimed funds",
            "inheritance", "beneficiary of", "consignment box", "fund transfer",
            "bonus code", "online casino", "deposit to claim", "freebie", "casino bonus",
            "free bets", "deposit now", "gamble responsibly", "immediate cash in/out",
            "cash in/out", "register to get", "best online casino", "max bonus",
            "match up to", "slots", "coupon code", "live casino", "cash-boost",
            "cash boost", "einzahlungen"
        ]
    },

    "Payment, Refund & Billing Lures": {
        "base_weight": 20,
        "bonus": 4,
        "keywords": [
            "payment failed", "refund", "refund approval", "tax refund", "unpaid invoice",
            "unusual charge", "processing fee", "advance fee", "pay now", "bank transfer",
            "wallet address", "pay immediately", "payment pending", "outstanding balance",
            "overdue payment", "billing issue", "cashback", "cash back", "reward points",
            "redeem points", "transaction failed", "payment declined", "auto-debit", "chargeback",
            "customs clearance fee", "handling charges", "courier fee", "delivery charges",
            "awaiting your payment", "still owe", "pay fee for delivery", "pay the cost to complete"
        ]
    },

    "KYC, Identity & Utility Disconnection Scams": {
        "base_weight": 26,
        "bonus": 5,
        "keywords": [
            "kyc update", "kyc verification", "update kyc", "complete kyc", "kyc expired",
            "kyc pending", "verify kyc", "kyc mandatory", "kyc required", "pan verification",
            "aadhaar verification", "link aadhaar", "link pan", "re-kyc", "ekyc", "e-kyc",
            "ckyc", "sim kyc", "bank kyc", "wallet kyc", "paytm kyc", "document verification",
            "electricity power supply", "power supply will be disconnected", "electricity will be disconnected",
            "bill was not updated", "electricity officer", "electricity bill unpaid", "power cut today",
            "chalan pending", "traffic chalan", "echallan", "e-challan", "court summons",
            "bijli connection", "bijli kat di", "pan link", "turant kyc", "sim block"
        ]
    },

    "Crypto, Ponzi & Fake Investment Fraud": {
        "base_weight": 26,
        "bonus": 6,
        "keywords": [
            "guaranteed return", "guaranteed profit", "double your money", "triple your money",
            "double your bitcoin", "trading pool", "deposit minimum", "airdrop", "connect wallet",
            "crypto giveaway", "investment opportunity", "trading signal", "forex signal",
            "binary option", "mining pool", "high return", "passive income", "financial freedom",
            "earn from home", "daily profit", "monthly return", "no risk", "100% safe investment",
            "elon musk giveaway", "bitcoin bonus", "ethereum giveaway", "usdt deposit",
            "recharge task", "order grabbing", "youtube like subscribe job", "telegram task",
            "prepaid task", "vip investment"
        ]
    },

    "Loan & Financial Fraud": {
        "base_weight": 22,
        "bonus": 5,
        "keywords": [
            "to get your loan", "get your loan", "loan of up to", "pozyczke", "instant loan",
            "personal loan approved", "pre-approved loan", "loan disbursement", "low interest loan",
            "collateral free loan", "quick loan approval", "loan amount sanctioned"
        ]
    },

    "Job, Part-Time & Task Scam Offers": {
        "base_weight": 22,
        "bonus": 5,
        "keywords": [
            "job offer", "job opportunity", "hiring now", "earn money", "earn daily", "earn weekly",
            "part time job", "part-time job", "work from home", "online job", "data entry job",
            "typing job", "registration fee", "joining fee", "salary per month", "per day salary",
            "no experience required", "no qualification", "daily payout", "earn 2000-5000",
            "hotel review job", "google map rating job", "like videos and earn", "hr recruiter",
            "interview cleared", "appointment letter", "offer letter attached"
        ]
    },

    "Delivery, Customs & Package Phishing": {
        "base_weight": 22,
        "bonus": 4,
        "keywords": [
            "parcel", "package", "delivery failed", "customs fee", "shipping fee", "delivery attempt",
            "courier", "track your order", "reschedule delivery", "shipment on hold",
            "customs clearance", "undelivered package", "incorrect address", "update address",
            "fedex delivery", "dhl express", "india post", "usps package", "ups shipment",
            "royal mail", "hermes delivery", "redelivery fee", "usps", "track from usps",
            "shipment address", "confirm the shipment", "pending delivery", "tracking code",
            "usps delivery", "awaiting your payment", "complete the actions here",
            "important alert regarding your", "package is waiting", "delivery process",
            "unpaid fees", "being held due to", "parcel is being held", "redelivery charge",
            "parcei", "heid"
        ]
    },

    "Authority & Corporate Impersonation": {
        "base_weight": 22,
        "bonus": 5,
        "keywords": [
            "customer support", "bank security", "security team", "fraud prevention department",
            "tax department", "income tax", "police department", "microsoft support", "apple support",
            "google support", "amazon support", "paypal support", "netflix billing", "official representative",
            "government agency", "reserve bank", "rbi", "sbi", "hdfc", "icici", "axis bank",
            "punjab national bank", "bank of baroda", "central bank", "from the desk of",
            "official notice", "legal notice", "ministry of", "department of", "cyber cell",
            "interpol", "cbi", "enforcement directorate", "ed notice", "customs department",
            "telecom department", "trai", "fbi", "irs agent", "federal reserve",
            "citbank", "boa bank", "westpac", "commbank", "cba", "anz", "services ontario",
            "cbi and cyber cell"
        ]
    },

    "Link Click & App Download Coercion": {
        "base_weight": 18,
        "bonus": 4,
        "keywords": [
            "click below", "click here", "click the link", "click on the link", "tap the link",
            "open the link", "visit the link", "below link", "link below", "click to verify",
            "click to confirm", "click to claim", "click to update", "click to unlock",
            "click to activate", "scan the qr", "scan qr code", "scan this code", "download the app",
            "install the app", "download anydesk", "download teamviewer", "download rustdesk",
            "quicksupport", "screen share", "install apk", "download apk", "click on apk",
            "follow here", "follow this link", "complete the actions", "cliccando sul link",
            "procedere al rinnovo", "cliquez ici", "haga clic", "hier klicken", "suivez le lien"
        ]
    },

    "Generic Scam Greetings & Suspicious Openers": {
        "base_weight": 12,
        "bonus": 3,
        "keywords": [
            "dear customer", "dear user", "dear valued", "dear sir", "dear madam",
            "dear sir/madam", "dear account holder", "dear beneficiary", "dear winner",
            "dear member", "dear friend", "respected sir", "respected customer",
            "dear esteemed", "hello dear", "attention please", "kind attention",
            "we are happy to inform", "happy to inform", "pleased to inform",
            "glad to inform", "this is to inform", "we wish to inform"
        ]
    },

    "Off-Platform Contact & Redirection": {
        "base_weight": 14,
        "bonus": 4,
        "keywords": [
            "contact us on whatsapp", "message on telegram", "call this number", "contact agent",
            "reach us on", "whatsapp us", "reply on whatsapp", "text us on", "join our channel",
            "join group", "dm us", "send message to", "contact on", "call us at", "call manager",
            "whatsapp helpline", "telegram executive", "chat with executive"
        ]
    },

    "Sextortion & Blackmail Coercion": {
        "base_weight": 35,
        "bonus": 8,
        "keywords": [
            "i know your password", "i have recorded you", "recorded video of you",
            "compromised your webcam", "dirty video", "send to all your contacts",
            "pay in bitcoin", "transfer btc", "i will ruin your reputation",
            "adult website", "watching porn", "pegasus spyware", "trojan virus installed"
        ]
    }
}
