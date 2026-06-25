export interface Document {
  id: string;
  filename: string;
  processed: boolean;
  indexed: boolean;
  upload_date?: string;
  processed_at?: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ATSAnalysis {
  ats_score: number;
  score_breakdown: Record<string, number>;
  missing_sections: string[];
  improvements: string[];
}

export interface SkillGap {
  existing_skills: string[];
  missing_skills: string[];
  recommended_skills: string[];
}

export interface InterviewQuestion {
  question: string;
  expected_answer: string;
  evaluation_criteria: string[];
  difficulty: string;
  category: string;
}

export interface MockInterview {
  introduction: string;
  questions: InterviewQuestion[];
  preparation_tips: string[];
}

export interface JobMatch {
  match_score: number;
  matching_skills: string[];
  missing_skills: string[];
  recommendations: string[];
}

export interface JobRecommendation {
  role: string;
  match: number;
  reason: string;
}

export interface Milestone {
  month: string;
  focus: string;
  topics: string[];
}

export interface CareerRoadmap {
  target_role: string;
  recommended_skills: string[];
  milestones: Milestone[];
}

export interface JobCompare {
  matched_skills: string[];
  missing_skills: string[];
  improvement_areas: string[];
}
