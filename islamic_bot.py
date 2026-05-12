#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════╗
║       🕌 البوت الإسلامي لتيليغرام        ║
║  أذكار | آيات | أحاديث | أوقات الصلاة   ║
╚══════════════════════════════════════════╝

التثبيت:
  pip install python-telegram-bot requests

التشغيل:
  python islamic_bot.py
"""

import logging
import random
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)

# ══════════════════════════════════════════
#   🔑 ضع TOKEN البوت هنا من @BotFather
# ══════════════════════════════════════════
BOT_TOKEN = "ضع_توكن_البوت_هنا"

# ══════════════════════════════════════════
#   📍 إحداثيات مدينتك لأوقات الصلاة
#   (الافتراضي: الرياض)
# ══════════════════════════════════════════
LATITUDE  = "24.6877"
LONGITUDE = "46.7219"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ════════════════════════════════════════════════════════
#                    البيانات الدينية
# ════════════════════════════════════════════════════════

ADHKAR_SABAH = [
    "🌅 *ذكر الصباح*\n\nأَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ.",
    "🌅 *ذكر الصباح*\n\nاللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ النُّشُورُ.",
    "🌅 *ذكر الصباح — سيد الاستغفار* ✨\n\nاللَّهُمَّ أَنْتَ رَبِّي لَا إِلَٰهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَىٰ عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ.",
    "🌅 *ذكر الصباح*\n\nبِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ.\n_(٣ مرات)_",
    "🌅 *ذكر الصباح*\n\nاللَّهُمَّ عَافِنِي فِي بَدَنِي، اللَّهُمَّ عَافِنِي فِي سَمْعِي، اللَّهُمَّ عَافِنِي فِي بَصَرِي، لَا إِلَٰهَ إِلَّا أَنْتَ.\n_(٣ مرات)_",
    "🌅 *ذكر الصباح*\n\nأَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ.\n_(٣ مرات)_",
    "🌅 *ذكر الصباح*\n\nرَضِيتُ بِاللَّهِ رَبًّا، وَبِالإِسْلَامِ دِينًا، وَبِمُحَمَّدٍ ﷺ نَبِيًّا.\n_(٣ مرات)_",
]

ADHKAR_MASA = [
    "🌙 *ذكر المساء*\n\nأَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ.",
    "🌙 *ذكر المساء*\n\nاللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ الْمَصِيرُ.",
    "🌙 *ذكر المساء — سيد الاستغفار* ✨\n\nاللَّهُمَّ أَنْتَ رَبِّي لَا إِلَٰهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَىٰ عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ.",
    "🌙 *ذكر المساء*\n\nاللَّهُمَّ إِنِّي أَمْسَيْتُ أُشْهِدُكَ وَأُشْهِدُ حَمَلَةَ عَرْشِكَ وَمَلَائِكَتَكَ وَجَمِيعَ خَلْقِكَ أَنَّكَ أَنْتَ اللَّهُ لَا إِلَٰهَ إِلَّا أَنْتَ وَأَنَّ مُحَمَّدًا عَبْدُكَ وَرَسُولُكَ.\n_(٤ مرات)_",
    "🌙 *ذكر المساء*\n\nاللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَفْوَ وَالْعَافِيَةَ فِي الدُّنْيَا وَالْآخِرَةِ.",
    "🌙 *ذكر المساء*\n\nاللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْهَمِّ وَالْحَزَنِ، وَالْعَجْزِ وَالْكَسَلِ، وَالْبُخْلِ وَالْجُبْنِ، وَضَلَعِ الدَّيْنِ وَغَلَبَةِ الرِّجَالِ.",
]

AYAT = [
    {"text": "﴿وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا ۝ وَيَرْزُقْهُ مِنْ حَيْثُ لَا يَحْتَسِبُ﴾", "ref": "سورة الطلاق: ٢-٣"},
    {"text": "﴿فَإِنَّ مَعَ الْعُسْرِ يُسْرًا ۝ إِنَّ مَعَ الْعُسْرِ يُسْرًا﴾", "ref": "سورة الشرح: ٥-٦"},
    {"text": "﴿وَإِذَا سَأَلَكَ عِبَادِي عَنِّي فَإِنِّي قَرِيبٌ ۖ أُجِيبُ دَعْوَةَ الدَّاعِ إِذَا دَعَانِ﴾", "ref": "سورة البقرة: ١٨٦"},
    {"text": "﴿رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ﴾", "ref": "سورة البقرة: ٢٠١"},
    {"text": "﴿وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ﴾", "ref": "سورة البقرة: ٢١٦"},
    {"text": "﴿حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ﴾", "ref": "سورة آل عمران: ١٧٣"},
    {"text": "﴿إِنَّ اللَّهَ مَعَ الصَّابِرِينَ﴾", "ref": "سورة البقرة: ١٥٣"},
    {"text": "﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾", "ref": "سورة الرعد: ٢٨"},
    {"text": "﴿وَقُل رَّبِّ زِدْنِي عِلْمًا﴾", "ref": "سورة طه: ١١٤"},
    {"text": "﴿وَلَا تَيْأَسُوا مِن رَّوْحِ اللَّهِ﴾", "ref": "سورة يوسف: ٨٧"},
    {"text": "﴿إِنَّ اللَّهَ لَا يُضِيعُ أَجْرَ الْمُحْسِنِينَ﴾", "ref": "سورة التوبة: ١٢٠"},
    {"text": "﴿وَمَا تَوْفِيقِي إِلَّا بِاللَّهِ ۚ عَلَيْهِ تَوَكَّلْتُ وَإِلَيْهِ أُنِيبُ﴾", "ref": "سورة هود: ٨٨"},
]

AHADITH = [
    {"text": "إنما الأعمال بالنيات، وإنما لكل امرئ ما نوى.", "ref": "متفق عليه"},
    {"text": "المسلم من سَلِم المسلمون من لسانه ويده.", "ref": "متفق عليه"},
    {"text": "لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه.", "ref": "متفق عليه"},
    {"text": "من كان يؤمن بالله واليوم الآخر فليقل خيراً أو ليصمت.", "ref": "متفق عليه"},
    {"text": "الطهور شطر الإيمان، والحمد لله تملأ الميزان.", "ref": "رواه مسلم"},
    {"text": "ابتسامتك في وجه أخيك صدقة.", "ref": "رواه الترمذي"},
    {"text": "من نفَّس عن مؤمن كربةً من كرب الدنيا، نفَّس الله عنه كربةً من كرب يوم القيامة.", "ref": "رواه مسلم"},
    {"text": "اتقِ الله حيثما كنت، وأتبع السيئة الحسنة تمحها، وخالق الناس بخلق حسن.", "ref": "رواه الترمذي"},
    {"text": "كلمتان خفيفتان على اللسان، ثقيلتان في الميزان: سبحان الله وبحمده، سبحان الله العظيم.", "ref": "متفق عليه"},
    {"text": "خير الناس أنفعهم للناس.", "ref": "رواه الطبراني"},
    {"text": "من صلى الفجر في جماعة فهو في ذمة الله.", "ref": "رواه مسلم"},
    {"text": "الدنيا سجن المؤمن وجنة الكافر.", "ref": "رواه مسلم"},
]

# ════════════════════════════════════════════════════════
#                     دوال مساعدة
# ════════════════════════════════════════════════════════

def get_prayer_times():
    """جلب أوقات الصلاة من aladhan.com"""
    try:
        url = f"http://api.aladhan.com/v1/timings?latitude={LATITUDE}&longitude={LONGITUDE}&method=4"
        r = requests.get(url, timeout=10)
        data = r.json()
        if data["code"] == 200:
            t = data["data"]["timings"]
            return {
                "الفجر":  t["Fajr"],
                "الشروق": t["Sunrise"],
                "الظهر":  t["Dhuhr"],
                "العصر":  t["Asr"],
                "المغرب": t["Maghrib"],
                "العشاء": t["Isha"],
            }
    except Exception:
        pass
    return None

def main_keyboard():
    buttons = [
        [
            InlineKeyboardButton("🌅 ذكر الصباح", callback_data="sabah"),
            InlineKeyboardButton("🌙 ذكر المساء", callback_data="masa"),
        ],
        [
            InlineKeyboardButton("📖 آية اليوم",   callback_data="aya"),
            InlineKeyboardButton("📿 حديث اليوم",  callback_data="hadith"),
        ],
        [InlineKeyboardButton("🕌 أوقات الصلاة", callback_data="salah")],
    ]
    return InlineKeyboardMarkup(buttons)

# ════════════════════════════════════════════════════════
#                    معالجات الأوامر
# ════════════════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🕌 *أهلاً بك في البوت الإسلامي*\n\n"
        "اختر من القائمة أو استخدم الأوامر:\n\n"
        "🌅 /sabah  — ذكر الصباح\n"
        "🌙 /masa   — ذكر المساء\n"
        "📖 /aya    — آية قرآنية\n"
        "📿 /hadith — حديث نبوي\n"
        "🕌 /salah  — أوقات الصلاة\n"
        "❓ /help   — المساعدة"
    )
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=main_keyboard())

async def sabah_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(ADHKAR_SABAH), parse_mode="Markdown", reply_markup=main_keyboard())

async def masa_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(ADHKAR_MASA), parse_mode="Markdown", reply_markup=main_keyboard())

async def aya_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = random.choice(AYAT)
    msg = f"📖 *آية اليوم*\n\n{item['text']}\n\n_{item['ref']}_"
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=main_keyboard())

async def hadith_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = random.choice(AHADITH)
    msg = f"📿 *حديث نبوي شريف*\n\nقال ﷺ:\n\n«{item['text']}»\n\n_{item['ref']}_"
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=main_keyboard())

async def salah_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ جاري جلب أوقات الصلاة...")
    times = get_prayer_times()
    if times:
        lines = "\n".join([f"  {name}: ⏰ `{t}`" for name, t in times.items()])
        msg = f"🕌 *أوقات الصلاة اليوم*\n\n{lines}\n\n_اللهم اجعلنا من المحافظين على الصلاة_ 🤲"
    else:
        msg = "⚠️ تعذّر جلب أوقات الصلاة، حاول لاحقاً."
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=main_keyboard())

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📋 *قائمة الأوامر*\n\n"
        "🌅 /sabah  — ذكر من أذكار الصباح\n"
        "🌙 /masa   — ذكر من أذكار المساء\n"
        "📖 /aya    — آية قرآنية كريمة\n"
        "📿 /hadith — حديث نبوي شريف\n"
        "🕌 /salah  — أوقات الصلاة\n"
        "❓ /help   — عرض هذه القائمة\n\n"
        "أو استخدم الأزرار أدناه 👇"
    )
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=main_keyboard())

# ════════════════════════════════════════════════════════
#                  معالج الأزرار التفاعلية
# ════════════════════════════════════════════════════════

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    d = query.data

    if d == "sabah":
        text = random.choice(ADHKAR_SABAH)
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=main_keyboard())

    elif d == "masa":
        text = random.choice(ADHKAR_MASA)
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=main_keyboard())

    elif d == "aya":
        item = random.choice(AYAT)
        msg = f"📖 *آية اليوم*\n\n{item['text']}\n\n_{item['ref']}_"
        await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=main_keyboard())

    elif d == "hadith":
        item = random.choice(AHADITH)
        msg = f"📿 *حديث نبوي شريف*\n\nقال ﷺ:\n\n«{item['text']}»\n\n_{item['ref']}_"
        await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=main_keyboard())

    elif d == "salah":
        await query.edit_message_text("⏳ جاري جلب أوقات الصلاة...")
        times = get_prayer_times()
        if times:
            lines = "\n".join([f"  {name}: ⏰ `{t}`" for name, t in times.items()])
            msg = f"🕌 *أوقات الصلاة اليوم*\n\n{lines}\n\n_اللهم اجعلنا من المحافظين على الصلاة_ 🤲"
        else:
            msg = "⚠️ تعذّر جلب أوقات الصلاة، حاول لاحقاً."
        await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=main_keyboard())

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اختر من القائمة 👇", reply_markup=main_keyboard())

# ════════════════════════════════════════════════════════
#                      تشغيل البوت
# ════════════════════════════════════════════════════════

def main():
    print("🕌 البوت الإسلامي يعمل الآن... اضغط Ctrl+C للإيقاف")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",  start))
    app.add_handler(CommandHandler("sabah",  sabah_cmd))
    app.add_handler(CommandHandler("masa",   masa_cmd))
    app.add_handler(CommandHandler("aya",    aya_cmd))
    app.add_handler(CommandHandler("hadith", hadith_cmd))
    app.add_handler(CommandHandler("salah",  salah_cmd))
    app.add_handler(CommandHandler("help",   help_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    app.run_polling()

if __name__ == "__main__":
    main()
