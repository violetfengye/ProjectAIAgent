import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export interface Requirement {
  id: number;
  title: string;
  description: string;
  priority: string;
  status: string;
  createdAt: string;
}

export interface CreateRequirementData {
  title: string;
  description: string;
  priority: string;
}

export const requirementsApi = {
  getAll: async () => {
    const response = await axios.get<Requirement[]>(`${API_URL}/requirements/`);
    return response.data;
  },

  getById: async (id: number) => {
    const response = await axios.get<Requirement>(
      `${API_URL}/requirements/${id}/`
    );
    return response.data;
  },

  create: async (data: CreateRequirementData) => {
    const response = await axios.post<Requirement>(
      `${API_URL}/requirements/`,
      data
    );
    return response.data;
  },

  update: async (id: number, data: Partial<CreateRequirementData>) => {
    const response = await axios.patch<Requirement>(
      `${API_URL}/requirements/${id}/`,
      data
    );
    return response.data;
  },

  delete: async (id: number) => {
    await axios.delete(`${API_URL}/requirements/${id}/`);
  },

  analyzeWithAI: async (description: string) => {
    const response = await axios.post(`${API_URL}/requirements/analyze/`, {
      description,
    });
    return response.data;
  },
};
