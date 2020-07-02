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
      bill_details: 'Платежные данные', personal_data: 'Данные профиля', security: 'Безопасность', logout: 'Выход'
    }
  }

  return new Promise(function (resolve) {
    resolve(locale)
  });
}
