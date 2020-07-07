import { localize } from 'vee-validate';

function loadLocale(code) {
  return import(`vee-validate/dist/locale/${code}.json`).then(locale => {
    localize(code, locale);
  });
}

export default function ({ app }, inject) {

  let lang = app.$cookies.get('app_lang');

  // before lang switch
  app.i18n.beforeLanguageSwitch = (oldLocale, newLocale) => {
    loadLocale(newLocale)
  }

  // after lang switch
  app.i18n.onLanguageSwitched = (oldLocale, newLocale) => {
    $nuxt.$emit('locale-changed', {oldLocale, newLocale})
  }

  // if lang is set inside cookies, set locale according to it
  if(lang) {
    loadLocale(lang)
    app.i18n.setLocale(lang)
  }
}
