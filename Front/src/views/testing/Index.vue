<template>
  <div class="testing-container">
    <div class="header">
      <h2>测试管理</h2>
      <a-button type="primary" @click="showCreateModal"> 创建测试任务 </a-button>
    </div>

    <a-table :columns="columns" :data-source="testTasks" :loading="loading" row-key="id">
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'status'">
          <a-tag :color="getStatusColor(record.status)">
            {{ record.status }}
          </a-tag>
        </template>
        <template v-else-if="column.key === 'action'">
          <a-space>
            <a @click="viewDetails(record)">查看详情</a>
            <a @click="runTest(record)">执行测试</a>
            <a-popconfirm title="确定要删除这个测试任务吗？" @confirm="deleteTask(record.id)">
              <a class="danger">删除</a>
            </a-popconfirm>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 创建测试任务对话框 -->
    <a-modal
      v-model:visible="createModalVisible"
      title="创建测试任务"
      @ok="handleCreate"
      :confirm-loading="creating"
    >
      <a-form :model="createForm" :rules="rules" ref="createFormRef" layout="vertical">
        <a-form-item label="任务名称" name="name">
          <a-input v-model:value="createForm.name" placeholder="请输入任务名称" />
        </a-form-item>
        <a-form-item label="描述" name="description">
          <a-textarea
            v-model:value="createForm.description"
            placeholder="请输入任务描述"
            :rows="4"
          />
        </a-form-item>
        <a-form-item label="测试类型" name="type">
          <a-select v-model:value="createForm.type" placeholder="请选择测试类型">
            <a-select-option value="unit">单元测试</a-select-option>
            <a-select-option value="integration">集成测试</a-select-option>
            <a-select-option value="e2e">端到端测试</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="测试框架" name="framework">
          <a-select v-model:value="createForm.framework" placeholder="请选择测试框架">
            <a-select-option value="jest">Jest</a-select-option>
            <a-select-option value="mocha">Mocha</a-select-option>
            <a-select-option value="pytest">PyTest</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 测试详情对话框 -->
    <a-modal v-model:visible="detailsModalVisible" title="测试详情" width="800px" :footer="null">
      <template v-if="currentTask">
        <a-descriptions :column="2">
          <a-descriptions-item label="任务名称">{{ currentTask.name }}</a-descriptions-item>
          <a-descriptions-item label="测试类型">{{ currentTask.type }}</a-descriptions-item>
          <a-descriptions-item label="测试框架">{{ currentTask.framework }}</a-descriptions-item>
          <a-descriptions-item label="状态">
            <a-tag :color="getStatusColor(currentTask.status)">
              {{ currentTask.status }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="创建时间">{{ currentTask.createdAt }}</a-descriptions-item>
          <a-descriptions-item label="描述">{{ currentTask.description }}</a-descriptions-item>
        </a-descriptions>

        <div class="test-cases" v-if="testCases.length">
          <h3>测试用例</h3>
          <a-table :columns="caseColumns" :data-source="testCases" :pagination="false" row-key="id">
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'status'">
                <a-tag :color="getCaseStatusColor(record.status)">
                  {{ record.status }}
                </a-tag>
              </template>
            </template>
          </a-table>
        </div>

        <div class="test-report" v-if="testReport">
          <h3>测试报告</h3>
          <a-descriptions :column="3">
            <a-descriptions-item label="总用例数">{{ testReport.totalCases }}</a-descriptions-item>
            <a-descriptions-item label="通过用例">{{ testReport.passedCases }}</a-descriptions-item>
            <a-descriptions-item label="失败用例">{{ testReport.failedCases }}</a-descriptions-item>
            <a-descriptions-item label="执行时间">{{
              testReport.executionTime
            }}</a-descriptions-item>
            <a-descriptions-item label="执行时间">{{ testReport.createdAt }}</a-descriptions-item>
          </a-descriptions>

          <div class="report-details">
            <h4>详细结果</h4>
            <a-table
              :columns="reportColumns"
              :data-source="testReport.details"
              :pagination="false"
              row-key="caseId"
            >
              <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'status'">
                  <a-tag :color="getCaseStatusColor(record.status)">
                    {{ record.status }}
                  </a-tag>
                </template>
                <template v-else-if="column.key === 'errorMessage'">
                  <a-tooltip :title="record.errorMessage">
                    <span class="error-message">{{ record.errorMessage }}</span>
                  </a-tooltip>
                </template>
              </template>
            </a-table>
          </div>
        </div>
      </template>
    </a-modal>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import type { FormInstance } from 'ant-design-vue'
import {
  getTestTasks,
  createTestTask,
  deleteTestTask,
  getTestCases,
  runTest,
  getTestReport,
  type TestTask,
  type CreateTestTaskParams,
  type TestCase,
  type TestReport,
} from '@/api/testing'

// 表格列定义
const columns = [
  {
    title: '任务名称',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '测试类型',
    dataIndex: 'type',
    key: 'type',
  },
  {
    title: '测试框架',
    dataIndex: 'framework',
    key: 'framework',
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
  },
  {
    title: '创建时间',
    dataIndex: 'createdAt',
    key: 'createdAt',
  },
  {
    title: '操作',
    key: 'action',
  },
]

// 测试用例表格列定义
const caseColumns = [
  {
    title: '用例名称',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '描述',
    dataIndex: 'description',
    key: 'description',
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
  },
]

// 测试报告表格列定义
const reportColumns = [
  {
    title: '用例名称',
    dataIndex: 'caseName',
    key: 'caseName',
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
  },
  {
    title: '执行时间',
    dataIndex: 'executionTime',
    key: 'executionTime',
  },
  {
    title: '错误信息',
    dataIndex: 'errorMessage',
    key: 'errorMessage',
  },
]

// 状态
const loading = ref(false)
const creating = ref(false)
const testTasks = ref<TestTask[]>([])
const testCases = ref<TestCase[]>([])
const testReport = ref<TestReport | null>(null)
const currentTask = ref<TestTask | null>(null)
const createModalVisible = ref(false)
const detailsModalVisible = ref(false)
const createFormRef = ref<FormInstance>()

// 表单数据
const createForm = ref<CreateTestTaskParams>({
  name: '',
  description: '',
  type: '',
  framework: '',
})

// 表单验证规则
const rules = {
  name: [{ required: true, message: '请输入任务名称' }],
  type: [{ required: true, message: '请选择测试类型' }],
  framework: [{ required: true, message: '请选择测试框架' }],
}

// 获取状态颜色
const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    pending: 'default',
    running: 'processing',
    completed: 'success',
    failed: 'error',
  }
  return colors[status] || 'default'
}

// 获取用例状态颜色
const getCaseStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    passed: 'success',
    failed: 'error',
    skipped: 'warning',
  }
  return colors[status] || 'default'
}

// 加载测试任务列表
const loadTestTasks = async () => {
  loading.value = true
  try {
    testTasks.value = await getTestTasks()
  } catch (error) {
    message.error('加载测试任务失败')
  } finally {
    loading.value = false
  }
}

// 显示创建对话框
const showCreateModal = () => {
  createModalVisible.value = true
  createForm.value = {
    name: '',
    description: '',
    type: '',
    framework: '',
  }
}

// 创建测试任务
const handleCreate = async () => {
  try {
    await createFormRef.value?.validate()
    creating.value = true
    await createTestTask(createForm.value)
    message.success('创建成功')
    createModalVisible.value = false
    loadTestTasks()
  } catch (error) {
    message.error('创建失败')
  } finally {
    creating.value = false
  }
}

// 删除测试任务
const deleteTask = async (id: number) => {
  try {
    await deleteTestTask(id)
    message.success('删除成功')
    loadTestTasks()
  } catch (error) {
    message.error('删除失败')
  }
}

// 查看详情
const viewDetails = async (task: TestTask) => {
  currentTask.value = task
  detailsModalVisible.value = true
  try {
    const [cases, report] = await Promise.all([getTestCases(task.id), getTestReport(task.id)])
    testCases.value = cases
    testReport.value = report
  } catch (error) {
    message.error('加载详情失败')
  }
}

// 执行测试
const runTest = async (task: TestTask) => {
  try {
    await runTest(task.id)
    message.success('测试任务已启动')
    loadTestTasks()
  } catch (error) {
    message.error('启动测试失败')
  }
}

onMounted(() => {
  loadTestTasks()
})
</script>

<style scoped>
.testing-container {
  padding: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.test-cases,
.test-report {
  margin-top: 24px;
}

.error-message {
  color: #ff4d4f;
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.danger {
  color: #ff4d4f;
}
</style>
