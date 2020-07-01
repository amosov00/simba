export default function ({ app }, inject) {

  let lang = app.$cookies.get('app_lang');

  app.i18n.onLanguageSwitched = (oldLocale, newLocale) => {
    $nuxt.$emit('locale-changed', { oldLocale, newLocale })
  }

  if(lang) {
    app.i18n.setLocale(lang)
  }
}
