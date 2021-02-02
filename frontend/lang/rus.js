export default context => {
  const locale = {
    auth: {
      activation: 'Активация',
      activation_success: 'Вы успешно подтвердили email!',
      activation_failed: 'Ошибка: неверный email/код или email уже подтвержден',
      password: 'пароль',
      pin_code: 'Пин-код',
      sign_in: 'Войти',
      forgot_pw: 'Забыли пароль?',
      submit: 'Отправить',
      registration: 'Регистрация',
      first_name: 'Имя',
      last_name: 'Фамилия',
      partner_id: 'Партнерский код',
      repeat_password: 'Повторите пароль',
      i_accept: 'Я принимаю',
      terms_of_agreement: 'условия соглашения',
      sign_up: 'Зарегистрироваться',
      sign_up_success: 'Вы зарегистрировались! Пожалуйста проверьте ваш email чтобы активировать аккаунт!',
      sign_up_error_referral: 'Для регистрации в системе необходим Партнерский код. Если у вас нет кода, пожалуйста, запросите в',
      to_support: 'службе поддержки',
      recover_success: 'Успешно! Проверьте ваш email для дальнейших инструкций.',
      recover_error: 'Ошибка: убедитесь что email введет верно',
      login_failed: 'Проверьте введенные email/пароль, возможно ваш email не подтвержден',
      login_failed_pin: 'Проверьте введенные email/пароль и пинкод',
    },
    footer: {
      tos: "Условия использования",
      privacy: "Политики конфиденциальности",
      cookies: "Политика cookies"
    },
    header_menu: {
      exchange: "Обмен",
      about: "О нас",
      howtouse: "Как использовать",
      transparency: "Прозрачность",
      wallet: "Кошелек",
      contacts: "Контакты"
    },
    exchange: {
      buy: "Покупка",
      sell: "Продажа",
      last_bills: "Последние сделки",
      empty_bills: "Список сделок пуст",
      more_bills: "Больше",
      confirm_wallet: "Подтверждение кошелька",
      confirm: "Подтвердить",
      cr_payment_bill: "Создать сделку",
      create: "Создать",
      amount_err: "Минимальная сумма сделки ",
      bill_payment: "Оплата сделки",
      send: "Отправьте",
      receive: "Получите",
      verify_auto: "Мы проверяем платеж автоматически.",
      verify_asap:
        "Как только оплата будет произведена, вы перейдете на следущий шаг сделки.",
      success: "Успех!",
      issued: "отправлено",
      wallet: "Кошелек",
      buy_more: "Купить еще",
      sell_more: "Продать еще",
      status: 'Статус',
      sent_payment: 'Платеж отправлен',
      choose_btc_wallet: {p1: 'Выберите BTC кошелек', p2: 'для вывода'},
      choose_eth_wallet: {p1: 'Выберите ETH кошелек', p2: 'для продажи SIMBA'},
      choose_btc_wallet_error: 'Пожалуйста выберите BTC кошелек',
      received_payment: 'Получен платеж',
      transaction_hash: 'Хеш транзакции',
      confirms: 'Подтверждений',
      payment_confirmation_buy: 'Как только сеть получит 3 подтверждения, токены SIMBA будут отправлены на ваш ETH адрес.',
      payment_confirmation_sell: 'Как только сеть получит {min_confirms} подтверждение(-я), BTC будут отправлены на ваш адрес.',
      statuses: {
        completed: 'Завершена',
        paid: 'Оплачена',
        created: 'Создана',
        waiting: 'В ожидании',
        cancelled: 'Отменена',
        expired: 'Просрочена',
        processing: 'В обработке'
      },
      error_creating_invoice: 'Произошла ошибка при создании инвойса',
      error_updating_invoice: 'Произошла ошибка при обновлении инвойса',
      error_confirming_invoice: 'Произошла ошибка при подтверждении инвойса',
      bill_expired: 'Сделка просрочена',
      time_is_out: 'Время вышло',
      time_is_limited: 'Время на каждую сделку ограничено 2 часами.',
      simba_redemption: 'Вывод Simba',
      send_simba_now: 'Отправить SIMBA сейчас',
      applied_fee: 'Комиссия',
      fee_in_simba: '(взымается в SIMBA)'
    },
    dropdown: {
      bill_details: "Реквизиты",
      personal_data: "Мои данные",
      security: "Безопасность",
      partner_program: 'Партнер. программа',
      logout: "Выход"
    },
    socials: {
      facebook: "https://www.facebook.com/simbastorageRU",
      bitcoin: "https://bitcointalk.org/index.php?topic=5260056.msg54734523#msg54734523",
      instagram: "https://www.instagram.com/simbastorageRU",
      medium: "https://medium.com/@simbastorage",
      zen: "https://zen.yandex.ru/simba",
      reddit: "https://www.reddit.com/r/simba_official/",
      twitter: "https://twitter.com/SWISSSST",
      vk: "https://vk.com/simbastorage",
      telegram: "https://t.me/simbastorage",
      telegram_chat: "https://t.me/simbastorage_ru",
      discord: "https://discord.com/channels/SimbaStorage#6018",
      streemit: "https://steemit.com/@simbastorage",
      github: "#",
      linkedin: "https://www.linkedin.com/company/simbastorage/"
    },
    profile: {
      sidebar: {
        personal: "Профиль",
        data: "Данные",
        verification: "Верификация",
        payment: "Платежи",
        bill_details: "Реквизиты",
        partner_program: "Партнер. программа",
        security: "Безопасность",
        change_password: "Изменить пароль",
        two_factor: "Двухфакт. аутентификация",
        logout: "Выход"
      },
      edit_my_profile: "Изменить мои данные",
      identity: "Верификация",
      email_verified: "Email подтвержден",
      email_unverified: "Email не подтверджен",
      email_verification: "Подтверждение email",
      verify_address: "Подтверждение адреса",
      id_verification: "Подтверждение паспорта",
      source_of_funds_verification: "Подтверждение источника средств",
      scan_qr_code: 'Отсканируйте этот QR код',
      after_scan_hit_enable: 'После сканирования QR кода, введите пин-код ниже и нажмите "Включить"',
      pin_code: 'Пин-код',
      btc_address_list: 'Список BTC адресов',
      eth_address_list: 'Список ETH адресов',
      for_withdraw_btc: 'для вывода Bitcoin при погашении SIMBA',
      for_issue_simba: 'для получения SIMBA',
    },
    messages: {
      two_factor_enable_failed: 'Не удалось включить двухфакторную аутентификацию!',
      two_factor_enable_success: 'Двухфакторная аутентификая включена!',
      two_factor_disable_failed: 'Не удалось отключить двухфакторную аутентификацию!',
      two_factor_disable_success: 'Двухфакторная аутентификая отключена!',
    },
    partner: {
      main:
        "Получайте токены за каждый депозит пользователей приглашенных по вашей " +
        "<a href='#' id='text-ref-link' class='link' rel='noreferrer noopener' target='_blank'>ссылке</a>. Как это работает?<br><br>" +
        "1. Вы копируете ссылку и отправляете вашему другу.<br>" +
        "2. Регистрируясь по вашей ссылке он будет привязан к вашему аккаунту.<br>" +
        "3. При каждом пополнении вы получите токены SST, которые сможете продать на бирже по актуальному курсу.<br>" +
        "4. Когда ваши друзья будут приглашать своих, вы будете получать дополнительный бонус.<br>" +
        "Так за 5 уровней вы получите: 5%, 1%, 1%, 0.5% и 0.5%.<br>" +
        "Предложение ограничено количеством предоставленных SST токенов.",
      invited: "Приглашенные пользователи",
      your_ref_link: "Ваша партнерская ссылка",
      your_ref_code: "Ваш партнерский код",
      your_reward_address: 'Ваш ETH адрес для вознаграждений',
      refs_empty: "У вас еще нет приглашенных пользователей",
      how_to_get_code: {
        p1: "Чтобы принять участие в партнерской программе, ",
        p2: "добавьте",
        p3: "Ethereum адрес"
      },
    },
    password: {
      current: "Текущий пароль",
      new: "Новый пароль",
      confirm: "Подтверждение пароля",
      change_success: "Пароль успешно изменен!",
      change_error: "Не удалось изменить пароль!"
    },
    transparency: {
      curr_balances: "Текущие балансы"
    },
    wallet: {
      transfer_simba: "Перевод SIMBA токенов",
      your_wallet: "Ваш кошелек",
      recipient: "Получатель",
      add_wallet: "добавить",
      txs_history: "История транзакций",
      delete_wallet: "удалить",
      delete_sure: "Вы уверены что хотите удалить этот адрес",
      txs_history_empty: "История транзакций пуста",
      transaction_failed: 'Ошибка: транзацкия не удалась',
      transaction_success: 'Транзакция проведена успешно!',
      pin_code: 'Пин-код',
      add_new_wallet: {p1: 'Добавить новый', p2: 'кошелек'},
      address_deleted: 'Адрес успешно удален!',
      address_added: 'Адрес успешно добавлен!',
      address_failed_with_pin: 'Ошибка при добавлении адреса, убедитесь что адрес и пин-код введены верно!',
      address_failed_to_add: 'Ошибка: убедитесь что адрес введен корректно, возможно данный адрес уже существует',
      failed_to_get_signature: 'Не удалось получить подпись!',
      new_eth_wallet_instruct: {
        text1: 'Для добавления нового адреса, нажмите кнопку "Добавить"',
        text2: 'Если вы делаете это в первый раз, пожалуйста установите расширение {metamask}',
        text3: 'Для мобильных устройств мы рекомендуем {metamask} или приложение {imtoken}'
      },
      eth_wallet_switch_info: 'чтобы изменить адрес измените его в вашем кошельке',
      new_btc_wallet_instruct: {
        text1: 'Добавляя BTC-адрес вашего кошелька, вы подтверждаете что ввели правильный адрес',
        text2: 'За полную и безвозвратную потерю средств при выводе на эти адреса вы берете ответственность на себя.'
      },
      security_verification: 'Подтверждение',
      confirm_verification: 'Для завершения, пройдите подтверждение вводом пин-кода',
      address_exist: 'Данный адрес уже существует в вашем списке!'
    },
    other: {
      confirm: 'Подтвердить',
      try_again: 'Попробовать еще раз',
      add: 'Добавить',
      date: "Дата",
      fee: "Комиссия",
      total: "Итого",
      send: "Отправить",
      address: "Адрес",
      type: "Тип",
      amount: "Кол.-во",
      more: "больше",
      sent: "Отправлено",
      name: "Имя",
      delete: "Удалить",
      cancel: "Отмена",
      level: "Уровень",
      reg_date: "Дата регистрации",
      change: "Изменить",
      enable: "Включить",
      disable: "Отключить",
      first_name: 'Имя',
      last_name: 'Фамилия',
      save: 'Сохранить',
      copied_to_clipboard: 'Скопировано в буфер обмена',
      search: 'Поиск',
      search_empty_results: 'Нет результатов'
    },
    about: {
      company_goal: "Цель компании",
      goal:
        "Название SIMBA отражает силу, мощь, честность и дружелюбие по отношению к миру, в котором мы строим этот бизнес. Мы объединили опыт профессионалов в блокчейн и криптоиндустрии с 3-5 летним стажем. <br />Simba стремится быть самой удобной и надежной платформой для хранения биткойнов. Наше решение привносит преимущества в области безопасности, удобства и эффективности при длительном хранении криптоактивов. Храните свои деньги в защищённом хранилище институционального уровня с простым интерфейсом и высоким уровнем конфиденциальности.",
      date_of_establishment: "Дата создания",
      establishment: "Проект SIMBA основан в октябре 2019",
      сompany_locations: "Расположение компании",
      locations:
        "К концу 2020 г. география SIMBA в 5 странах: Швейцария, Лихтенштейн, ОАЭ, Эстония и Новая Зеландия.",
      our_mission: "Наша миссия",
      mission:
        "Общая задача нашей команды заключается в том, чтобы предоставить лучший сервис для поклонников и сторонников блокчейн индустрии и криптовалют. Каждый из нас по-разному прошел этот тернистый путь развития в новой и высокотехнологичной индустрии. Нас объединила общая вера в то, что мы в силах явить миру уникальный продукт, который будет служить людям. И поэтому мы создали его таким надежным, прозрачным и удобным, что каждый пользователь сможет гордиться, говоря «я храню свои биткоины в хранилище SIMBA». Для вас холодное хранилище SIMBA - это безопасность и спокойствие за будущее. Наша миссия - поддерживать эти характеристики на высочайшем уровне и расти, покоряя новые вершины."
    },
    account_page: {
      _id: 'ID',
      email: 'Email',
      email_is_active: 'Email подтвержден',
      verification_code: 'Код подтверждения',
      recover_code: 'Код восстановления',
      secret_2fa: 'Секретный ключ 2FA',
      two_factor: '2FA включена',
      first_name: 'Имя',
      last_name: 'Фамилия',
      user_btc_addresses: 'Список адресов Bitcoin',
      user_eth_addresses: 'Список адресов Ethereum',
      btc_address: 'BTC address',
      is_staff: 'Сотрудник',
      is_superuser: 'Суперпользователь',
      is_active: 'Активен',
      terms_and_condition: 'Принял условия и положения',
      created_at: 'Дата регистрации',
      list_is_empty: 'Список пуст',
      yes: 'Да',
      no: 'Нет',
      not_available: 'Н/Д',
      account_info: 'Учетная запись',
      account_changed_success: 'Данные учетной записи успешно изменены!',
      account_changed_error: 'Не удалось изменить данные учетной записи!',
      deleted_addresses: 'Архивные адреса (удаленные)',
      two_factor_modal: {
        step1: {
          title: '1. Установите OTP приложение (мы рекомендуем {link}).',
          subtitle: 'Используйте приложение на своем мобильном телефоне для получения одноразовых проверочных кодов, даже если ваш телефон в оффлайне. Доступно на Android, iPhone и Windows Phone.'
        },
        step2: {
          title: '2. Внимание!',
          subtitle: 'Код на 3-ем шаге должен быть сохранен для восстановления доступа к вашей личной учетной записи, если вы потеряете доступ к устройству или приложению которое генерирует одноразовые пароли.'
        },
        step3: {
          title: '3. Отсканируйте QR код',
          subtitle: 'Если вы не можете отсканировать QR-код, введите этот код вручную в приложение.'
        },
        attention: 'КОД ВОССТАНОВЛЕНИЯ. ПОЖАЛУЙСТА ЗАПИШИТЕ ЕГО.',
        step4: {
          title: '4. Введите код сгенерированный в вашем OTP приложении'
        },
        six_digit_code: '6-значный код'
      },
      enabled_2fa: 'Включена 2FA'
    },
    su_invoices: {
      invoices: 'Сделки',
      invoice: 'Сделка',
      user_id: "ID пользователя",
      status: "Статус",
      invoice_type: "Операция",
      btc_amount: "Сумма BTC",
      simba_amount: "Сумма SIMBA",
      btc_amount_proceeded: "Сумма обработанных BTC",
      simba_amount_proceeded: "Сумма обработанных SIMBA",
      target_eth_address: "Целевой ETH адрес",
      target_btc_address: "Целевой BTC адрес",
      eth_tx_hashes: "Хеши транзакций ETH",
      btc_tx_hashes: "Хеши транзакций BTC",
      created_at: "Дата создания",
      finised_at: "Дата заверщения",
      _id: "ID",
      eth_txs: "ETH транзакции",
      btc_txs: "BTC транзакции",
      not_available: "Н/Д",
      not_completed: "Незавершенные",
      empty: "Отсутствует(-ют)",
      sst_tx_hashes: 'Хеши SST транзакций',
      sst_tx_detailed: 'SST транзакции (подробно)',
      sst_tx_table: {
        show: 'Показать',
        hide: 'Скрыть',
        transactionHash: 'Хеш',
        amount: 'Вознаграждение',
        user_id: 'ID пользователя',
        level: 'Уровень'
      },
      invoice_type_1: "Покупка",
      invoice_type_2: "Продажа"
    },
    xpub: {
      confirm_your_action: 'Подтвердите ваше действие',
      confirm_change_status: 'Вы уверены что хотите изменить статус?',
      something_went_wrong: 'Что-то пошло не так!',
      status_changed: 'Статус успешно изменен!',
      status_active: 'Активен',
      status_inactive: 'Неактивен',
    },
    su_users: {
      users: 'Пользователи'
    },
    su_payouts_mm: {
      manage_payouts: {
        full: 'Управление выплатами',
        short: 'Управл. выплатами'
      },
      date: "Дата",
      transactions: "Транзакции",
      payout: "Выплата",
      actions: "Действия",
      target_address: "Адрес для выплаты",
      pay: "Оплатить",
      cancel: "Отменить",
      confirm_cancel_msg: "Вы действительно хотите отменить эту сделку?",
      confirm_pay_msg: "Вы действительно хотите произвести оплату по этой сделке?",
      status: "Ручной режим",
      enabled: "Включен",
      disabled: "Выключен",
      change_status: "Изменить статус",
      processing_only: "Только со статусом \"В обработке\"",
      refresh: "Обновить"
    }
  };

  return new Promise(function (resolve) {
    resolve(locale);
  });
};
