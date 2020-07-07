<template>
  <div class="card two-fa-window">
    <div class="card-content">
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
    </div>
  </div>
</template>
<script>
import QrcodeVue from "qrcode.vue";

export default {
  data() {
    return {
      value: "",
      size: 230,
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
    enable2fa() {
      this.$store.dispatch('confirm2fa', this.confirm2faData)
      this.$parent.close()
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
.two-fa-window
  max-width: 647px
  padding: 20px 40px
  text-align: center
</style>
