export default context => {
  const locale = {
    auth: {
      activation: 'Activation',
      activation_success: 'You successfully verified your email!',
      activation_failed: 'Error: invalid email/code or email is already verified',
      password: 'password',
      pin_code: 'Pin code',
      sign_in: 'Sign in',
      forgot_pw: 'Forgot password?',
      submit: 'Submit',
      registration: 'Registration',
      first_name: 'first name',
      last_name: 'last name',
      partner_id: 'partner id',
      repeat_password: 'repeat password',
      i_accept: 'I accept',
      terms_of_agreement: 'terms of agreement',
      sign_up: 'Sign up',
      sign_up_success: 'Successfully registered! Please check your email to activate your account.',
      sign_up_error_referral: 'Partner ID is required. If this is your first time on the site and you don\'t have any code, please contact',
      to_support: 'support',
      recover_success: 'Success! Please check your email for further instructions.',
      recover_error: 'Error: make sure email is entered correctly',
      login_failed: 'Check your email/password and make sure you activated your account',
      login_failed_pin: 'Please check your email/password and pin-code',
    },
    footer: {
      tos: "Terms of Use",
      privacy: "Privacy Policy",
      cookies: "Cookies Policy"
    },
    header_menu: {
      exchange: "Exchange",
      about: "About",
      howtouse: "How to use",
      transparency: "Transparency",
      wallet: "Wallet",
      contacts: "Contacts"
    },
    exchange: {
      buy: "Buy",
      sell: "Sell",
      last_bills: "Last bills",
      empty_bills: "Your bills list is empty",
      more_bills: "More",
      confirm_wallet: "Confirm wallet",
      confirm: "Confirm",
      cr_payment_bill: "Create payment bill",
      create: "Create",
      amount_err: "Minimum amount ",
      bill_payment: "Bill payment",
      send: "Send",
      receive: "Receive",
      verify_auto: "We verify payment automatically.",
      verify_asap:
        "As soon as payment is made, the status of this state will change to another.",
      success: "Success!",
      issued: "issued",
      wallet: "Wallet",
      buy_more: "Buy more",
      sell_more: "Sell more",
      status: 'Status',
      received_payment: 'Received payment',
      sent_payment: 'Payment sent',
      choose_btc_wallet: {p1: 'Choose BTC wallet', p2: 'to get coins after redeem'},
      choose_btc_wallet_error: 'Please choose a BTC wallet',
      transaction_hash: 'Transaction hash',
      confirms: 'Confirmations',
      payment_confirmation_buy: 'As soon as network get 3 confirmations, SIMBA tokens will be issued to your ETH address.',
      payment_confirmation_sell: 'As soon as network get 3 confirmations, BTC will be sent to your address.',
      statuses: {
        completed: 'Paid',
        created: 'Created',
        waiting: 'Waiting',
        cancelled: 'Cancelled',
        expired: 'Expired'
      },
      error_creating_invoice: 'Error creating invoice',
      error_updating_invoice: 'Error updating invoice',
      error_confirming_invoice: 'Error confirming invoice',
      bill_expired: 'Bill expired',
      time_is_out: 'Time is out',
      time_is_limited: 'Time for each bill is limited with 2 hours.',
      simba_redemption: 'Simba redemption',
      send_simba_now: 'Send SIMBA now'
    },
    dropdown: {
      bill_details: "Bill details",
      personal_data: "Personal data",
      security: "Security Settings",
      logout: "Log out"
    },
    socials: {
      facebook: "https://www.facebook.com/simbastorage",
      bitcoin: "https://bitcointalk.org/index.php?action=profile;u=2816745",
      instagram: "https://www.instagram.com/simbastorage/",
      medium: "https://medium.com/@simbastorage",
      zen: "https://zen.yandex.ru/simba",
      reddit: "https://www.reddit.com/r/simbastorage",
      twitter: "https://twitter.com/SWISSSST",
      vk: "https://vk.com/simbastorage",
      telegram: "https://t.me/simbastorage",
      telegram_chat: "https://t.me/simbastorage_en",
      discord: "https://discord.com/channels/SimbaStorage#6018",
      streemit: "https://steemit.com/@simbastorage",
      github: "#",
      linkedin: "http://www.linkedin.cn/company/simbastorage"
    },
    profile: {
      sidebar: {
        personal: "Personal",
        data: "Data",
        verification: "Verification",
        payment: "Payment",
        bill_details: "Bill details",
        partner_program: "Partner program",
        security: "Security",
        change_password: "Change password",
        two_factor: "Two-Factor Auth",
        logout: "Logout"
      },
      edit_my_profile: "Edit my profile",
      identity: "Identify verification",
      email_verified: "Email verified",
      email_unverified: "Email Unverified",
      email_verification: "Email verification",
      verify_address: "Verify address",
      id_verification: "ID verification",
      source_of_funds_verification: "Source of funds verification",
      scan_qr_code: 'Scan this QR code',
      after_scan_hit_enable: 'After code scanning type pin code below and hit enable button.',
      pin_code: 'Pin code',
      btc_address_list: 'BTC Address list',
      eth_address_list: 'ETH Address list',
      for_withdraw_btc: 'for withdrawal Bitcoin when redeem SIMBA',
      for_issue_simba: 'for issue SIMBA',
    },
    messages: {
      two_factor_enable_failed: 'Failed to enable two-factor authentication!',
      two_factor_enable_success: 'Two-factor authentication successfuly enabled!',
      two_factor_disable_failed: 'Failed to disable two-factor authentication!',
      two_factor_disable_success: 'Two-factor authentication successfuly disabled!',
    },
    partner: {
      main:
        "Get tokens for each deposit of users invited via your " +
        "<a href='#' id='text-ref-link' class='link' rel='noreferrer noopener' target='_blank'>link</a>. " +
        "How it works?<br><br>" +
        "1. You copy the link and send it to your friend.<br>" +
        "2. After sign up with your link, it will be tied to your account.<br>" +
        "3. With each recharge, you will receive SST tokens that you can sell" +
        "on the exchange at the current rate.<br><br>The offer is limited by amount of provided SST tokens.",
      invited: "Invited",
      your_ref_link: "Your partner link",
      your_ref_code: "Your partner code",
      refs_empty: "You don't have invited users yet",
      how_to_get_code: {p1: "To get your partner code, ", p2: "add", p3: "your reward wallet"}
    },
    password: {
      current: "Current password",
      new: "New password",
      confirm: "Password confirmation",
      change_success: "Your password successfully changed!",
      change_error: "Failed to change password!"
    },
    transparency: {
      curr_balances: "Current balances"
    },
    wallet: {
      transfer_simba: "Transfer SIMBA tokens",
      your_wallet: "Your wallet",
      recipient: "Recipient",
      add_wallet: "add new",
      txs_history: "History of transactions",
      delete_wallet: "delete",
      delete_sure: "Are you sure you want to delete this address",
      txs_history_empty: "Your transaction history is empty.",
      transaction_failed: 'Transaction failed',
      transaction_success: 'Transaction completed successfully',
      pin_code: 'Pin-code',
      add_new_wallet: { p1: 'Add new', p2:'wallet'},
      address_deleted: 'Address successfully deleted!',
      address_added: 'Address successfully deleted!',
      address_failed_with_pin: 'Failed to add address, make sure you entered correct address and pin-code!',
      address_failed_to_add: 'Error: make sure your provided address is correct, maybe this address already exists',
      failed_to_get_signature: 'Failed to get signature!',
    },
    other: {
      try_again: 'Try again',
      add: 'Add',
      date: "Date",
      fee: "Fee",
      total: "Total",
      send: "Send",
      address: "Address",
      type: "Type",
      amount: "Amount",
      more: "more",
      sent: "Sent",
      name: "Name",
      delete: "Delete",
      cancel: "Cancel",
      level: "Level",
      reg_date: "Registration date",
      change: "Change",
      enable: "Enable",
      disable: "Disable",
      first_name: 'First name',
      last_name: 'Last name',
      save: 'Save',
      copied_to_clipboard: 'Copied to clipboard'
    },
    about: {
      company_goal: "Company goal",
      goal:
        "The name SIMBA shows the strength, power, honesty and a friendly attitude towards the world in which we develop this business. We have combined together the knowledge and experience of professionals who are in the blockchain and crypto industry for more than 3-5 years.<br /> SIMBA aims to be the most convenient and robust platform for Bitcoin storage. Our product brings security and efficiency for long-term holdings of crypto assets. It provides a secure storage of institutional level with a user-friendly interface and high level of privacy.",
      date_of_establishment: "Date of establishment",
      establishment: "The SIMBA project was founded in October 2019.",
      сompany_locations: "Company locations",
      locations:
        "By the end of 2020, SIMBA has locations in 5 countries: Switzerland, Liechtenstein, the United Arab Emirates, Estonia and New Zealand.",
      our_mission: "Our mission",
      mission:
        'The common goal of our team is to provide the best service for the followers and supporters of cryptocurrencies and the whole blockchain industry. Each of us had a development path in the crypto industry in his or her own way. We were brought together by a common belief that we are able to show the world a unique product that will serve people. That is why it is so reliable, transparent and convenient that every user can be proud to say "I store my Bitcoins in the SIMBA storage". The cold SIMBA storage means a secure future with no worries. Our mission is to maintain these standards at the highest level, grow and soar to new heights.'
    }
  };

  return new Promise(function(resolve) {
    resolve(locale);
  });
};
