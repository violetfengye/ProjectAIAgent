import request from "@/utils/request";

export interface Deployment {
  id: number;
  name: string;
  description: string;
  environment: string;
  deployType: string;
  status: string;
  createdAt: string;
  logs?: string;
}

export interface CreateDeploymentParams {
  name: string;
  description: string;
  environment: string;
  deployType: string;
}

// 获取部署任务列表
export function getDeployments() {
  return request<Deployment[]>({
    url: "/api/deployments",
    method: "get",
  });
}

// 创建部署任务
export function createDeployment(data: CreateDeploymentParams) {
  return request<Deployment>({
    url: "/api/deployments",
    method: "post",
    data,
  });
}

// 删除部署任务
export function deleteDeployment(id: number) {
  return request({
    url: `/api/deployments/${id}`,
    method: "delete",
  });
}

// 获取部署详情
export function getDeploymentDetails(id: number) {
  return request<Deployment>({
    url: `/api/deployments/${id}`,
    method: "get",
  });
}

// 开始部署
export function startDeployment(id: number) {
  return request<Deployment>({
    url: `/api/deployments/${id}/start`,
    method: "post",
  });
}

// 回滚部署
export function rollbackDeployment(id: number) {
  return request<Deployment>({
    url: `/api/deployments/${id}/rollback`,
    method: "post",
  });
}
