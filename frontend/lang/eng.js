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
      bill_details: 'Bill details', personal_data: 'Personal data', security: 'Security Settings', logout: 'Log out'
    },
    socials: {
      facebook: 'https://www.facebook.com/simbastorage', bitcoin: 'https://bitcointalk.org/index.php?action=profile;u=2816745',
      instagram: 'https://www.instagram.com/simbastorage/', medium: 'https://medium.com/@simbastorage', zen: 'https://zen.yandex.ru/simba',
      reddit: 'https://www.reddit.com/r/simbastorage', twitter: 'https://twitter.com/SWISSSST', vk: 'https://vk.com/simbastorage',
      telegram: 'https://t.me/simbastorage', telegram_chat: 'https://t.me/simbastorage_en',
      discord: 'https://discord.com/channels/SimbaStorage#6018',
      streemit: 'https://steemit.com/@simbastorage', github: '#', linkedin: 'http://www.linkedin.cn/company/simbastorage'
    },
    profile: {
      sidebar: {
        personal: 'Personal', data: 'Data', verification: 'Verification', payment: 'Payment',
        bill_details: 'Bill details', partner_program: 'Partner program', security: 'Security',
        change_password: 'Change password', two_factor: 'Two-Factor Auth', logout: 'Logout'
      },
      edit_my_profile: 'Edit my profile',
      identity: 'Identify verification', email_verified: 'Email verified',
      email_verification: 'Email verification', verify_address: 'Verify address',
      id_verification: 'ID verification', source_of_funds_verification: 'Source of funds verification'
    },
    partner: {
      main: "Get tokens for each deposit of users invited via your link. " +
        "How it works?<br><br>" +
        "1. You copy the link and send it to your friend.<br>" +
        "2. After sign up with your link, it will be tied to your account.<br>" +
        "3. With each recharge, you will receive SST tokens that you can sell" +
        "on the exchange at the current rate. The offer is limited by amount of provided SST tokens.",
      invited: 'Invited',  your_ref_link: 'Your referral link',
      your_ref_code: 'Your referral code', refs_empty: 'You don\'t have invited users yet'
    },
    password: {
      current: 'Current password', new: 'New password', confirm: 'Password confirmation'
    },
    transparency: {
      curr_balances: 'Current balances'
    },
    wallet: {
      transfer_simba: 'Transfer SIMBA tokens', your_wallet: 'Your wallet', recipient: 'Recipient',add_wallet: 'add new',
      txs_history: 'History of transactions', delete_wallet: 'delete',
      delete_sure: 'Are you sure you want to delete this address', txs_history_empty: 'Your transaction history is empty.'
    },
    other: {
      date: 'Date', fee: 'Fee', total: 'Total', send: 'Send', address: 'Address', type: 'Type', amount: 'Amount',
      more: 'more', sent: 'Sent', name: 'Name', delete: 'Delete', cancel: 'Cancel', level: 'Level',
      reg_date: 'Registration date', change: 'Change', enable: 'Enable', disable: 'Disable'
    }
  }

  return new Promise(function (resolve) {
    resolve(locale)
  });
}
