export default function ({ app }, inject) {

  let lang = app.$cookies.get('app_lang');

  app.i18n.onLanguageSwitched = (oldLocale, newLocale) => {
    $nuxt.$emit('locale-changed', {oldLocale, newLocale})
  }

/*  app.i18n.beforeLanguageSwitch = () => {
    document.body.classList.add('test')

    document.querySelector('body.test').addEventListener('animationend', () => {
      document.body.classList.remove('test');
      console.log('anim end!')
    })
  }*/

  if(lang) {
    app.i18n.setLocale(lang)
  }
}
