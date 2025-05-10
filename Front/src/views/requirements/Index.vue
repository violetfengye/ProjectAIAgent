<template>
  <div class="requirements">
    <a-page-header title="需求管理" sub-title="使用AI辅助分析和管理项目需求">
      <template #extra>
        <a-button type="primary" @click="showCreateModal"> 新建需求 </a-button>
      </template>
    </a-page-header>

    <a-card style="margin-top: 16px">
      <a-table
        :columns="columns"
        :data-source="requirements"
        :loading="loading"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-space>
              <a @click="editRequirement(record)">编辑</a>
              <a @click="viewRequirement(record)">查看</a>
              <a-popconfirm
                title="确定要删除这条需求吗？"
                @confirm="deleteRequirement(record)"
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
        <a-form-item label="需求标题" name="title">
          <a-input v-model:value="formState.title" />
        </a-form-item>
        <a-form-item label="需求描述" name="description">
          <a-textarea
            v-model:value="formState.description"
            :rows="4"
            placeholder="请输入需求描述，AI将协助分析并提供建议"
          />
        </a-form-item>
        <a-form-item label="优先级" name="priority">
          <a-select v-model:value="formState.priority">
            <a-select-option value="high">高</a-select-option>
            <a-select-option value="medium">中</a-select-option>
            <a-select-option value="low">低</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from "vue";
import type { FormInstance } from "ant-design-vue";

interface Requirement {
  id: number;
  title: string;
  description: string;
  priority: string;
  status: string;
  createdAt: string;
}

const columns = [
  {
    title: "标题",
    dataIndex: "title",
    key: "title",
  },
  {
    title: "优先级",
    dataIndex: "priority",
    key: "priority",
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

const requirements = ref<Requirement[]>([
  {
    id: 1,
    title: "用户登录功能",
    description: "实现用户登录和认证功能",
    priority: "high",
    status: "进行中",
    createdAt: "2024-03-31",
  },
]);

const loading = ref(false);
const modalVisible = ref(false);
const modalTitle = ref("新建需求");
const formRef = ref<FormInstance>();

const formState = reactive({
  title: "",
  description: "",
  priority: "medium",
});

const rules = {
  title: [{ required: true, message: "请输入需求标题" }],
  description: [{ required: true, message: "请输入需求描述" }],
  priority: [{ required: true, message: "请选择优先级" }],
};

const showCreateModal = () => {
  modalTitle.value = "新建需求";
  modalVisible.value = true;
};

const handleModalOk = async () => {
  try {
    await formRef.value?.validate();
    // TODO: 调用API保存需求
    modalVisible.value = false;
  } catch (error) {
    console.error("Validation failed:", error);
  }
};

const editRequirement = (record: Requirement) => {
  modalTitle.value = "编辑需求";
  formState.title = record.title;
  formState.description = record.description;
  formState.priority = record.priority;
  modalVisible.value = true;
};

const viewRequirement = (record: Requirement) => {
  // TODO: 实现需求详情查看
  console.log("View requirement:", record);
};

const deleteRequirement = (record: Requirement) => {
  // TODO: 调用API删除需求
  console.log("Delete requirement:", record);
};
</script>

<style scoped>
.requirements {
  padding: 24px;
}
</style>
