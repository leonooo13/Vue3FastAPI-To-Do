<template>
  <PostIt class="post-it">
    <form @submit.prevent="submitRegistrationDetails">
      <div class="container">
        <h2>创建账户</h2>
        <div class="icon-div" :class="{ isError: errorName }">
          <img src="@/assets/register/user.png" alt="user" class="user-img" />
          <input type="text" placeholder="输入姓名" v-model="name" @blur="errorName = ''" @keypress="errorName = ''" />
        </div>
        <span v-if="errorName" class="error">{{ errorName }}<br /></span>

        <div class="icon-div" :class="{ isError: errorEmail }">
          <img src="@/assets/register/email.png" alt="email" class="email-img" />
          <input type="text" placeholder="输入邮箱" v-model="email" @blur="errorEmail = ''"
            @keypress="errorEmail = ''" />
        </div>
        <span v-if="errorEmail" class="error">{{ errorEmail }}<br /></span>
        <div class="icon-div" :class="{ isError: errorUsername }">
          <img src="@/assets/register/username.png" alt="username" class="username-img" />
          <input type="text" placeholder="输入用户名" v-model="username" @blur="errorUsername = ''"
            @keypress="errorUsername = ''" />
        </div>
        <span v-if="errorUsername" class="error">{{ errorUsername }}<br /></span>

        <div class="icon-div" :class="{ isError: errorPassword }">
          <img src="@/assets/register/password.png" alt="password" class="password-img" />
          <input id="inline-input" :type="passwordType" placeholder="输入密码" v-model="password"
            @blur="errorPassword = ''" @keypress="errorPassword = ''" />
          <img :src="showPassword ? openEyesURL : closedEyesURL" alt="show-password" class="show-password-img"
            @click="toggleShow" />
        </div>
        <div class="icon-div" :class="{ isError: errorPassword }">
          <img alt="password-verification" class="verification-img"
            :src="passwordsMatch ? lockedPasswordURL : unlockedPasswordURL" :class="passwordsMatch
              ? 'password-is-confirmed'
              : 'password-not-confirmed'
              " />
          <input :type="passwordType" placeholder="再次输入密码" v-model="passwordConfirmation"
            @blur="errorPassword = ''" @keypress="errorPassword = ''" />
        </div>
        <span v-if="errorPassword" class="error" style="margin-top: 5px; display: block">{{ errorPassword }}</span>
        <span v-if="errorRegister" class="error" style="margin-top: 5px; display: block">
          {{ errorRegister }}</span>
        <span v-else><br /></span>
        <button class="button-74" type="submit">注册</button>

        <div style="margin-top: 15px;">
          已有账户?
          <router-link to="/login">登录</router-link>
        </div>

      </div>
    </form>
  </PostIt>
</template>

<script setup>
import { ref, watch } from "vue";
import { useAuthStore } from "@/store/authStore.js";
import PostIt from "@/components/layout/PostIt.vue";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();
// 从后端获取注册错误信息
const { errorRegister } = storeToRefs(authStore);
const name = ref("");
const email = ref("");
const emailRegEx =
  /^(([^<>()\]\\.,;:\s@"]+(\.[^<>()\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/;

const errorName = ref("");
const errorEmail = ref("");
const errorUsername = ref("");
const errorPassword = ref("");

const username = ref("");
const password = ref("");
const passwordConfirmation = ref("");
const showPassword = ref(false);
const passwordType = ref("password");
const passwordsMatch = ref(false);

const lockedPasswordURL = new URL("@/assets/register/locked.png", import.meta.url).href;
const unlockedPasswordURL = new URL("@/assets/register/unlocked.png", import.meta.url).href;

const openEyesURL = new URL("@/assets/register/eyes.png", import.meta.url).href;
const closedEyesURL = new URL("@/assets/register/closed_eyes.png", import.meta.url).href;

function toggleShow() {
  showPassword.value = !showPassword.value;
  if (showPassword.value) {
    passwordType.value = "text";
  } else {
    passwordType.value = "password";
  }
}
async function submitRegistrationDetails() {
  // 验证姓名
  if (name.value === "") {
    errorName.value = "请输入姓名";
  } else {
    errorName.value = "";
  }

  // 验证邮箱
  if (email.value === null || email.value === "") {
    errorEmail.value = "请输入邮箱";
  } else if (!emailRegEx.test(email.value)) {
    errorEmail.value = "请输入有效的邮箱";
  } else {
    errorEmail.value = "";
  }

  // 验证用户名
  if (username.value === "") {
    errorUsername.value = "请输入用户名";
  } else {
    errorUsername.value = "";
  }

  // 验证密码匹配
  if (password.value === "" || passwordConfirmation.value === "") {
    errorPassword.value = "请输入密码";
  } else if (password.value !== passwordConfirmation.value) {
    errorPassword.value = "密码不匹配";
  } else {
    errorPassword.value = "";
  }

  // 一次性检查所有错误
  let errorsArray = [
    errorName.value,
    errorEmail.value,
    errorUsername.value,
    errorPassword.value,
  ];
  const checker = (arr) => arr.every((arr) => arr === "");

  if (checker(errorsArray)) {
    const payload = {
      name: name.value,
      email: email.value,
      username: username.value,
      password: password.value,
    };
    await authStore.register(payload);
  }
}

// 如果任何输入发生变化，清除后端错误
watch([name, username, email, password, passwordConfirmation], () => {
  errorRegister.value = false;
});

watch([password, passwordConfirmation], () => {
  if (passwordConfirmation.value !== password.value) {
    passwordsMatch.value = false;
  } else {
    passwordsMatch.value = true;
  }
});
</script>

<style scoped>
* {
  font-family: "Kalam", cursive;
}

.user-img,
.email-img,
.username-img {
  width: 25px;
  height: 25px;
}

.password-img,
.verification-img {
  width: 20px;
  height: 20px;
  margin-left: 2px;
}

.show-password-img {
  width: 25px;
  height: 25px;
  margin-right: 3px;
}

.password-is-confirmed {
  filter: invert(50%) sepia(31%) saturate(1012%) hue-rotate(60deg) brightness(98%) contrast(87%);
}

.password-not-confirmed {
  filter: invert(14%) sepia(67%) saturate(5511%) hue-rotate(356deg) brightness(86%) contrast(98%);
}

#icon {
  margin-right: 10px;
}

.fa-icons {
  font-size: 18px;
  margin-left: 5px;
}

.icon-div {
  display: flex;
  flex-direction: row;
  border: 1px solid #374669;
  border-radius: 5px;
  background: #fff;
  align-items: center;
  overflow: hidden;
  margin-top: 2px;
}

.icon-div input {
  outline: none;
  border: none;
  background: none;
  font-size: 1em;
  padding: 0.3em;
  color: inherit;
  flex: auto 1 1;
  width: 100%;
  background: none;
  background-color: transparent;
}

.post-it {
  font-size: 15px;
  width: 200px;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}

#google:hover {
  background-color: rgb(238, 238, 172);
}

.error {
  color: red;
}

.isError {
  border: 0.5px solid red;
}

.button-74 {
  background-color: #fbeee0;
  border: 2px solid #422800;
  border-radius: 25px;
  box-shadow: #422800 4px 4px 0 0;
  color: #422800;
  cursor: pointer;
  display: inline-block;
  font-weight: 600;
  font-size: 18px;
  padding: 0 18px;
  line-height: 40px;
  text-align: center;
  text-decoration: none;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  margin-top: 10px;
}

.button-74:hover {
  background-color: #fff;
}

.button-74:active {
  box-shadow: #422800 2px 2px 0 0;
  transform: translate(2px, 2px);
}

@media (min-width: 768px) {
  .button-74 {
    min-width: 120px;
    padding: 0 25px;
  }
}

/* headlines with lines */
.decorated {
  overflow: hidden;
  text-align: center;
}

.decorated>span {
  position: relative;
  display: inline-block;
}

.decorated>span:before,
.decorated>span:after {
  content: "";
  position: absolute;
  top: 50%;
  border-bottom: 1px solid;
  width: 100vw;
  margin: 0 20px;
}

.decorated>span:before {
  right: 100%;
}

.decorated>span:after {
  left: 100%;
}
</style>