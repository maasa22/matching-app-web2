<template>
  <div>
    <div class="container2">
      <div class="chat_title"></div>
      <div class="msg_history"></div>
      <div class="input_area"></div>
    </div>
  </div>
</template>
<script>
export default {};
</script>
<style scoped>
html,
body {
  height: 100vh;
}

.container2 {
  height: 50vh;
  top: 20px;
  bottom: 20px;
  border: black;
}
.chat_title {
  height: 50%;
  background-color: beige;
}
.msg_history {
  height: 30%;
  background-color: #553333;
}
.input_area {
  height: 20%;
  background-color: #115500;
}
</style>
