import axios from 'axios';
import type {
  VideoSource,
  Task,
  PaginationMeta,
} from '../types';

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
});

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const videoApi = {
  upload: async (file: File): Promise<VideoSource> => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post<VideoSource>('/videos/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  list: async (page = 1, pageSize = 20) => {
    return api.get<{ videos: VideoSource[]; pagination: PaginationMeta }>('/videos', {
      params: { page, page_size: pageSize },
    });
  },

  get: async (id: string): Promise<VideoSource> => {
    return api.get<VideoSource>(`/videos/${id}`);
  },

  delete: async (id: string) => {
    return api.delete<{ deleted_id: string }>(`/videos/${id}`);
  },
};

export const taskApi = {
  create: async (data: {
    name: string;
    task_type: 'realtime' | 'offline';
    input_config: any;
    output_config: any;
    model_settings?: any;
    priority?: number;
  }): Promise<Task> => {
    return api.post<Task>('/tasks', data);
  },

  list: async (page = 1, pageSize = 20, status?: string, taskType?: string) => {
    return api.get<{ tasks: Task[]; pagination: PaginationMeta }>('/tasks', {
      params: { page, page_size: pageSize, status, task_type: taskType },
    });
  },

  get: async (id: string): Promise<Task> => {
    return api.get<Task>(`/tasks/${id}`);
  },

  start: async (id: string) => {
    return api.post<{ task_id: string; status: string; started_at: string }>(`/tasks/${id}/start`);
  },

  stop: async (id: string) => {
    return api.post<{ task_id: string; status: string }>(`/tasks/${id}/stop`);
  },

  delete: async (id: string) => {
    return api.delete<{ deleted_id: string }>(`/tasks/${id}`);
  },

  getOutput: async (id: string) => {
    return api.get<{ output_url: string; output_type: string }>(`/tasks/${id}/output`);
  },
};

export const modelApi = {
  list: async () => {
    return api.get<{ models: any[] }>('/models');
  },

  get: async (name: string) => {
    return api.get<any>(`/models/${name}`);
  },

  getInstances: async () => {
    return api.get<{ instances: any[] }>('/models/instances');
  },
};

export default api;