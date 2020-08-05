<template>
  <div class="card two-fa-window">
    <!--<div class="card-content">
      <div class="title is-4">{{$t('other.enable')}} 2FA</div>
      <div class="mt-2">
        <p class="subtitle">1. {{$t('profile.scan_qr_code')}}</p>
        <qrcode-vue
          class="mt-2"
          :value="value"
          :size="size"
          level="H"
        ></qrcode-vue>
      </div>
      <div class="mt-2">
        <p class="subtitle">
          2. {{$t('profile.after_scan_hit_enable')}}.
        </p>
        <b-field class="mt-2">
          <b-input type="number" v-model="confirm2faData.pin_code" :placeholder="$t('profile.pin_code')"></b-input>
        </b-field>
      </div>
      <div>
        <b-button @click="enable2fa" class="btn w-100 mt-4">{{$t('other.enable')}}</b-button>
      </div>
    </div>-->
    <div class="card-content">
      <div class="title is-5 main-title">{{$t('other.enable')}} 2FA</div>
      <div class="two-fa-step">
        <i18n class="title is-6" path="account_page.two_factor_modal.step1.title" tag="div">
          <template #link>
            <a href="https://support.google.com/accounts/answer/1066447?co=GENIE.Platform%3DAndroid&hl=en&oco=0" rel="noreferrer noopener" target="_blank">Google Authenticator</a>
          </template>
        </i18n>
        <div>{{ $t('account_page.two_factor_modal.step1.subtitle')}}</div>
      </div>
      <div class="two-fa-step">
        <div class="title is-6">{{ $t('account_page.two_factor_modal.step2.title')}}</div>
        <div>{{ $t('account_page.two_factor_modal.step2.subtitle')}}</div>
      </div>
      <div class="two-fa-step">
        <div class="title is-6">{{ $t('account_page.two_factor_modal.step3.title')}}</div>
        <div class="is-flex align-items-center">
          <qrcode-vue
            :value="value"
            :size="size"
            level="H"
          ></qrcode-vue>
          <div class="two-fa-step__backup">
            <div class="black">{{ $t('account_page.two_factor_modal.step3.subtitle')}}</div>
            <div class="two-fa-step__backup-input">{{ confirm2faData.token }}</div>
            <div class="is-uppercase has-text-weight-bold black">{{ $t('account_page.two_factor_modal.attention')}}</div>
          </div>
        </div>
      </div>
      <div class="two-fa-step">
        <div class="title is-6">{{ $t('account_page.two_factor_modal.step4.title')}}</div>
        <ValidationObserver tag="div" ref="form_pincode">
            <ValidationProvider rules="required|digits:6" v-slot="{ errors }" :name="$i18n.t('account_page.two_factor_modal.six_digit_code')" tag="div">
              <div class="is-flex align-items-center">
                <input v-model="confirm2faData.pin_code" type="text" maxlength="6" class="smb-input mr-2" :placeholder="$i18n.t('account_page.two_factor_modal.six_digit_code')">
                <button @click="enable2fa" class="btn">{{$t('other.enable')}}</button>
              </div>
              <div class="error">{{ errors[0] }}</div>
            </ValidationProvider>
        </ValidationObserver>
      </div>
    </div>
  </div>
</template>
<script>
import QrcodeVue from "qrcode.vue";

import { ValidationProvider, ValidationObserver } from 'vee-validate'

export default {
  data() {
    return {
      value: "",
      size: 180,
      confirm2faData: {
        token: '',
        pin_code: null,
      }
    };
  },
  components: {
    QrcodeVue
  },
  methods: {
    async enable2fa() {
      let isValid = await this.$refs.form_pincode.validate();

      if(isValid) {
        this.$store.dispatch('confirm2fa', this.confirm2faData)
        this.$parent.close()
      }
    }
  },
  async created() {
    const { data } = await this.$axios.get("/account/2fa/");
    this.value = data.URL;

    const reg = new RegExp("[?&]" + "secret" + "=([^&#]*)", "i");
    const queryString = reg.exec(this.value);
    this.confirm2faData.token = queryString ? queryString[1] : null;
  }
};
</script>

<style lang="sass" scoped>
.error
  color: #DC6161
  width: 220px
  padding-top: 5px
  font-size: 12px

.smb-input
  border: 1px solid #000000
  &:focus::placeholder
    opacity: 0
  &::placeholder
    color: #000000
    font-weight: normal
    opacity: 1
    transition: 100ms opacity

.black
  color: #000000

.title
  color: #000000
  margin-bottom: 15px

.main-title
  margin-bottom: 35px

.two-fa-step
  padding-bottom: 20px
  margin-bottom: 20px
  border-bottom: 1px solid #DFDFDF
  color: #8C8C8C
  &:last-child
    padding-bottom: 0
    margin-bottom: 0
    border-bottom: none

  &__backup
    flex: 1 1 0
    margin-left: 20px
    &-input
      margin: 16px 0
      padding: 28px
      background-color: #FFDB62
      text-align: center
      font-weight: bold
      font-size: 36px
      line-height: 100%
      color: #000000

.two-fa-window
  width: 810px
  padding: 40px
  .card-content
    padding: 0
</style>
