<template>
  <div class="home">
    <a-row :gutter="[16, 16]">
      <a-col :span="24">
        <a-card>
          <h1>欢迎使用AI辅助软件工程平台</h1>
          <p>
            本平台集成了先进的AI技术，帮助您更高效地完成软件开发全生命周期的管理工作。
          </p>
        </a-card>
      </a-col>
      <a-col :span="8" v-for="(feature, index) in features" :key="index">
        <a-card :title="feature.title" class="feature-card">
          <template #cover>
            <div class="feature-icon">
              <component :is="feature.icon" :style="{ fontSize: '32px' }" />
            </div>
          </template>
          <p>{{ feature.description }}</p>
          <a-button type="primary" @click="$router.push(feature.route)">
            开始使用
          </a-button>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script lang="ts" setup>
import {
  FileTextOutlined,
  CodeOutlined,
  BuildOutlined,
  BugOutlined,
  RocketOutlined,
  AppstoreOutlined,
} from "@ant-design/icons-vue";

const features = [
  {
    title: "需求管理",
    description: "使用AI辅助分析和管理项目需求，自动生成需求文档。",
    icon: FileTextOutlined,
    route: "/requirements",
  },
  {
    title: "架构设计",
    description: "智能推荐系统架构，自动生成数据库设计方案。",
    icon: AppstoreOutlined,
    route: "/architecture",
  },
  {
    title: "代码生成",
    description: "基于需求自动生成代码，提供代码优化建议。",
    icon: CodeOutlined,
    route: "/code",
  },
  {
    title: "测试管理",
    description: "自动生成测试用例，执行自动化测试。",
    icon: BugOutlined,
    route: "/testing",
  },
  {
    title: "部署管理",
    description: "自动化部署流程，监控系统运行状态。",
    icon: RocketOutlined,
    route: "/deployment",
  },
  {
    title: "项目概览",
    description: "实时查看项目进度和质量指标。",
    icon: BuildOutlined,
    route: "/dashboard",
  },
];
</script>

<style scoped>
.home {
  padding: 24px;
}
.feature-card {
  height: 100%;
  text-align: center;
}
.feature-icon {
  padding: 24px;
  background: #fafafa;
  text-align: center;
}
h1 {
  text-align: center;
  margin-bottom: 16px;
}
p {
  margin-bottom: 16px;
}
</style>
