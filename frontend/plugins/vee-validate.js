import { extend, localize } from 'vee-validate';
import { required, email, min, confirmed, max, regex, alpha_num, alpha, alpha_spaces } from 'vee-validate/dist/rules';
import en from 'vee-validate/dist/locale/en.json';
import { setInteractionMode } from 'vee-validate';

setInteractionMode('eager');

// Install English and Arabic locales.
localize({
  en
});

extend('email', email);
extend('min', min);
extend('max', max);
extend('regex', regex);
extend('alpha', alpha);
extend('alpha_num', alpha_num);
extend('alpha_spaces', alpha_spaces);
extend('required', required);
extend('confirmed', confirmed);
