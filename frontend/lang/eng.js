export default (context) => {
  const locale = {
    footer: {
      tos: 'Terms of Use', privacy: 'Privacy Policy', cookies: 'Cookies Policy'
    },
    header_menu: {
      exchange: 'Exchange', about: 'About', howtouse: 'How to use', transparency: 'Transparency',
      wallet: 'Wallet', contacts: 'Contacts'
    },
    exchange: {
      buy: 'Buy', sell: 'Sell',
      last_bills: 'Last bills', empty_bills: 'Your bills list is empty', more_bills: 'More',
      confirm_wallet: 'Confirm wallet', confirm: 'Confirm',
      cr_payment_bill: 'Create payment bill', create: 'Create', amount_err: 'Minimum amount ',
      bill_payment: 'Bill payment', send: 'Send', receive: 'Receive',
      verify_auto: 'We verify payment automatically.',
      verify_asap: 'As soon as payment is made, the status of this state will change to another.',
      success: 'Success!', issued: 'issued', wallet: 'Wallet', buy_more: 'Buy more'
    },
    dropdown: {
      bill_details: 'Bill details', personal_data: 'Personal data', security: 'Security', logout: 'Logout'
    }
  }

  return new Promise(function (resolve) {
    resolve(locale)
  });
}
