<template>
  <a-layout class="layout">
    <a-layout-header>
      <div class="logo" />
      <a-menu
        v-model:selectedKeys="selectedKeys"
        theme="dark"
        mode="horizontal"
        :style="{ lineHeight: '64px' }"
      >
        <a-menu-item key="home">
          <router-link to="/">首页</router-link>
        </a-menu-item>
        <a-menu-item key="requirements">
          <router-link to="/requirements">需求管理</router-link>
        </a-menu-item>
        <a-menu-item key="architecture">
          <router-link to="/architecture">架构设计</router-link>
        </a-menu-item>
        <a-menu-item key="code">
          <router-link to="/code">代码生成</router-link>
        </a-menu-item>
        <a-menu-item key="testing">
          <router-link to="/testing">测试管理</router-link>
        </a-menu-item>
        <a-menu-item key="deployment">
          <router-link to="/deployment">部署管理</router-link>
        </a-menu-item>
      </a-menu>
    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <div :style="{ background: '#fff', padding: '24px', minHeight: '280px' }">
        <router-view></router-view>
      </div>
    </a-layout-content>
    <a-layout-footer style="text-align: center">
      AI辅助软件工程平台 ©2025 Created by Isaleafa.
    </a-layout-footer>
  </a-layout>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const selectedKeys = ref([(route.name as string) || 'home'])
</script>

<style scoped>
.layout {
  min-height: 100vh;
}
.logo {
  float: left;
  width: 120px;
  height: 31px;
  margin: 16px 24px 16px 0;
  background: rgba(255, 255, 255, 0.3);
}
</style>
