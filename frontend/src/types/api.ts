export type User = {
  id: string;
  email: string;
  name: string;
  role: "USER" | "ADMIN";
  is_active: boolean;
};

export type PlantSpecies = { id: string; name: string; name_en: string };

export type Plant = {
  id: string;
  name: string;
  species: string;
  variety?: string;
  started_at?: string;
  location?: string;
  notes?: string;
  status: string;
};

export type Diagnosis = {
  id: string;
  status: string;
  message?: string;
  confidence: number;
  model: { name: string; version: string };
  plant: { name: string; name_vi: string };
  disease: { code: string; name: string; name_vi: string };
  prediction: {
    status: string;
    confidence: number;
    top_predictions: Array<{ class: string; confidence: number }>;
  } | null;
  symptoms?: string;
  cause?: string;
  prevention?: string;
  recommendation: string;
  health_assessment?: {
    status: string;
    risk: "none" | "low" | "medium" | "high" | "unassessed";
    confidence: number;
    scope: string;
  };
  explainability?: { available: boolean; heatmap?: string; method?: string };
  created_at?: string;
};

export type Dashboard = {
  total_plants: number;
  total_predictions: number;
  healthy_plants: number;
  diseased_plants: number;
  recent_diagnoses: Diagnosis[];
  class_distribution: Record<string, number>;
};
