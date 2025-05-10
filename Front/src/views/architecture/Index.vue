<template>
  <div class="architecture">
    <a-page-header title="架构设计" sub-title="使用AI辅助进行系统架构设计">
      <template #extra>
        <a-button type="primary" @click="showCreateModal">
          新建架构设计
        </a-button>
      </template>
    </a-page-header>

    <a-card style="margin-top: 16px">
      <a-table
        :columns="columns"
        :data-source="architectures"
        :loading="loading"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <a @click="editArchitecture(record)">编辑</a>
              <a @click="viewArchitecture(record)">查看</a>
              <a-popconfirm
                title="确定要删除这个架构设计吗？"
                @confirm="deleteArchitecture(record)"
              >
                <a>删除</a>
              </a-popconfirm>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <a-modal
      v-model:visible="modalVisible"
      :title="modalTitle"
      @ok="handleModalOk"
      width="800px"
    >
      <a-form :model="formState" :rules="rules" ref="formRef">
        <a-form-item label="架构名称" name="name">
          <a-input v-model:value="formState.name" />
        </a-form-item>
        <a-form-item label="架构描述" name="description">
          <a-textarea
            v-model:value="formState.description"
            :rows="4"
            placeholder="请输入架构描述，AI将协助分析并提供建议"
          />
        </a-form-item>
        <a-form-item label="技术栈" name="techStack">
          <a-select
            v-model:value="formState.techStack"
            mode="multiple"
            placeholder="请选择技术栈"
          >
            <a-select-option value="vue">Vue.js</a-select-option>
            <a-select-option value="react">React</a-select-option>
            <a-select-option value="django">Django</a-select-option>
            <a-select-option value="spring">Spring Boot</a-select-option>
            <a-select-option value="mysql">MySQL</a-select-option>
            <a-select-option value="postgresql">PostgreSQL</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from "vue";
import type { FormInstance } from "ant-design-vue";

interface Architecture {
  id: number;
  name: string;
  description: string;
  techStack: string[];
  createdAt: string;
}

const columns = [
  {
    title: "名称",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "技术栈",
    dataIndex: "techStack",
    key: "techStack",
  },
  {
    title: "创建时间",
    dataIndex: "createdAt",
    key: "createdAt",
  },
  {
    title: "操作",
    key: "action",
  },
];

const architectures = ref<Architecture[]>([
  {
    id: 1,
    name: "前后端分离架构",
    description: "使用Vue.js + Django + PostgreSQL的现代Web应用架构",
    techStack: ["vue", "django", "postgresql"],
    createdAt: "2024-03-31",
  },
]);

const loading = ref(false);
const modalVisible = ref(false);
const modalTitle = ref("新建架构设计");
const formRef = ref<FormInstance>();

const formState = reactive({
  name: "",
  description: "",
  techStack: [],
});

const rules = {
  name: [{ required: true, message: "请输入架构名称" }],
  description: [{ required: true, message: "请输入架构描述" }],
  techStack: [{ required: true, message: "请选择技术栈" }],
};

const showCreateModal = () => {
  modalTitle.value = "新建架构设计";
  modalVisible.value = true;
};

const handleModalOk = async () => {
  try {
    await formRef.value?.validate();
    // TODO: 调用API保存架构设计
    modalVisible.value = false;
  } catch (error) {
    console.error("Validation failed:", error);
  }
};

const editArchitecture = (record: Architecture) => {
  modalTitle.value = "编辑架构设计";
  formState.name = record.name;
  formState.description = record.description;
  formState.techStack = record.techStack;
  modalVisible.value = true;
};

const viewArchitecture = (record: Architecture) => {
  // TODO: 实现架构设计详情查看
  console.log("View architecture:", record);
};

const deleteArchitecture = (record: Architecture) => {
  // TODO: 调用API删除架构设计
  console.log("Delete architecture:", record);
};
</script>

<style scoped>
.architecture {
  padding: 24px;
}
</style>
