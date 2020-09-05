<template>
  <div class="container">
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
        <v-btn class="mr-4">登録</v-btn>
      </nuxt-link>
    </v-row>
    <v-select v-model="gender" :items="gender_option" label="性別"></v-select>
    <!-- <v-select
      v-model="prefectures"
      :items="prefectures_option"
      label="都道府県"
      multiple
      chips
    ></v-select>-->
    <v-select v-model="age_min" :items="age_min_option" label="何歳以上"></v-select>
  </div>
</template>
<style scoped>
.box {
  display: inline-block;
  width: 100px;
}
</style>

<script>
export default {
  data: () => ({
    gender: null,
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
