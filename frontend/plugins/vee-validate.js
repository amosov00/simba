import Vue from 'vue';
import { extend } from 'vee-validate';
import { required, email, min, confirmed, max, regex, alpha_num, alpha, alpha_spaces, digits } from 'vee-validate/dist/rules';
import { setInteractionMode, ValidationObserver, ValidationProvider, } from 'vee-validate';

Vue.component('ValidationObserver', ValidationObserver)
Vue.component('ValidationProvider', ValidationProvider)

setInteractionMode('eager');


extend('email', email);
extend('min', min);
extend('max', max);
extend('regex', regex);
extend('alpha', alpha);
extend('alpha_num', alpha_num);
extend('alpha_spaces', alpha_spaces);
extend('required', required);
extend('confirmed', confirmed);
extend('digits', digits);

