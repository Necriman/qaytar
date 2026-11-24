"""All user-facing texts (uz = O'zbekcha lotin, ru = Русский). HTML parse mode."""

T: dict[str, dict[str, str]] = {
    # ---------- start / menu ----------
    "choose_lang": {
        "uz": (
            "🇺🇿 <b>Assalomu alaykum!</b> Qulay tilni tanlang.\n"
            "🇷🇺 <b>Здравствуйте!</b> Выберите удобный язык.\n\n"
            "<i>Tilni keyin ham o'zgartirish mumkin: 🌐 Til / Язык</i>"
        ),
        "ru": (
            "🇺🇿 <b>Assalomu alaykum!</b> Qulay tilni tanlang.\n"
            "🇷🇺 <b>Здравствуйте!</b> Выберите удобный язык.\n\n"
            "<i>Язык можно поменять позже: 🌐 Til / Язык</i>"
        ),
    },
    "welcome": {
        "uz": (
            "<b>Assalomu alaykum! Men — Qaytar 🛡</b>\n\n"
            "Kontrakt, xususiy bog'cha yoki maktab va ipoteka uchun to'lagan pulingizning "
            "<b>12% ini davlatdan qaytarib olishga</b> yordam beraman.\n\n"
            "💡 Masalan: 20 mln so'm kontrakt → <b>2 400 000 so'm</b> qaytadi.\n\n"
            "Nima qila olaman:\n"
            "✅ 1 daqiqada huquqingizni tekshiraman va summani hisoblayman\n"
            "📄 Hujjatlaringizdagi xatolarni topaman\n"
            "🧭 Soliq ilovasida qadamma-qadam yo'l ko'rsataman\n"
            "🤝 Xohlasangiz — birga topshiramiz\n\n"
            "🔐 <i>Biz hech qachon parol, ERI, SMS-kod yoki karta ma'lumotlarini so'ramaymiz.</i>\n\n"
            "Boshlash uchun quyidagi tugmani bosing 👇"
        ),
        "ru": (
            "<b>Здравствуйте! Я — Qaytar 🛡</b>\n\n"
            "Помогаю <b>вернуть от государства 12%</b> денег, потраченных на контракт в вузе, "
            "частный сад или школу и ипотеку.\n\n"
            "💡 Например: контракт 20 млн сум → вернётся <b>2 400 000 сум</b>.\n\n"
            "Что я умею:\n"
            "✅ За 1 минуту проверю право и посчитаю сумму\n"
            "📄 Найду ошибки в ваших документах\n"
            "🧭 Пошагово проведу по приложению Soliq\n"
            "🤝 Если хотите — подадим вместе\n\n"
            "🔐 <i>Мы никогда не просим пароли, ЭЦП, SMS-коды или данные карты.</i>\n\n"
            "Нажмите кнопку ниже, чтобы начать 👇"
        ),
    },
    "btn_check": {"uz": "✅ Huquqimni tekshirish", "ru": "✅ Проверить право"},
    "btn_docs": {"uz": "📄 Hujjatlarni tekshirish", "ru": "📄 Проверить документы"},
    "btn_guide": {"uz": "🧭 Yo'riqnoma", "ru": "🧭 Инструкция"},
    "btn_book": {"uz": "🤝 Birga topshiramiz", "ru": "🤝 Подать вместе"},
    "btn_articles": {"uz": "📚 Maqolalar", "ru": "📚 Статьи"},
    "btn_remind": {"uz": "⏰ Eslatmalar", "ru": "⏰ Напоминания"},
    "btn_privacy": {"uz": "🔒 Maxfiylik", "ru": "🔒 Конфиденциальность"},
    "btn_lang": {"uz": "🌐 Til / Язык", "ru": "🌐 Til / Язык"},
    "menu_hint": {"uz": "Asosiy menyu 👇", "ru": "Главное меню 👇"},
    "cancel": {"uz": "❌ Bekor qilish", "ru": "❌ Отмена"},
    "cancelled": {"uz": "Bekor qilindi. Asosiy menyu 👇", "ru": "Отменено. Главное меню 👇"},
    "unknown": {
        "uz": "Tushunmadim 🙂 Menyudagi tugmalardan foydalaning.",
        "ru": "Не понял 🙂 Пожалуйста, используйте кнопки меню.",
    },

    # ---------- privacy consent ----------
    "consent_basic": {
        "uz": (
            "<b>🔒 Shaxsiy ma'lumotlar haqida qisqacha</b>\n\n"
            "Hisob-kitob uchun faqat siz kiritgan raqamlarni (to'lov summasi, maosh) saqlaymiz — "
            "statistika uchun. Ism, telefon va hujjatlar <b>bu bosqichda so'ralmaydi</b>.\n\n"
            "Davom etish orqali siz O'zbekiston Respublikasining «Shaxsga doir ma'lumotlar to'g'risida»gi "
            "Qonuniga muvofiq ma'lumotlaringiz qayta ishlanishiga rozilik bildirasiz.\n\n"
            "📄 <a href=\"{privacy}\">Maxfiylik siyosati</a> · <a href=\"{terms}\">Foydalanish shartlari</a>"
        ),
        "ru": (
            "<b>🔒 Коротко о персональных данных</b>\n\n"
            "Для расчёта мы сохраняем только введённые вами цифры (сумма оплаты, зарплата) — "
            "для статистики. Имя, телефон и документы <b>на этом шаге не запрашиваются</b>.\n\n"
            "Продолжая, вы даёте согласие на обработку данных в соответствии с Законом "
            "Республики Узбекистан «О персональных данных».\n\n"
            "📄 <a href=\"{privacy}\">Политика конфиденциальности</a> · <a href=\"{terms}\">Условия использования</a>"
        ),
    },
    "btn_agree": {"uz": "✅ Roziman", "ru": "✅ Согласен(на)"},
    "btn_disagree": {"uz": "❌ Rozi emasman", "ru": "❌ Не согласен(на)"},
    "consent_declined": {
        "uz": "Tushunarli. Rozilik bermasangiz ham <b>🧭 Yo'riqnoma</b> va <b>📚 Maqolalar</b> bo'limlaridan bemalol foydalanishingiz mumkin.",
        "ru": "Понятно. Без согласия вы всё равно можете пользоваться разделами <b>🧭 Инструкция</b> и <b>📚 Статьи</b>.",
    },

    # ---------- eligibility wizard ----------
    "q_kind": {
        "uz": "<b>1/5.</b> Nima uchun to'lagansiz?",
        "ru": "<b>1/5.</b> За что вы платили?",
    },
    "kind_uni": {"uz": "🎓 OTM kontrakti", "ru": "🎓 Контракт в вузе"},
    "kind_school": {"uz": "🏫 Xususiy bog'cha / maktab", "ru": "🏫 Частный сад / школа"},
    "kind_mortgage": {"uz": "🏠 Ipoteka", "ru": "🏠 Ипотека"},
    "q_who": {
        "uz": "<b>2/5.</b> Kim uchun to'langan?",
        "ru": "<b>2/5.</b> За кого платили?",
    },
    "who_self": {"uz": "🙋 O'zim uchun", "ru": "🙋 За себя"},
    "who_child": {"uz": "👧 Farzandim uchun", "ru": "👧 За ребёнка"},
    "who_spouse": {"uz": "💍 Turmush o'rtog'im uchun", "ru": "💍 За супруга(у)"},
    "q_age": {
        "uz": "O'qiyotgan shaxs <b>26 yoshdan kichikmi</b>?",
        "ru": "Учащемуся <b>меньше 26 лет</b>?",
    },
    "yes": {"uz": "✅ Ha", "ru": "✅ Да"},
    "no": {"uz": "❌ Yo'q", "ru": "❌ Нет"},
    "dont_know": {"uz": "🤷 Bilmayman", "ru": "🤷 Не знаю"},
    "not_eligible_age": {
        "uz": (
            "😔 Farzand yoki turmush o'rtog'i uchun to'lovda imtiyoz odatda <b>26 yoshgacha</b> bo'lganlar uchun beriladi.\n\n"
            "Agar o'qiyotgan shaxsning o'zi rasmiy ishlasa va o'zi to'lasa — u o'zi uchun qaytarib olishi mumkin. "
            "Qaytadan tekshirib ko'ring: <b>✅ Huquqimni tekshirish</b>."
        ),
        "ru": (
            "😔 Льгота за ребёнка или супруга(у) обычно действует, если учащемуся <b>меньше 26 лет</b>.\n\n"
            "Если учащийся сам официально работает и платит сам — он может вернуть налог за себя. "
            "Проверьте ещё раз: <b>✅ Проверить право</b>."
        ),
    },
    "q_employed": {
        "uz": (
            "<b>3/5.</b> To'lovni qilgan odam <b>rasmiy ishlaydimi</b> va maoshidan <b>12% daromad solig'i</b> ushlanadimi?\n\n"
            "<i>💡 Bu eng muhim shart: davlat faqat ushlab qolingan soliqni qaytaradi.</i>"
        ),
        "ru": (
            "<b>3/5.</b> Тот, кто платил, <b>официально работает</b>, и с его зарплаты удерживают <b>12% подоходного налога</b>?\n\n"
            "<i>💡 Это главное условие: государство возвращает только удержанный налог.</i>"
        ),
    },
    "not_eligible_employed": {
        "uz": (
            "😔 Afsuski, rasmiy daromad va ushlangan soliq bo'lmasa, qaytariladigan pul ham bo'lmaydi.\n\n"
            "💡 <b>Maslahat:</b> oiladagi boshqa rasmiy ishlaydigan a'zo (masalan, ota yoki ona) keyingi to'lovlarni "
            "<b>o'z kartasidan, o'z nomidan</b> qilsa — keyingi yil u 12% ni qaytarib oladi."
        ),
        "ru": (
            "😔 К сожалению, без официального дохода и удержанного налога возвращать нечего.\n\n"
            "💡 <b>Совет:</b> если следующие платежи будет делать другой член семьи с официальной работой "
            "(например, отец или мать) — <b>со своей карты и на своё имя</b>, то в следующем году он вернёт 12%."
        ),
    },
    "employed_unknown": {
        "uz": (
            "Buni tekshirish oson: <b>Soliq</b> ilovasi → «Daromadlarim» bo'limida ish beruvchi to'lagan daromad va "
            "ushlangan soliq ko'rinadi. Hozircha <b>ha</b> deb hisoblaymiz 👇"
        ),
        "ru": (
            "Это легко проверить: в приложении <b>Soliq</b> → раздел «Мои доходы» видны доходы от работодателя "
            "и удержанный налог. Пока посчитаем, что <b>да</b> 👇"
        ),
    },
    "q_paid": {
        "uz": "<b>4/5.</b> Yil davomida <b>qancha to'ladingiz</b>? (so'mda)\n\n<i>Masalan: 20000000 yoki 20 mln</i>",
        "ru": "<b>4/5.</b> <b>Сколько вы заплатили</b> за год? (в сумах)\n\n<i>Например: 20000000 или 20 млн</i>",
    },
    "q_salary": {
        "uz": (
            "<b>5/5.</b> To'lovchining <b>oylik rasmiy maoshi</b> qancha? (soliq ushlanishidan oldin)\n\n"
            "<i>Bu qaytarish chegarasini hisoblash uchun kerak: 12% dan ortiq qaytmaydi. Masalan: 6 mln</i>"
        ),
        "ru": (
            "<b>5/5.</b> Какая <b>официальная зарплата в месяц</b> у плательщика? (до удержания налога)\n\n"
            "<i>Нужно, чтобы посчитать лимит: вернуть можно не больше удержанного налога. Например: 6 млн</i>"
        ),
    },
    "bad_number": {
        "uz": "🤔 Summani tushunmadim. Faqat raqam yozing, masalan: <code>20000000</code> yoki <code>20 mln</code>",
        "ru": "🤔 Не понял сумму. Напишите число, например: <code>20000000</code> или <code>20 млн</code>",
    },
    "result": {
        "uz": (
            "🎉 <b>Siz taxminan {refund} so'm qaytarib olishingiz mumkin!</b>\n\n"
            "📊 Hisob-kitob:\n"
            "• To'langan: {paid} so'm × 12% = {by_expense} so'm\n"
            "• Yil davomida ushlangan soliq (taxminan): {by_tax} so'm\n"
            "{limit_note}"
            "\n📅 <b>{year}-yil</b> xarajatlari uchun deklaratsiya <b>{deadline}</b> gacha topshiriladi. "
            "Pul ariza qabul qilingandan keyin <b>15 ish kuni</b> ichida kartaga tushadi.\n\n"
            "<i>⚠️ Bu taxminiy hisob. Yakuniy qarorni soliq organi qabul qiladi.</i>\n\n"
            "Keyingi qadam 👇"
        ),
        "ru": (
            "🎉 <b>Вы можете вернуть примерно {refund} сум!</b>\n\n"
            "📊 Расчёт:\n"
            "• Оплачено: {paid} сум × 12% = {by_expense} сум\n"
            "• Удержанный за год налог (примерно): {by_tax} сум\n"
            "{limit_note}"
            "\n📅 Декларацию за расходы <b>{year} года</b> подают до <b>{deadline}</b>. "
            "Деньги приходят на карту в течение <b>15 рабочих дней</b> после принятия заявления.\n\n"
            "<i>⚠️ Это примерный расчёт. Окончательное решение принимает налоговый орган.</i>\n\n"
            "Следующий шаг 👇"
        ),
    },
    "limit_note": {
        "uz": "• ⚠️ Qaytarish ushlangan soliq bilan cheklangan, shuning uchun summa kamroq.\n",
        "ru": "• ⚠️ Возврат ограничен удержанным налогом, поэтому сумма меньше.\n",
    },
    "mortgage_note": {
        "uz": "\n🏠 <i>Ipoteka bo'yicha qaysi to'lovlar (asosiy qarz, foizlar) hisobga olinishini bankdagi ma'lumotnoma bo'yicha tekshirib oling.</i>\n",
        "ru": "\n🏠 <i>Какие платежи по ипотеке (основной долг, проценты) учитываются — уточните по справке из банка.</i>\n",
    },

    # ---------- documents ----------
    "docs_intro": {
        "uz": (
            "<b>📄 Hujjatlarni tekshirish</b>\n\n"
            "Ko'pchilik pulni aynan hujjatdagi xato tufayli ololmaydi: to'lov <b>boshqa odamning kartasidan</b> "
            "qilingan, ism mos kelmaydi, yil noto'g'ri.\n\n"
            "Tekshirishning 2 usuli bor:\n"
            "🤖 <b>AI bilan</b> — shartnoma va cheklar rasmini yuborasiz, sun'iy intellekt ma'lumotlarni o'qiydi va solishtiradi.\n"
            "📝 <b>AI-siz</b> — 6 ta savolga javob berasiz, men xatolarni ko'rsataman. Hech qanday rasm yuborilmaydi."
        ),
        "ru": (
            "<b>📄 Проверка документов</b>\n\n"
            "Многие не получают деньги именно из-за ошибки в документах: оплата <b>с карты другого человека</b>, "
            "не совпадает ФИО, не тот год.\n\n"
            "Есть 2 способа проверки:\n"
            "🤖 <b>С ИИ</b> — вы присылаете фото договора и чеков, искусственный интеллект читает и сверяет данные.\n"
            "📝 <b>Без ИИ</b> — отвечаете на 6 вопросов, я показываю ошибки. Никакие фото не отправляются."
        ),
    },
    "btn_docs_ai": {"uz": "🤖 AI bilan tekshirish", "ru": "🤖 Проверить с ИИ"},
    "btn_docs_manual": {"uz": "📝 AI-siz (savollar)", "ru": "📝 Без ИИ (вопросы)"},
    "ai_consent": {
        "uz": (
            "<b>🤖 AI tekshiruvi uchun alohida rozilik</b>\n\n"
            "Siz yuborgan rasm:\n"
            "• faqat <b>operativ xotirada</b> qayta ishlanadi va <b>diskka yoki bazaga saqlanmaydi</b>;\n"
            "• o'qish uchun <b>Google Gemini</b> sun'iy intellekt xizmatiga (O'zbekistondan tashqaridagi serverlarga) yuboriladi;\n"
            "• tekshiruvdan so'ng xabaringiz chatdan <b>o'chiriladi</b>, o'qilgan ma'lumotlar sessiya tugashi bilan (ko'pi bilan 30 daqiqa) yo'q qilinadi.\n\n"
            "❗ <b>Pasport, ID-karta, ERI yoki karta raqamini yubormang.</b> Shartnomadagi pasport raqami va JShShIRni "
            "yopib qo'yishingiz mumkin — tekshiruvga ta'sir qilmaydi.\n\n"
            "«Roziman» tugmasini bosib, siz rasmdagi shaxsga doir ma'lumotlarni sun'iy intellekt yordamida qayta ishlash "
            "va xorijga uzatishga <b>aniq rozilik</b> bildirasiz. Rasmda boshqa shaxs (masalan, farzandingiz) ma'lumotlari "
            "bo'lsa — uning yoki qonuniy vakilining roziligi borligini tasdiqlaysiz.\n\n"
            "📄 <a href=\"{privacy}\">Maxfiylik siyosati</a>"
        ),
        "ru": (
            "<b>🤖 Отдельное согласие на проверку с ИИ</b>\n\n"
            "Присланное фото:\n"
            "• обрабатывается только <b>в оперативной памяти</b> и <b>не сохраняется на диск или в базу</b>;\n"
            "• для распознавания отправляется в сервис искусственного интеллекта <b>Google Gemini</b> (серверы за пределами Узбекистана);\n"
            "• после проверки ваше сообщение <b>удаляется</b> из чата, а распознанные данные стираются по окончании сессии (не дольше 30 минут).\n\n"
            "❗ <b>Не присылайте паспорт, ID-карту, ЭЦП или номер карты.</b> Серию паспорта и ПИНФЛ в договоре можно "
            "закрыть — на проверку это не влияет.\n\n"
            "Нажимая «Согласен(на)», вы даёте <b>явное согласие</b> на обработку персональных данных с фото с помощью "
            "искусственного интеллекта и их трансграничную передачу. Если на фото данные другого лица (например, ребёнка) — "
            "вы подтверждаете, что у вас есть его согласие или вы его законный представитель.\n\n"
            "📄 <a href=\"{privacy}\">Политика конфиденциальности</a>"
        ),
    },
    "ai_disabled": {
        "uz": "AI tekshiruvi hozir sozlanmagan. Savollar orqali tekshiramiz 👇",
        "ru": "Проверка с ИИ сейчас не настроена. Проверим через вопросы 👇",
    },
    "send_docs": {
        "uz": (
            "📸 Endi rasmlarni <b>bittadan</b> yuboring:\n"
            "1️⃣ Shartnoma (birinchi sahifa — tomonlar va summa ko'rinadigan)\n"
            "2️⃣ To'lov cheklari yoki bank ko'chirmasi\n\n"
            "Barchasini yuborgach — <b>«✅ Tekshiruvni yakunlash»</b> tugmasini bosing."
        ),
        "ru": (
            "📸 Теперь присылайте фото <b>по одному</b>:\n"
            "1️⃣ Договор (первая страница — где видны стороны и сумма)\n"
            "2️⃣ Чеки об оплате или банковская выписка\n\n"
            "Когда отправите всё — нажмите <b>«✅ Завершить проверку»</b>."
        ),
    },
    "btn_docs_done": {"uz": "✅ Tekshiruvni yakunlash", "ru": "✅ Завершить проверку"},
    "doc_reading": {"uz": "🔍 O'qiyapman...", "ru": "🔍 Читаю..."},
    "doc_read_ok": {
        "uz": "✅ Qabul qilindi: <b>{kind}</b>\n{details}\n\n🗑 <i>Rasmingiz chatdan o'chirildi va saqlanmadi.</i>\n\nYana rasm yuboring yoki tekshiruvni yakunlang.",
        "ru": "✅ Принято: <b>{kind}</b>\n{details}\n\n🗑 <i>Ваше фото удалено из чата и не сохранено.</i>\n\nПришлите ещё фото или завершите проверку.",
    },
    "doc_read_fail": {
        "uz": "😕 Rasmni o'qib bo'lmadi. Yorug'roq joyda, to'liq va tekis suratga oling, keyin qayta yuboring.",
        "ru": "😕 Не удалось прочитать фото. Сфотографируйте при хорошем свете, целиком и ровно, и пришлите снова.",
    },
    "doc_sensitive": {
        "uz": "⛔️ Bu <b>pasport / ID-karta yoki karta</b>ga o'xshaydi. Uni yubormang! Rasm o'chirildi va hech qayerda saqlanmadi.",
        "ru": "⛔️ Похоже на <b>паспорт / ID-карту или банковскую карту</b>. Не присылайте их! Фото удалено и нигде не сохранено.",
    },
    "doc_need_photo": {
        "uz": "Iltimos, hujjatni <b>rasm</b> sifatida yuboring (yoki tekshiruvni yakunlang).",
        "ru": "Пожалуйста, пришлите документ <b>фотографией</b> (или завершите проверку).",
    },
    "docs_none": {
        "uz": "Hali hech qanday hujjat yuborilmadi.",
        "ru": "Вы ещё не прислали ни одного документа.",
    },
    "docs_report_title": {"uz": "<b>📋 Tekshiruv natijasi</b>\n", "ru": "<b>📋 Результат проверки</b>\n"},
    "docs_all_ok": {
        "uz": "\n🎉 <b>Jiddiy xato topilmadi!</b> Hujjatlaringiz topshirishga tayyor ko'rinadi.",
        "ru": "\n🎉 <b>Серьёзных ошибок не найдено!</b> Документы выглядят готовыми к подаче.",
    },
    "docs_footer": {
        "uz": "\n\n🧹 <i>Sessiya ma'lumotlari o'chirildi.</i>\n<i>⚠️ Bu avtomatik tekshiruv, yakuniy qarorni soliq organi qabul qiladi.</i>",
        "ru": "\n\n🧹 <i>Данные сессии удалены.</i>\n<i>⚠️ Это автоматическая проверка, окончательное решение принимает налоговый орган.</i>",
    },

    # manual checklist
    "mq1": {
        "uz": "<b>1/6.</b> Shartnomada <b>to'lovchi</b> (buyurtmachi) sifatida deklaratsiya topshiradigan odam ko'rsatilganmi yoki o'qiyotgan shaxsning o'zimi?",
        "ru": "<b>1/6.</b> В договоре <b>плательщиком</b> (заказчиком) указан тот, кто будет подавать декларацию, или сам учащийся?",
    },
    "mq2": {
        "uz": "<b>2/6.</b> To'lovlar aynan deklaratsiya topshiradigan odamning <b>o'z kartasi yoki hisobidan</b> qilinganmi?",
        "ru": "<b>2/6.</b> Платежи сделаны именно <b>с карты или счёта</b> того, кто будет подавать декларацию?",
    },
    "mq3": {
        "uz": "<b>3/6.</b> Har bir to'lov uchun <b>chek yoki bank ko'chirmasi</b> bormi?",
        "ru": "<b>3/6.</b> На каждый платёж есть <b>чек или банковская выписка</b>?",
    },
    "mq4": {
        "uz": "<b>4/6.</b> Hamma to'lovlar <b>bitta kalendar yili</b> ichida qilinganmi (deklaratsiya yili)?",
        "ru": "<b>4/6.</b> Все платежи сделаны в <b>одном календарном году</b> (год декларации)?",
    },
    "mq5": {
        "uz": "<b>5/6.</b> Shartnomadagi va to'lovdagi <b>ism-familiya bir xil</b> yozilganmi (lotin/kirill farqi ham)?",
        "ru": "<b>5/6.</b> <b>ФИО в договоре и в платежах совпадают</b> (включая латиницу/кириллицу)?",
    },
    "mq6": {
        "uz": "<b>6/6.</b> Soliq ilovasiga <b>Face ID</b> yoki <b>ERI</b> orqali kira olasizmi?",
        "ru": "<b>6/6.</b> Можете войти в приложение Soliq через <b>Face ID</b> или <b>ЭЦП</b>?",
    },
    "mfix1": {
        "uz": "❗ Shartnomada to'lovchi boshqa odam. Ariza beruvchi bilan shartnomadagi to'lovchi mos bo'lishi kerak — OTMdan shartnomaga qo'shimcha kelishuv yoki ma'lumotnoma so'rang.",
        "ru": "❗ В договоре указан другой плательщик. Заявитель и плательщик по договору должны совпадать — попросите в вузе допсоглашение или справку.",
    },
    "mfix2": {
        "uz": "❗ To'lov boshqa odamning kartasidan qilingan. Bunday to'lovni odatda faqat karta egasi qaytarib oladi. Keyingi to'lovlarni o'z kartangizdan qiling.",
        "ru": "❗ Оплата с карты другого человека. Обычно вернуть налог за такой платёж может только владелец карты. Следующие платежи делайте со своей карты.",
    },
    "mfix3": {
        "uz": "❗ Chek yo'q. Bank ilovasidan to'lov tarixi (ko'chirma) yoki OTM buxgalteriyasidan to'lov haqida ma'lumotnoma oling.",
        "ru": "❗ Нет чеков. Возьмите выписку в банковском приложении или справку об оплате в бухгалтерии вуза.",
    },
    "mfix4": {
        "uz": "❗ To'lovlar turli yillarda. Har bir yil uchun alohida deklaratsiya topshiriladi — to'lovlarni yillar bo'yicha ajrating.",
        "ru": "❗ Платежи в разные годы. За каждый год подаётся отдельная декларация — разделите платежи по годам.",
    },
    "mfix5": {
        "uz": "❗ Ism-familiya farq qiladi. Pasportdagi yozuv bilan solishtiring va kerak bo'lsa OTMdan to'g'rilangan ma'lumotnoma oling.",
        "ru": "❗ ФИО отличается. Сверьте с паспортом и при необходимости возьмите в вузе справку с исправлением.",
    },
    "mfix6": {
        "uz": "❗ Kirish imkoni yo'q. Soliq ilovasida Face ID orqali ro'yxatdan o'tish mumkin yoki ERIni xizmat ko'rsatish markazida bepul olish mumkin.",
        "ru": "❗ Нет доступа. В приложении Soliq можно зарегистрироваться через Face ID, а ЭЦП можно бесплатно получить в центре госуслуг.",
    },
    "manual_ok": {
        "uz": "🎉 <b>Hammasi joyida!</b> Hujjatlaringiz tayyor ko'rinadi. Endi <b>🧭 Yo'riqnoma</b> bo'yicha topshiring yoki biz bilan birga.",
        "ru": "🎉 <b>Всё в порядке!</b> Документы выглядят готовыми. Теперь подавайте по <b>🧭 Инструкции</b> или вместе с нами.",
    },
    "manual_issues": {
        "uz": "<b>📋 Topilgan muammolar ({n}):</b>\n\n",
        "ru": "<b>📋 Найденные проблемы ({n}):</b>\n\n",
    },

    # ---------- guide ----------
    "guide_steps": {
        "uz": (
            "<b>🧭 1-qadam / 7. Tayyorgarlik</b>\n\nKerak bo'ladi:\n• Shartnoma (yoki ipoteka shartnomasi)\n• To'lov cheklari / bank ko'chirmasi\n• Bank kartangiz (pul shu kartaga tushadi)\n• Telefon va <b>Soliq</b> ilovasi yoki ERI\n\n💡 Hujjatlarni oldindan <b>📄 Hujjatlarni tekshirish</b> orqali tekshiring.",
            "<b>🧭 2-qadam / 7. Kirish</b>\n\n<b>Soliq</b> mobil ilovasini oching (yoki kompyuterda my3.soliq.uz).\nTelefonda — <b>Face ID</b> orqali, kompyuterda — <b>ERI</b> orqali kiring.\n\n🔐 Login va kodlarni <b>hech kimga</b> bermang — hatto bizga ham.",
            "<b>🧭 3-qadam / 7. Deklaratsiya</b>\n\nXizmatlar ichidan <b>«Jismoniy shaxslarning jami yillik daromadi to'g'risidagi deklaratsiya»</b>ni tanlang va xarajat qilingan <b>yilni</b> belgilang.",
            "<b>🧭 4-qadam / 7. Daromadlarni tekshirish</b>\n\nIsh joyingizdan olgan daromad va ushlangan soliq odatda <b>avtomatik</b> to'ldiriladi. Raqamlar to'g'riligini tekshiring.",
            "<b>🧭 5-qadam / 7. Imtiyozni tanlash</b>\n\n<b>«Soliq imtiyozlari»</b> bo'limida xarajat turini qo'shing.\n🎓 Ta'lim uchun — <b>Soliq kodeksining 378-moddasi 16.2-bandi</b>.\n🏫/🏠 Bog'cha, maktab yoki ipoteka uchun — ro'yxatdan mos imtiyozni nomi bo'yicha tanlang.\n\nSummani kiriting.",
            "<b>🧭 6-qadam / 7. Hujjatlarni yuklash</b>\n\nShartnoma va to'lov hujjatlarini yuklang, ma'lumotlarni yana bir bor tekshiring va <b>deklaratsiyani yuboring</b>.\n\nMuddat: hisobot yilidan keyingi yilning <b>1-apreligacha</b>.",
            "<b>🧭 7-qadam / 7. Pulni qaytarish arizasi</b>\n\nDeklaratsiya qabul qilingach, alohida <b>«Ortiqcha to'langan soliq summalarini qaytarish»</b> xizmati orqali ariza bering va karta/bank rekvizitlarini kiriting.\n\n💸 Pul ariza qabul qilingandan keyin <b>15 ish kuni</b> ichida tushadi.\n\n🤝 Qiynalsangiz — <b>Birga topshiramiz</b>!",
        ),
        "ru": (
            "<b>🧭 Шаг 1 / 7. Подготовка</b>\n\nПонадобится:\n• Договор (или договор ипотеки)\n• Чеки об оплате / банковская выписка\n• Ваша банковская карта (деньги придут на неё)\n• Телефон и приложение <b>Soliq</b> или ЭЦП\n\n💡 Заранее проверьте документы через <b>📄 Проверить документы</b>.",
            "<b>🧭 Шаг 2 / 7. Вход</b>\n\nОткройте мобильное приложение <b>Soliq</b> (или my3.soliq.uz на компьютере).\nНа телефоне входите через <b>Face ID</b>, на компьютере — через <b>ЭЦП</b>.\n\n🔐 Никому не сообщайте логины и коды — даже нам.",
            "<b>🧭 Шаг 3 / 7. Декларация</b>\n\nВ услугах выберите <b>«Декларация о совокупном годовом доходе физических лиц»</b> и укажите <b>год</b>, в котором были расходы.",
            "<b>🧭 Шаг 4 / 7. Проверка доходов</b>\n\nДоходы с работы и удержанный налог обычно подтягиваются <b>автоматически</b>. Проверьте, что цифры верные.",
            "<b>🧭 Шаг 5 / 7. Выбор льготы</b>\n\nВ разделе <b>«Налоговые льготы»</b> добавьте вид расхода.\n🎓 Для обучения — <b>п. 16.2 статьи 378 Налогового кодекса</b>.\n🏫/🏠 Для сада, школы или ипотеки — выберите подходящую льготу из списка по названию.\n\nВведите сумму.",
            "<b>🧭 Шаг 6 / 7. Загрузка документов</b>\n\nЗагрузите договор и платёжные документы, ещё раз проверьте данные и <b>отправьте декларацию</b>.\n\nСрок: до <b>1 апреля</b> года, следующего за отчётным.",
            "<b>🧭 Шаг 7 / 7. Заявление на возврат</b>\n\nКогда декларацию примут, подайте отдельное заявление через услугу <b>«Возврат излишне уплаченных сумм налогов»</b> и укажите реквизиты карты/банка.\n\n💸 Деньги приходят в течение <b>15 рабочих дней</b> после принятия заявления.\n\n🤝 Сложно? — <b>Подадим вместе</b>!",
        ),
    },
    "btn_prev": {"uz": "⬅️ Oldingi", "ru": "⬅️ Назад"},
    "btn_next": {"uz": "Keyingi ➡️", "ru": "Далее ➡️"},
    "guide_disclaimer": {
        "uz": "\n\n<i>ℹ️ Menyular nomi ilova yangilanishi bilan biroz o'zgarishi mumkin.</i>",
        "ru": "\n\n<i>ℹ️ Названия пунктов могут немного меняться после обновлений приложения.</i>",
    },

    # ---------- booking ----------
    "book_intro": {
        "uz": (
            "<b>🤝 Birga topshiramiz</b>\n\n"
            "Mutaxassisimiz siz bilan <b>uchrashuvda yoki video qo'ng'iroqda</b> hammasini birga qiladi: hujjatlarni "
            "tekshiradi, qayerga bosishni ko'rsatadi. Deklaratsiyani <b>siz o'zingiz, o'z telefoningizdan</b> yuborasiz — "
            "biz parol va kodlaringizni hech qachon so'ramaymiz.\n\n"
            "💰 <b>Narx:</b>\n"
            "• Bron: <b>{price} so'm</b> (umumiy to'lovdan chegiriladi)\n"
            "• Pul qaytgach: qaytgan summaning <b>{fee}%</b>\n"
            "• Pul qaytmasa — qo'shimcha to'lov yo'q 🙌\n\n"
            "Bron qilish uchun ism va telefon raqamingiz kerak bo'ladi."
        ),
        "ru": (
            "<b>🤝 Подаём вместе</b>\n\n"
            "Наш специалист <b>на встрече или по видеозвонку</b> сделает всё вместе с вами: проверит документы, покажет, "
            "куда нажимать. Декларацию вы отправляете <b>сами, со своего телефона</b> — мы никогда не просим пароли и коды.\n\n"
            "💰 <b>Стоимость:</b>\n"
            "• Бронь: <b>{price} сум</b> (засчитывается в общую оплату)\n"
            "• После возврата: <b>{fee}%</b> от вернувшейся суммы\n"
            "• Не вернули — больше ничего не платите 🙌\n\n"
            "Для брони понадобятся имя и номер телефона."
        ),
    },
    "btn_book_start": {"uz": "📝 Bron qilish", "ru": "📝 Забронировать"},
    "book_consent": {
        "uz": (
            "🔒 Bron uchun <b>ismingiz va telefon raqamingiz</b> faqat siz bilan bog'lanish maqsadida saqlanadi va "
            "xizmat ko'rsatilgandan so'ng 6 oy ichida o'chiriladi. Istalgan vaqtda <b>🔒 Maxfiylik</b> → o'chirish orqali o'chirishingiz mumkin.\n\n"
            "📄 <a href=\"{privacy}\">Maxfiylik siyosati</a> · <a href=\"{terms}\">Foydalanish shartlari</a>"
        ),
        "ru": (
            "🔒 Для брони ваши <b>имя и номер телефона</b> хранятся только для связи с вами и удаляются в течение "
            "6 месяцев после оказания услуги. Удалить их можно в любой момент: <b>🔒 Конфиденциальность</b> → удалить.\n\n"
            "📄 <a href=\"{privacy}\">Политика конфиденциальности</a> · <a href=\"{terms}\">Условия использования</a>"
        ),
    },
    "q_name": {"uz": "Ismingizni yozing:", "ru": "Как вас зовут?"},
    "q_phone": {
        "uz": "📱 Telefon raqamingizni yuboring (pastdagi tugma) yoki yozing:",
        "ru": "📱 Отправьте номер телефона (кнопка внизу) или напишите его:",
    },
    "btn_share_phone": {"uz": "📱 Raqamni yuborish", "ru": "📱 Отправить номер"},
    "bad_phone": {
        "uz": "Raqamni tushunmadim. Masalan: <code>+998901234567</code>",
        "ru": "Не понял номер. Например: <code>+998901234567</code>",
    },
    "q_format": {"uz": "Qanday qulay?", "ru": "Как удобнее?"},
    "fmt_offline": {"uz": "☕️ Uchrashuv (Toshkent)", "ru": "☕️ Встреча (Ташкент)"},
    "fmt_video": {"uz": "📹 Video qo'ng'iroq", "ru": "📹 Видеозвонок"},
    "book_done": {
        "uz": (
            "✅ <b>Bron №{id} qabul qilindi!</b>\n\n"
            "To'lov uchun: <code>{card}</code>\n{holder}\nSumma: <b>{price} so'm</b>\n\n"
            "To'lovdan so'ng <b>chek skrinshotini shu yerga yuboring</b> — biz tasdiqlab, siz bilan bog'lanamiz. "
            "Deklaratsiya mavsumi (yanvar–mart) boshlanishi bilan birinchi navbatda sizga yozamiz. 🚀"
        ),
        "ru": (
            "✅ <b>Бронь №{id} принята!</b>\n\n"
            "Для оплаты: <code>{card}</code>\n{holder}\nСумма: <b>{price} сум</b>\n\n"
            "После оплаты <b>пришлите сюда скриншот чека</b> — мы подтвердим и свяжемся с вами. "
            "Как только откроется сезон деклараций (январь–март), напишем вам в первую очередь. 🚀"
        ),
    },
    "receipt_received": {
        "uz": "🙏 Chek qabul qilindi va adminga yuborildi. Tasdiqlangach xabar beramiz.",
        "ru": "🙏 Чек получен и отправлен администратору. Сообщим, когда подтвердим.",
    },
    "booking_paid": {
        "uz": "🎉 <b>To'lovingiz tasdiqlandi!</b> Bron №{id} faol. Tez orada siz bilan bog'lanamiz.",
        "ru": "🎉 <b>Оплата подтверждена!</b> Бронь №{id} активна. Скоро свяжемся с вами.",
    },

    # ---------- articles ----------
    "articles_title": {"uz": "<b>📚 Maqolalar</b>\n\nMavzuni tanlang 👇", "ru": "<b>📚 Статьи</b>\n\nВыберите тему 👇"},
    "btn_back": {"uz": "⬅️ Orqaga", "ru": "⬅️ Назад"},

    # ---------- reminders ----------
    "remind_on": {
        "uz": "⏰ <b>Eslatmalar yoqildi!</b>\n\nDeklaratsiya mavsumi ochilganda (yanvar), muddat tugashiga 1 oy va 1 hafta qolganda xabar beraman.",
        "ru": "⏰ <b>Напоминания включены!</b>\n\nНапишу, когда откроется сезон деклараций (январь), а также за месяц и за неделю до дедлайна.",
    },
    "remind_off": {"uz": "🔕 Eslatmalar o'chirildi.", "ru": "🔕 Напоминания выключены."},
    "rem_jan": {
        "uz": "📣 <b>Deklaratsiya mavsumi ochildi!</b>\n\nO'tgan yildagi kontrakt, bog'cha/maktab va ipoteka to'lovlari uchun 12% ni qaytarish vaqti keldi. Muddat — <b>1-aprel</b>.\n\nBoshlash: /start",
        "ru": "📣 <b>Сезон деклараций открыт!</b>\n\nПора возвращать 12% за контракт, сад/школу и ипотеку прошлого года. Срок — <b>до 1 апреля</b>.\n\nНачать: /start",
    },
    "rem_month": {
        "uz": "⏳ <b>1-aprelgacha 1 oy qoldi!</b> Deklaratsiyani hali topshirmagan bo'lsangiz — hozir vaqti. /start",
        "ru": "⏳ <b>До 1 апреля остался месяц!</b> Если ещё не подали декларацию — самое время. /start",
    },
    "rem_week": {
        "uz": "🔥 <b>Oxirgi hafta!</b> 1-aprelgacha deklaratsiyani topshiring, aks holda bu yil uchun pul qaytmaydi. /start",
        "ru": "🔥 <b>Последняя неделя!</b> Подайте декларацию до 1 апреля, иначе за этот год деньги не вернутся. /start",
    },

    # ---------- privacy menu ----------
    "privacy_menu": {
        "uz": (
            "<b>🔒 Maxfiylik va xavfsizlik</b>\n\n"
            "✅ Hujjat rasmlari <b>saqlanmaydi</b> — faqat operativ xotirada tekshiriladi.\n"
            "✅ Bazada faqat: Telegram ID, til, hisob-kitob raqamlari, bron uchun ism va telefon.\n"
            "✅ Parol, ERI, SMS-kod, karta ma'lumotlarini <b>hech qachon so'ramaymiz</b>.\n"
            "✅ Ma'lumotlaringizni istalgan vaqtda o'chirishingiz mumkin.\n\n"
            "📄 <a href=\"{privacy}\">Maxfiylik siyosati</a> · <a href=\"{terms}\">Foydalanish shartlari</a>"
        ),
        "ru": (
            "<b>🔒 Конфиденциальность и безопасность</b>\n\n"
            "✅ Фото документов <b>не сохраняются</b> — проверяются только в оперативной памяти.\n"
            "✅ В базе только: Telegram ID, язык, цифры расчёта, имя и телефон для брони.\n"
            "✅ Мы <b>никогда не просим</b> пароли, ЭЦП, SMS-коды и данные карты.\n"
            "✅ Свои данные можно удалить в любой момент.\n\n"
            "📄 <a href=\"{privacy}\">Политика конфиденциальности</a> · <a href=\"{terms}\">Условия использования</a>"
        ),
    },
    "btn_delete_me": {"uz": "🗑 Ma'lumotlarimni o'chirish", "ru": "🗑 Удалить мои данные"},
    "confirm_delete": {
        "uz": "Barcha ma'lumotlaringiz (hisob-kitoblar, bronlar) o'chiriladi. Tasdiqlaysizmi?",
        "ru": "Все ваши данные (расчёты, брони) будут удалены. Подтверждаете?",
    },
    "deleted": {
        "uz": "🗑 Ma'lumotlaringiz o'chirildi. Qayta boshlash: /start",
        "ru": "🗑 Ваши данные удалены. Начать заново: /start",
    },
}

ARTICLES: list[dict[str, dict[str, str]]] = [
    {
        "title": {"uz": "💡 12% nima va kimga qaytariladi?", "ru": "💡 Что такое 12% и кому возвращают?"},
        "body": {
            "uz": (
                "<b>💡 12% nima va kimga qaytariladi?</b>\n\n"
                "O'zbekistonda maoshdan <b>12% daromad solig'i</b> ushlanadi. Agar siz shu daromad hisobidan ta'lim, "
                "xususiy bog'cha/maktab yoki ipoteka uchun to'lagan bo'lsangiz, davlat shu summaga to'g'ri keladigan soliqni qaytaradi.\n\n"
                "📐 Formula oddiy: <b>to'langan summa × 12%</b>.\n"
                "20 mln kontrakt → 2,4 mln; 25 mln → 3 mln so'm.\n\n"
                "Kimlar olishi mumkin:\n"
                "• O'zi uchun to'lagan rasmiy ishlaydigan talaba\n"
                "• 26 yoshgacha farzandi yoki turmush o'rtog'i uchun to'lagan ota-ona yoki er/xotin\n"
                "• Xususiy bog'cha va maktab uchun to'lagan ota-onalar\n"
                "• Ipoteka to'layotganlar\n\n"
                "Asosiy shart — to'lovchining rasmiy daromadi va undan ushlangan soliq bo'lishi."
            ),
            "ru": (
                "<b>💡 Что такое 12% и кому возвращают?</b>\n\n"
                "В Узбекистане с зарплаты удерживают <b>12% подоходного налога</b>. Если из этого дохода вы платили за "
                "обучение, частный сад/школу или ипотеку — государство возвращает налог с этой суммы.\n\n"
                "📐 Формула простая: <b>оплаченная сумма × 12%</b>.\n"
                "Контракт 20 млн → 2,4 млн; 25 млн → 3 млн сум.\n\n"
                "Кто может получить:\n"
                "• Официально работающий студент, который платит за себя\n"
                "• Родитель или супруг(а), платящие за ребёнка или супруга(у) до 26 лет\n"
                "• Родители, платящие за частный сад и школу\n"
                "• Те, кто платит ипотеку\n\n"
                "Главное условие — у плательщика есть официальный доход и удержанный с него налог."
            ),
        },
    },
    {
        "title": {"uz": "⚠️ Nega ko'pchilik ololmaydi: 5 ta xato", "ru": "⚠️ Почему многие не получают: 5 ошибок"},
        "body": {
            "uz": (
                "<b>⚠️ Nega ko'pchilik ololmaydi: 5 ta xato</b>\n\n"
                "1️⃣ <b>Boshqaning kartasidan to'lash.</b> Kontraktni bobo to'lagan, deklaratsiyani ota topshiryapti — mos kelmaydi.\n"
                "2️⃣ <b>Rasmiy daromad yo'q.</b> Soliq ushlanmagan bo'lsa, qaytariladigan ham yo'q.\n"
                "3️⃣ <b>Chek yo'q.</b> To'lovni hujjat bilan tasdiqlash kerak.\n"
                "4️⃣ <b>Muddatni o'tkazib yuborish.</b> Deklaratsiya keyingi yilning 1-apreligacha.\n"
                "5️⃣ <b>Ikkinchi arizani unutish.</b> Deklaratsiyadan keyin alohida «qaytarish» arizasi kerak — busiz pul kelmaydi.\n\n"
                "📄 Hujjatlaringizni bot orqali tekshiring — bu xatolarni oldindan topamiz."
            ),
            "ru": (
                "<b>⚠️ Почему многие не получают: 5 ошибок</b>\n\n"
                "1️⃣ <b>Оплата с чужой карты.</b> Контракт оплатил дедушка, а декларацию подаёт отец — не совпадает.\n"
                "2️⃣ <b>Нет официального дохода.</b> Если налог не удерживали — возвращать нечего.\n"
                "3️⃣ <b>Нет чеков.</b> Оплату нужно подтвердить документами.\n"
                "4️⃣ <b>Пропущенный срок.</b> Декларация — до 1 апреля следующего года.\n"
                "5️⃣ <b>Забытое второе заявление.</b> После декларации нужно отдельное заявление на возврат — без него деньги не придут.\n\n"
                "📄 Проверьте документы в боте — найдём эти ошибки заранее."
            ),
        },
    },
    {
        "title": {"uz": "🏫 Bog'cha va maktab uchun 12%", "ru": "🏫 12% за сад и школу"},
        "body": {
            "uz": (
                "<b>🏫 Xususiy bog'cha va maktab uchun 12%</b>\n\n"
                "2026-yildan boshlab nodavlat bog'cha va maktab to'lovlari uchun ham daromad solig'ini qaytarish mumkinligi haqida "
                "rasmiy tushuntirishlar e'lon qilindi.\n\n"
                "Masalan, oyiga 2 mln so'm × 12 oy = 24 mln → <b>2,88 mln so'm</b> qaytishi mumkin (soliq yetarli ushlangan bo'lsa).\n\n"
                "Kerak: muassasa bilan shartnoma, to'lov cheklari, to'lovchining rasmiy daromadi.\n\n"
                "<i>Aniq shartlarni my3.soliq.uz yoki Soliq ilovasida tekshiring.</i>"
            ),
            "ru": (
                "<b>🏫 12% за частный сад и школу</b>\n\n"
                "С 2026 года опубликованы официальные разъяснения: подоходный налог можно вернуть и за оплату "
                "негосударственных садов и школ.\n\n"
                "Например: 2 млн сум в месяц × 12 = 24 млн → может вернуться <b>2,88 млн сум</b> (если удержано достаточно налога).\n\n"
                "Нужно: договор с учреждением, чеки об оплате, официальный доход плательщика.\n\n"
                "<i>Точные условия проверяйте на my3.soliq.uz или в приложении Soliq.</i>"
            ),
        },
    },
    {
        "title": {"uz": "🏠 Ipoteka bo'yicha 12%", "ru": "🏠 12% по ипотеке"},
        "body": {
            "uz": (
                "<b>🏠 Ipoteka bo'yicha 12%</b>\n\n"
                "Ipoteka krediti bo'yicha to'lovlar ham imtiyozga kiradi. Har yili to'lagan summangizdan 12% qaytishi mumkin — "
                "bu ko'pincha <b>yiliga millionlab so'm</b>.\n\n"
                "Kerak: ipoteka shartnomasi, bankdan yil davomida to'langan summa haqida ma'lumotnoma, rasmiy daromad.\n\n"
                "💡 Bank ilovasida yoki filialida «yil davomida to'langan summalar haqida ma'lumotnoma» so'rang."
            ),
            "ru": (
                "<b>🏠 12% по ипотеке</b>\n\n"
                "Платежи по ипотечному кредиту тоже дают право на льготу. Каждый год можно вернуть 12% от выплаченного — "
                "часто это <b>миллионы сумов в год</b>.\n\n"
                "Нужно: договор ипотеки, справка из банка о суммах, выплаченных за год, официальный доход.\n\n"
                "💡 Попросите в приложении или отделении банка «справку о выплаченных за год суммах»."
            ),
        },
    },
    {
        "title": {"uz": "📅 Muddatlar va pul qachon tushadi", "ru": "📅 Сроки и когда придут деньги"},
        "body": {
            "uz": (
                "<b>📅 Muddatlar</b>\n\n"
                "• Deklaratsiya: xarajat qilingan yildan keyingi yilning <b>1-apreligacha</b>.\n"
                "  Masalan, 2026-yil to'lovlari uchun — 2027-yil 1-aprelgacha.\n"
                "• Keyin alohida <b>qaytarish arizasi</b> beriladi.\n"
                "• Pul ariza qabul qilingandan keyin <b>15 ish kuni</b> ichida kartaga tushadi.\n\n"
                "⏰ Muddatni unutmaslik uchun botda <b>Eslatmalar</b>ni yoqing."
            ),
            "ru": (
                "<b>📅 Сроки</b>\n\n"
                "• Декларация: до <b>1 апреля</b> года, следующего за годом расходов.\n"
                "  Например, за платежи 2026 года — до 1 апреля 2027 года.\n"
                "• Затем подаётся отдельное <b>заявление на возврат</b>.\n"
                "• Деньги приходят на карту в течение <b>15 рабочих дней</b> после принятия заявления.\n\n"
                "⏰ Чтобы не пропустить срок, включите в боте <b>Напоминания</b>."
            ),
        },
    },
    {
        "title": {"uz": "🛡 Firibgarlardan ehtiyot bo'ling", "ru": "🛡 Осторожно, мошенники"},
        "body": {
            "uz": (
                "<b>🛡 Firibgarlardan ehtiyot bo'ling</b>\n\n"
                "«12% ni qaytarib beramiz» deb yozadigan firibgarlar ko'p. Eslab qoling:\n\n"
                "❌ Hech kimga Soliq/my.gov.uz <b>login, parol, ERI</b> bermang\n"
                "❌ <b>SMS-kod</b>ni hech kimga aytmang\n"
                "❌ Kartangiz <b>CVV</b> va amal qilish muddatini yubormang\n"
                "❌ Noma'lum ilova yoki <b>.apk</b> fayllarni o'rnatmang\n\n"
                "✅ Qaytarish xizmatining o'zi davlat tomonidan <b>bepul</b>. Qaytar faqat yordam beradi — "
                "deklaratsiyani doim <b>siz o'zingiz</b> yuborasiz."
            ),
            "ru": (
                "<b>🛡 Осторожно, мошенники</b>\n\n"
                "Мошенников, которые пишут «вернём ваши 12%», много. Запомните:\n\n"
                "❌ Никому не давайте <b>логин, пароль, ЭЦП</b> от Soliq/my.gov.uz\n"
                "❌ Никому не сообщайте <b>SMS-коды</b>\n"
                "❌ Не отправляйте <b>CVV</b> и срок действия карты\n"
                "❌ Не устанавливайте неизвестные приложения и <b>.apk</b>-файлы\n\n"
                "✅ Сама услуга возврата у государства <b>бесплатная</b>. Qaytar только помогает — "
                "декларацию всегда отправляете <b>вы сами</b>."
            ),
        },
    },
]


def t(key: str, lang: str, **kwargs) -> str:
    value = T[key].get(lang) or T[key]["uz"]
    return value.format(**kwargs) if kwargs else value
