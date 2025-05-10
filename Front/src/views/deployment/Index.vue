<template>
  <div class="deployment">
    <a-page-header title="部署管理" sub-title="使用AI辅助进行应用部署和配置">
      <template #extra>
        <a-button type="primary" @click="showCreateModal">
          新建部署任务
        </a-button>
      </template>
    </a-page-header>

    <a-card style="margin-top: 16px">
      <a-table :columns="columns" :data-source="deployments" :loading="loading">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-tag :color="getStatusColor(record.status)">
              {{ record.status }}
            </a-tag>
          </template>
          <template v-if="column.key === 'action'">
            <a-space>
              <a @click="viewDetails(record)">查看详情</a>
              <a @click="startDeploy(record)">开始部署</a>
              <a @click="rollback(record)">回滚</a>
              <a-popconfirm
                title="确定要删除这个部署任务吗？"
                @confirm="deleteDeployment(record)"
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
        <a-form-item label="部署名称" name="name">
          <a-input v-model:value="formState.name" />
        </a-form-item>
        <a-form-item label="部署描述" name="description">
          <a-textarea
            v-model:value="formState.description"
            :rows="4"
            placeholder="请描述部署需求，AI将协助生成部署配置"
          />
        </a-form-item>
        <a-form-item label="部署环境" name="environment">
          <a-select v-model:value="formState.environment">
            <a-select-option value="development">开发环境</a-select-option>
            <a-select-option value="staging">预发布环境</a-select-option>
            <a-select-option value="production">生产环境</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="部署方式" name="deployType">
          <a-select v-model:value="formState.deployType">
            <a-select-option value="docker">Docker容器</a-select-option>
            <a-select-option value="kubernetes">Kubernetes集群</a-select-option>
            <a-select-option value="serverless">Serverless</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>

    <a-modal
      v-model:visible="detailsModalVisible"
      title="部署详情"
      width="800px"
    >
      <div v-if="currentDeployment">
        <a-descriptions bordered>
          <a-descriptions-item label="部署名称">
            {{ currentDeployment.name }}
          </a-descriptions-item>
          <a-descriptions-item label="部署描述">
            {{ currentDeployment.description }}
          </a-descriptions-item>
          <a-descriptions-item label="部署环境">
            {{ currentDeployment.environment }}
          </a-descriptions-item>
          <a-descriptions-item label="部署方式">
            {{ currentDeployment.deployType }}
          </a-descriptions-item>
          <a-descriptions-item label="状态">
            <a-tag :color="getStatusColor(currentDeployment.status)">
              {{ currentDeployment.status }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="创建时间">
            {{ currentDeployment.createdAt }}
          </a-descriptions-item>
        </a-descriptions>

        <div v-if="currentDeployment.logs" style="margin-top: 16px">
          <h3>部署日志</h3>
          <pre style="background: #f5f5f5; padding: 16px; border-radius: 4px">
            {{ currentDeployment.logs }}
          </pre>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from "vue";
import type { FormInstance } from "ant-design-vue";
import { message } from "ant-design-vue";
import {
  getDeployments,
  createDeployment,
  deleteDeployment,
  getDeploymentDetails,
  startDeployment,
  rollbackDeployment,
  type Deployment,
} from "@/api/deployment";

interface Deployment {
  id: number;
  name: string;
  description: string;
  environment: string;
  deployType: string;
  status: string;
  createdAt: string;
  logs?: string;
}

const columns = [
  {
    title: "部署名称",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "部署环境",
    dataIndex: "environment",
    key: "environment",
  },
  {
    title: "部署方式",
    dataIndex: "deployType",
    key: "deployType",
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

const deployments = ref<Deployment[]>([]);
const loading = ref(false);
const modalVisible = ref(false);
const modalTitle = ref("新建部署任务");
const formRef = ref<FormInstance>();

const detailsModalVisible = ref(false);
const currentDeployment = ref<Deployment | null>(null);

const formState = reactive({
  name: "",
  description: "",
  environment: "",
  deployType: "",
});

const rules = {
  name: [{ required: true, message: "请输入部署名称" }],
  description: [{ required: true, message: "请输入部署描述" }],
  environment: [{ required: true, message: "请选择部署环境" }],
  deployType: [{ required: true, message: "请选择部署方式" }],
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

const fetchDeployments = async () => {
  loading.value = true;
  try {
    const data = await getDeployments();
    deployments.value = data;
  } catch (error) {
    message.error("获取部署列表失败");
  } finally {
    loading.value = false;
  }
};

const showCreateModal = () => {
  modalTitle.value = "新建部署任务";
  modalVisible.value = true;
};

const handleModalOk = async () => {
  try {
    await formRef.value?.validate();
    await createDeployment(formState);
    message.success("创建部署任务成功");
    modalVisible.value = false;
    fetchDeployments();
  } catch (error) {
    console.error("Validation failed:", error);
    message.error("创建部署任务失败");
  }
};

const viewDetails = async (record: Deployment) => {
  try {
    const data = await getDeploymentDetails(record.id);
    currentDeployment.value = data;
    detailsModalVisible.value = true;
  } catch (error) {
    message.error("获取部署详情失败");
  }
};

const startDeploy = async (record: Deployment) => {
  try {
    await startDeployment(record.id);
    message.success("开始部署");
    fetchDeployments();
  } catch (error) {
    message.error("部署失败");
  }
};

const rollback = async (record: Deployment) => {
  try {
    await rollbackDeployment(record.id);
    message.success("回滚成功");
    fetchDeployments();
  } catch (error) {
    message.error("回滚失败");
  }
};

const deleteDeployment = async (record: Deployment) => {
  try {
    await deleteDeployment(record.id);
    message.success("删除部署任务成功");
    fetchDeployments();
  } catch (error) {
    message.error("删除部署任务失败");
  }
};

onMounted(() => {
  fetchDeployments();
});
</script>

<style scoped>
.deployment {
  padding: 24px;
}
</style>
