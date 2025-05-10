<template>
  <div class="code">
    <a-page-header title="代码生成" sub-title="使用AI辅助生成和优化代码">
      <template #extra>
        <a-button type="primary" @click="showCreateModal">
          新建代码生成任务
        </a-button>
      </template>
    </a-page-header>

    <a-card style="margin-top: 16px">
      <a-table :columns="columns" :data-source="codeTasks" :loading="loading">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-tag :color="getStatusColor(record.status)">
              {{ record.status }}
            </a-tag>
          </template>
          <template v-if="column.key === 'action'">
            <a-space>
              <a @click="viewCode(record)">查看代码</a>
              <a @click="downloadCode(record)">下载</a>
              <a-popconfirm
                title="确定要删除这个任务吗？"
                @confirm="deleteTask(record)"
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
        <a-form-item label="任务名称" name="name">
          <a-input v-model:value="formState.name" />
        </a-form-item>
        <a-form-item label="代码描述" name="description">
          <a-textarea
            v-model:value="formState.description"
            :rows="4"
            placeholder="请详细描述需要生成的代码功能，AI将根据描述生成相应的代码"
          />
        </a-form-item>
        <a-form-item label="编程语言" name="language">
          <a-select v-model:value="formState.language">
            <a-select-option value="python">Python</a-select-option>
            <a-select-option value="java">Java</a-select-option>
            <a-select-option value="javascript">JavaScript</a-select-option>
            <a-select-option value="typescript">TypeScript</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="框架" name="framework">
          <a-select v-model:value="formState.framework">
            <a-select-option value="django">Django</a-select-option>
            <a-select-option value="spring">Spring Boot</a-select-option>
            <a-select-option value="vue">Vue.js</a-select-option>
            <a-select-option value="react">React</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from "vue";
import type { FormInstance } from "ant-design-vue";

interface CodeTask {
  id: number;
  name: string;
  description: string;
  language: string;
  framework: string;
  status: string;
  createdAt: string;
}

const columns = [
  {
    title: "任务名称",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "编程语言",
    dataIndex: "language",
    key: "language",
  },
  {
    title: "框架",
    dataIndex: "framework",
    key: "framework",
  },
  {
    title: "状态",
    dataIndex: "status",
    key: "status",
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

const codeTasks = ref<CodeTask[]>([
  {
    id: 1,
    name: "用户认证模块",
    description: "生成用户登录、注册、密码重置等功能的代码",
    language: "python",
    framework: "django",
    status: "已完成",
    createdAt: "2024-03-31",
  },
]);

const loading = ref(false);
const modalVisible = ref(false);
const modalTitle = ref("新建代码生成任务");
const formRef = ref<FormInstance>();

const formState = reactive({
  name: "",
  description: "",
  language: "",
  framework: "",
});

const rules = {
  name: [{ required: true, message: "请输入任务名称" }],
  description: [{ required: true, message: "请输入代码描述" }],
  language: [{ required: true, message: "请选择编程语言" }],
  framework: [{ required: true, message: "请选择框架" }],
};

const getStatusColor = (status: string) => {
  switch (status) {
    case "已完成":
      return "success";
    case "进行中":
      return "processing";
    case "失败":
      return "error";
    default:
      return "default";
  }
};

const showCreateModal = () => {
  modalTitle.value = "新建代码生成任务";
  modalVisible.value = true;
};

const handleModalOk = async () => {
  try {
    await formRef.value?.validate();
    // TODO: 调用API创建代码生成任务
    modalVisible.value = false;
  } catch (error) {
    console.error("Validation failed:", error);
  }
};

const viewCode = (record: CodeTask) => {
  // TODO: 实现代码查看功能
  console.log("View code:", record);
};

const downloadCode = (record: CodeTask) => {
  // TODO: 实现代码下载功能
  console.log("Download code:", record);
};

const deleteTask = (record: CodeTask) => {
  // TODO: 调用API删除任务
  console.log("Delete task:", record);
};
</script>

<style scoped>
.code {
  padding: 24px;
}
</style>
