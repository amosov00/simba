import Vue from 'vue'
import { extend, setInteractionMode, ValidationObserver, ValidationProvider } from 'vee-validate'
import {
  alpha,
  alpha_num,
  alpha_spaces,
  confirmed,
  digits,
  email,
  max,
  min,
  regex,
  required,
} from 'vee-validate/dist/rules'

Vue.component('ValidationObserver', ValidationObserver)
Vue.component('ValidationProvider', ValidationProvider)

setInteractionMode('eager')

extend('email', email)
extend('min', min)
extend('max', max)
extend('regex', regex)
extend('alpha', alpha)
extend('alpha_num', alpha_num)
extend('alpha_spaces', alpha_spaces)
extend('required', required)
extend('confirmed', confirmed)
extend('digits', digits)
