export default context => {
  const locale = {
    auth: {
      password: 'пароль',
      pin_code: 'пин код',
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
      recover_error: 'Ошибка: убедитесь что email введет верно'
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
      transparency: "Прозначность",
      wallet: "Кошелек",
      contacts: "Контакты"
    },
    exchange: {
      buy: "Купить",
      sell: "Продать",
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
      verify_auto: "Платежи подтверждаются автоматически.",
      verify_asap:
        "Как только оплата будет произведена, вы перейдете на следущий шаг сделки.",
      success: "Успех!",
      issued: "отправлено",
      wallet: "Кошелек",
      buy_more: "Купить еще"
    },
    dropdown: {
      bill_details: "Реквизиты",
      personal_data: "Мои данные",
      security: "Безопасность",
      logout: "Выход"
    },
    socials: {
      facebook: "https://www.facebook.com/simbastorageRU",
      bitcoin: "https://bitcointalk.org/index.php?action=profile;u=2816745",
      instagram: "https://www.instagram.com/simbastorageRU",
      medium: "https://medium.com/@simbastorage",
      zen: "https://zen.yandex.ru/simba",
      reddit: "https://www.reddit.com/r/simbastorage",
      twitter: "https://twitter.com/SWISSSST",
      vk: "https://vk.com/simbastorage",
      telegram: "https://t.me/simbastorage",
      telegram_chat: "https://t.me/simbastablecoin_ru",
      discord: "https://discord.com/channels/SimbaStorage#6018",
      streemit: "https://steemit.com/@simbastorage",
      github: "#",
      linkedin: "http://www.linkedin.cn/company/simbastorage"
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
        "4. Когда ваши друзья будут приглашать своих, вы будете получать дополнительный бонус. Так за 5 уровней вы получите: 5%, 1%, 1%, 0.5% и 0.5%.<br><br>" +
        "Предложение ограничено количеством предоставленных SST токенов.",
      invited: "Приглашенные пользователи",
      your_ref_link: "Ваша партнерская ссылка",
      your_ref_code: "Ваш партнерский код",
      refs_empty: "У вас еще нет приглашенных пользователей",
      how_to_get_code: {p1: "Чтобы принять участие в партнерской программе, ", p2: "добавьте", p3:"Ethereum адрес"},
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
      txs_history_empty: "История транзакций пуста"
    },
    other: {
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
      save: 'Сохранить'
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
        "Общая задача нашей команды заключается в том, чтобы предоставить лучший сервис для поклонников и сторонников блокчейн индустрии и криптовалют. Каждый из нас по-разному прошел этот тернистый путь развития в новой и высокотехнологичной индустрии. Нас объединила общая вера в то, что мы в силах явить миру уникальный продукт, который будет служить людям. И поэтому мы создали его таким надежным, прозрачным и удобным, что каждый пользователь сможет гордиться, говоря «я храню свои биткоины в хранилище SIMBA». Для вас холодное хранилище SIMBA - это безопасность и спокойствие за будущее. Наша миссия - поддерживать эти характеристике на высочайшем уровне и расти, покоряя новые вершины."
    }
  };

  return new Promise(function(resolve) {
    resolve(locale);
  });
};
