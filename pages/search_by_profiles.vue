<template>
  <div class="container">
    <nuxt-link :to="{ path: 'search' }">
      <button>一覧へ</button>
    </nuxt-link>
    <v-row>
      <nuxt-link
        :to="{
          path: 'search',
          query: {
            age_min: age_min,
            age_max: age_max,
            //prefectures: prefectures
          }
        }"
      >
        <v-btn class="mr-4">検索</v-btn>
      </nuxt-link>
      <v-btn class="mr-4" @click="onReset">リセット</v-btn>
    </v-row>
    <!-- <v-select
      v-model="prefectures"
      :items="prefectures_option"
      label="都道府県"
      multiple
      chips
    ></v-select>-->

    <v-select v-model="age_min" :items="age_min_option" label="何歳以上"></v-select>

    <v-select v-model="age_max" :items="age_max_option" label="何歳以下"></v-select>
  </div>
</template>
<style scoped>
.box {
  display: inline-block;
  width: 100px;
}
</style>

<script>
//   methods: {
//     async onSubmit(evt) {},
//     onReset(evt) {
//       evt.preventDefault();
//       // Reset our form values
//       this.form.age_min = 17;
//       this.form.age_max = 31;
//       this.form.prefectures = null;
//       // Trick to reset/clear native browser form validation state
//       this.show = false;
//       this.$nextTick(() => {
//         this.show = true;
//       });
//     }
//   }
// };

export default {
  data: () => ({
    prefectures: null,
    age_min: null, //17
    age_max: null, //31
    prefectures_option: ["東京都", "埼玉県", "神奈川県"],
    age_min_option: [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    age_max_option: [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
  }),

  methods: {
    onReset() {
      this.prefectures = null;
      this.age_min = null;
      this.age_max = null;
    },
  },
};
</script>
