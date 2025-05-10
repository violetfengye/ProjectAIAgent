import request from '@/utils/request'

export interface TestTask {
  id: number
  name: string
  description: string
  type: string
  framework: string
  status: string
  createdAt: string
}

export interface CreateTestTaskParams {
  name: string
  description: string
  type: string
  framework: string
}

export interface TestCase {
  id: number
  name: string
  description: string
  steps: string[]
  expectedResult: string
  status: string
}

export interface TestReport {
  id: number
  taskId: number
  totalCases: number
  passedCases: number
  failedCases: number
  executionTime: string
  createdAt: string
  details: {
    caseId: number
    caseName: string
    status: string
    executionTime: string
    errorMessage?: string
  }[]
}

// 获取测试任务列表
export function getTestTasks() {
  return request<TestTask[]>({
    url: '/api/testing/tasks',
    method: 'get',
  })
}

// 创建测试任务
export function createTestTask(data: CreateTestTaskParams) {
  return request<TestTask>({
    url: '/api/testing/tasks',
    method: 'post',
    data,
  })
}

// 删除测试任务
export function deleteTestTask(id: number) {
  return request({
    url: `/api/testing/tasks/${id}`,
    method: 'delete',
  })
}

// 获取测试用例列表
export function getTestCases(taskId: number) {
  return request<TestCase[]>({
    url: `/api/testing/tasks/${taskId}/cases`,
    method: 'get',
  })
}

// 执行测试
export function runTest(taskId: number) {
  return request<TestReport>({
    url: `/api/testing/tasks/${taskId}/run`,
    method: 'post',
  })
}

// 获取测试报告
export function getTestReport(taskId: number) {
  return request<TestReport>({
    url: `/api/testing/tasks/${taskId}/report`,
    method: 'get',
  })
}
