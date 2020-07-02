export default (context) => {
  const locale = {
    footer: {
      tos: 'Условия использования', privacy: 'Политики конфиденциальности', cookies: 'Политика cookies'
    },
    header_menu: {
      exchange: 'Обмен', about: 'О нас', howtouse: 'Как использовать', transparency: 'Прозначность',
      wallet: 'Кошелек', contacts: 'Контакты'
    },
    exchange: {
      buy: 'Купить', sell: 'Продать',
      last_bills: 'Последние сделки', empty_bills: 'Список сделок пуст', more_bills: 'Больше',
      confirm_wallet: 'Подтверждение кошелька', confirm: 'Подтвердить',
      cr_payment_bill: 'Создать сделку', create: 'Создать', amount_err: 'Минимальная сумма сделки ',
      bill_payment: 'Оплата сделки', send: 'Отправьте', receive: 'Получите',
      verify_auto: 'Платежи подтверждаются автоматически.',
      verify_asap: 'Как только оплата будет произведена, вы перейдете на следущий шаг сделки.',
      success: 'Успех!', issued: 'отправлено', wallet: 'Кошелек', buy_more: 'Купить еще'
    },
    dropdown: {
      bill_details: 'Реквизиты', personal_data: 'Мои данные', security: 'Безопасность', logout: 'Выход'
    },
    socials: {
      facebook: 'https://www.facebook.com/simbastorageRU', bitcoin: 'https://bitcointalk.org/index.php?action=profile;u=2816745',
      instagram: 'https://www.instagram.com/simbastorageRU', medium: 'https://medium.com/@simbastorage', zen: 'https://zen.yandex.ru/simba',
      reddit: 'https://www.reddit.com/r/simbastorage', twitter: 'https://twitter.com/SWISSSST', vk: 'https://vk.com/simbastorage',
      telegram: 'https://t.me/simbastorage', telegram_chat: 'https://t.me/simbastablecoin_ru',
      discord: 'https://discord.com/channels/SimbaStorage#6018',
      streemit: 'https://steemit.com/@simbastorage', github: '#', linkedin: 'http://www.linkedin.cn/company/simbastorage'
    },
    profile: {
      sidebar: {
        personal: 'Профиль', data: 'Данные', verification: 'Верификация', payment: 'Платежи',
        bill_details: 'Реквизиты', partner_program: 'Партнер. программа', security: 'Безопасность',
        change_password: 'Изменить пароль', two_factor: 'Двухфакт. авторизация', logout: 'Выход'
      }
    },
    partner: {
      main: "Получайте токены за каждый депозит пользователей приглашенных по вашей ссылке. Как это работает?<br><br>" +
        "1. Вы копируете ссылку и отправляете вашему другу.<br>" +
        "2. Регистрируясь по вашей ссылке он будет привязан к вашему аккаунту.<br>" +
        "3. При каждом пополнении вы получите токены SST, которые сможете продать на бирже по актуальному курсу.<br>" +
        "4. Когда ваши друзья будут приглашать своих, вы будете получать дополнительный бонус. Так за 5 уровней вы получите: 5%, 1%, 1%, 0.5% и 0.5%.<br><br>" +
        "Предложение ограничено количеством предоставленных SST токенов."
    }
  }

  return new Promise(function (resolve) {
    resolve(locale)
  });
}
