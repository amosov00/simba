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
      choose_eth_wallet: {p1: 'Choose ETH wallet', p2: 'to sell SIMBA'},
      choose_btc_wallet_error: 'Please choose a BTC wallet',
      transaction_hash: 'BTC payout',
      confirms: 'Confirmations',
      payment_confirmation_buy: 'As soon as network get 3 confirmations, SIMBA tokens will be issued to your ETH address.',
      payment_confirmation_sell: 'As soon as network get {min_confirms} confirmation(s), BTC will be sent to your address.',
      statuses: {
        completed: 'Completed',
        paid: 'Paid',
        created: 'Created',
        waiting: 'Waiting',
        cancelled: 'Cancelled',
        expired: 'Expired',
        processing: 'Processing'
      },
      error_creating_invoice: 'Error creating invoice',
      error_updating_invoice: 'Error updating invoice',
      error_confirming_invoice: 'Error confirming invoice',
      bill_expired: 'Bill expired',
      time_is_out: 'Time is out',
      time_is_limited: 'Time for each bill is limited with 2 hours.',
      simba_redemption: 'Simba redemption',
      send_simba_now: 'Send SIMBA now',
      applied_fee: 'Applied fee',
      fee_in_simba: '(charged in SIMBA)'
    },
    dropdown: {
      bill_details: "Bill details",
      personal_data: "Personal data",
      security: "Security Settings",
      partner_program: 'Partner program',
      logout: "Log out"
    },
    socials: {
      facebook: "https://www.facebook.com/simbastorage",
      bitcoin: "https://bitcointalk.org/index.php?topic=5260057.msg54734561#msg54734561",
      instagram: "https://www.instagram.com/simbastorage/",
      medium: "https://medium.com/@simbastorage",
      zen: "https://zen.yandex.ru/simba",
      reddit: "https://www.reddit.com/r/simba_official/",
      twitter: "https://twitter.com/SWISSSST",
      vk: "https://vk.com/simbastorage",
      telegram: "https://t.me/simbastorage",
      telegram_chat: "https://t.me/simbastorage_en",
      discord: "https://discord.com/channels/SimbaStorage#6018",
      streemit: "https://steemit.com/@simbastorage",
      github: "#",
      linkedin: "https://www.linkedin.com/company/simbastorage/"
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
        "3. With each recharge, you will receive SST tokens that you can sell <br>" +
        "on the exchange at the current rate.<br>" +
        "4. When your referrals invite with their partner link, you'll recieve an additional bonus.<br>" +
        "So for 5 levels you will get: 5%, 1%, 1%, 0.5% and 0.5%<br>" +
        "<br>The offer is limited by amount of provided SST tokens.",
      invited: "Invited",
      your_ref_link: "Your partner link",
      your_ref_code: "Your partner code",
      your_reward_address: 'Your ETH reward address',
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
      new_eth_wallet_instruct: {
        text1: 'To add a new address, press "Add" button',
        text2: 'If this is your first time, please install {metamask} extension.',
        text3: 'For mobile devices we recommend the {metamask} or {imtoken} application.',
      },
      eth_wallet_switch_info: 'to change the address you need to switch in the wallet',
      new_btc_wallet_instruct: {
        text1: 'By adding the BTC address of your wallet you confirm that you have entered the correct one.',
        text2: 'For total and irrevocable loss of funds when withdrawing to these address you accept the responsibility.'
      },
      security_verification: 'Security verification',
      confirm_verification: 'To confirm, please complete the verification by entering pin-code',
      address_exist: 'This address already exists in your list!'
    },
    other: {
      confirm: 'Confirm',
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
      copied_to_clipboard: 'Copied to clipboard',
      search: 'Search',
      search_empty_results: 'No results found',
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
    },
    account_page: {
      _id: 'ID',
      email: 'Email',
      email_is_active: 'Email is activated',
      verification_code: 'Verification code',
      recover_code: 'Recovery code',
      secret_2fa: '2FA secret',
      two_factor: '2FA enabled',
      first_name: 'First name',
      last_name: 'Last name',
      user_btc_addresses: 'Bitcoin address list',
      user_eth_addresses: 'Ethereum address list',
      btc_address: 'BTC address',
      is_staff: 'Is staff',
      is_superuser: 'Is superuser',
      is_active: 'Is active',
      terms_and_condition: 'Accepted terms and condition',
      created_at: 'Date of registration',
      list_is_empty: 'Empty',
      yes: 'Yes',
      no: 'No',
      not_available: 'N/A',
      account_info: 'Account information',
      account_changed_success: 'Account data successfully changed!',
      account_changed_error: 'Error changing account data!',
      deleted_addresses: 'Archived addresses (deleted)',
      two_factor_modal: {
        step1: {
          title: '1. Install OTP Mobile App (we recommend {link}).',
          subtitle: 'Use an app on your mobile to obtain single-use validation codes, even when your phone is offline. Available on Android, iPhone and Windows Phone.'
        },
        step2: {
          title: '2. Attention!',
          subtitle: 'The code in Step 3 should be saved to restore access to your personal account, if you lose your device or access to application that generates one-time passwords.'
        },
        step3: {
          title: '3. Scan QR Code',
          subtitle: 'If you unable to scan the QR code, please enter this code manually into the app.'
        },
        attention: 'THIS IS BACKUP CODE. PLEASE SAVE IT ON A PAPER CAREFULLY',
        step4: {
          title: '4. Enter the code generated in your App'
        },
        six_digit_code: '6 digit code'
      },
      enabled_2fa: 'Enabled 2FA'
    },
    su_invoices: {
      invoices: 'Invoices',
      invoice: 'Invoice',
      user_id: "User ID",
      status: "Status",
      invoice_type: "Operation",
      btc_amount: "BTC amount",
      simba_amount: "SIMBA amount",
      btc_amount_proceeded: "BTC amount proceeded",
      simba_amount_proceeded: "Simba amount proceeded",
      target_eth_address: "Target ETH address",
      target_btc_address: "Target BTC address",
      eth_tx_hashes: "ETH transaction hashes",
      btc_tx_hashes: "BTC transaction hashes",
      created_at: "Date of creation",
      finised_at: "Date of completion",
      _id: "ID",
      eth_txs: "ETH transactions",
      btc_txs: "BTC transactions",
      not_available: "N/A",
      not_paid: "Unpaid",
      empty: "Empty",
      sst_tx_hashes: 'SST transaction hashes',
      sst_tx_detailed: 'SST transactions (detailed)',
      sst_tx_table: {
        show: 'Show',
        hide: 'Hide',
        transactionHash: 'Hash',
        amount: 'Reward',
        user_id: 'User ID',
        level: 'Level'
      }
    },
    xpub: {
      confirm_your_action: 'Confirm your action',
      confirm_change_status: 'Are you sure you want to change the status?',
      something_went_wrong: 'Something went wrong!',
      status_changed: 'Status successfully changed!',
      status_active: 'Active',
      status_inactive: 'Inactive',
    },
    su_users: {
      users: 'Users',

    },
    su_payouts_mm: {
      manage_payouts: { full: 'Payouts management', short: 'Manage payouts' },
      date: "Date",
      transactions: "Transactions",
      payout: "Payout",
      actions: "Actions",
      target_address: "Payout address",
      pay: "Pay",
      cancel: "Cancel",
      confirm_cancel_msg: "Are you sure you want to CANCEL this invoice?",
      confirm_pay_msg: "Are you sure you want to PAYOUT on this invoice?",
      status: "Manual mode",
      enabled: "Enabled",
      disabled: "Disabled",
      change_status: "Change status",
      processing_only: "With \"Processing\" status only",
      refresh: "Refresh"
    }
  };

  return new Promise(function(resolve) {
    resolve(locale);
  });
};
