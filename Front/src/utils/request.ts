import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { message } from 'ant-design-vue'

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 15000,
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 在这里可以添加token等认证信息
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  },
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    const res = response.data
    // 这里可以根据后端的响应结构进行调整
    if (res.code === 0) {
      return res.data
    } else {
      message.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message || '请求失败'))
    }
  },
  (error) => {
    console.error('Response error:', error)
    message.error(error.message || '请求失败')
    return Promise.reject(error)
  },
)

// 封装请求方法
function request<T = any>(config: AxiosRequestConfig): Promise<T> {
  return service(config)
}

export default request
