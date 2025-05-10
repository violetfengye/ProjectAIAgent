<template>
  <div class="login-container">
    <a-card class="login-card" title="AI辅助软件工程平台">
      <a-form
        :model="formState"
        name="login"
        @finish="onFinish"
        autocomplete="off"
      >
        <a-form-item
          name="username"
          :rules="[{ required: true, message: '请输入用户名!' }]"
        >
          <a-input v-model:value="formState.username" placeholder="用户名">
            <template #prefix>
              <UserOutlined />
            </template>
          </a-input>
        </a-form-item>

        <a-form-item
          name="password"
          :rules="[{ required: true, message: '请输入密码!' }]"
        >
          <a-input-password
            v-model:value="formState.password"
            placeholder="密码"
          >
            <template #prefix>
              <LockOutlined />
            </template>
          </a-input-password>
        </a-form-item>

        <a-form-item>
          <a-button type="primary" html-type="submit" :loading="loading" block>
            登录
          </a-button>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from "vue";
import { UserOutlined, LockOutlined } from "@ant-design/icons-vue";
import { useRouter } from "vue-router";

const router = useRouter();
const loading = ref(false);

const formState = reactive({
  username: "",
  password: "",
});

const onFinish = async (values: any) => {
  loading.value = true;
  try {
    // TODO: 实现登录逻辑
    console.log("Success:", values);
    router.push("/");
  } catch (error) {
    console.error("Login failed:", error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f0f2f5;
}

.login-card {
  width: 100%;
  max-width: 400px;
}
</style>
