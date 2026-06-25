import axios from 'axios';
import type { 
  Document, 
  ChatMessage, 
  ATSAnalysis, 
  SkillGap, 
  InterviewQuestion, 
  MockInterview,
  JobMatch,
  JobRecommendation,
  CareerRoadmap,
  JobCompare
} from '../types';

const BASE_URL = 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Document Service
export const documentService = {
  uploadDocument: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },
  getDocuments: async (): Promise<Document[]> => {
    const res = await api.get('/documents');
    return res.data.data;
  },
  processDocument: async (id: string) => {
    const res = await api.post(`/documents/${id}/process`);
    return res.data;
  },
  deleteDocument: async (id: string) => {
    const res = await api.delete(`/documents/${id}`);
    return res.data;
  },
  createIndex: async (id: string) => {
    const res = await api.post(`/documents/${id}/index`);
    return res.data;
  }
};

// Chat Service
export const chatService = {
  ragChat: async (docId: string, query: string) => {
    const res = await api.post('/rag/query', { document_id: docId, query });
    return res.data;
  }
};

// Resume Service
export const resumeService = {
  getAtsScore: async (docId: string): Promise<ATSAnalysis> => {
    const res = await api.post('/resume/ats-score', { document_id: docId });
    return res.data.data;
  },
  getSkillGap: async (docId: string, target_role: string = "Software Engineer"): Promise<SkillGap> => {
    const res = await api.post('/resume/skill-gap', { document_id: docId, target_role });
    return res.data.data;
  }
};

// Interview Service
export const interviewService = {
  generateMock: async (docId: string, role: string): Promise<MockInterview> => {
    const res = await api.post('/interview/mock', { document_id: docId, role });
    return res.data.data;
  }
};

// Job Service
export const jobService = {
  matchJob: async (docId: string, jd: string): Promise<JobMatch> => {
    const res = await api.post('/job/match', { document_id: docId, job_description: jd });
    return res.data.data;
  },
  recommendJobs: async (docId: string): Promise<JobRecommendation[]> => {
    const res = await api.post('/job/recommend', { document_id: docId });
    return res.data.data;
  },
  generateRoadmap: async (docId: string, role: string): Promise<CareerRoadmap> => {
    const res = await api.post('/job/roadmap', { document_id: docId, target_role: role });
    return res.data.data;
  },
  compareJob: async (docId: string, jd: string): Promise<JobCompare> => {
    const res = await api.post('/job/compare', { document_id: docId, job_description: jd });
    return res.data.data;
  }
};
