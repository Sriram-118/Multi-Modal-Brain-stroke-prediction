/**
 * TypeScript type definitions for Stroke Prediction Application
 */

// Clinical data interface matching Django form fields
export interface ClinicalData {
  gender: string;        // t1 field
  age: number;          // t2 field  
  hypertension: number; // t3 field (0 or 1)
  glucose: number;      // t4 field
  bmi: number;          // t5 field
  smoking: string;      // t6 field
  image?: File;         // t7 field
}

// Prediction result interface
export interface PredictionResult {
  clinicalPrediction: string;
  imagePrediction: string;
  normalScore: number;
  strokeScore: number;
  chartData?: ChartData;
}

// Chart data interface
export interface ChartData {
  labels: string[];
  datasets: ChartDataset[];
}

export interface ChartDataset {
  label: string;
  data: number[];
  backgroundColor?: string | string[];
  borderColor?: string | string[];
  borderWidth?: number;
}

// Form validation interfaces
export interface ValidationState {
  isValid: boolean;
  errors: Map<string, string>;
  touched: Set<string>;
  submitted: boolean;
}

export interface ValidationRule {
  required?: boolean;
  min?: number;
  max?: number;
  pattern?: RegExp;
  custom?: (value: any) => ValidationResult;
}

export interface ValidationResult {
  isValid: boolean;
  message?: string;
}

// Loading state interface
export interface LoadingState {
  isLoading: boolean;
  operation: string;
  progress?: number;
}

// File upload interface
export interface FileUploadConfig {
  allowedTypes: string[];
  maxSize: number;
  multiple?: boolean;
}

// Chart configuration interface
export interface ChartConfig {
  type: 'bar' | 'line' | 'pie' | 'doughnut' | 'scatter';
  responsive?: boolean;
  maintainAspectRatio?: boolean;
  plugins?: {
    legend?: any;
    title?: any;
    tooltip?: any;
  };
  scales?: any;
  animation?: any;
}

// API response interface
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// Model performance metrics
export interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  fscore: number;
}

export interface AlgorithmMetrics {
  [algorithmName: string]: ModelMetrics;
}

// User interface
export interface User {
  username: string;
  email?: string;
  isAuthenticated: boolean;
}

// Navigation item interface
export interface NavigationItem {
  label: string;
  url: string;
  icon?: string;
  active?: boolean;
  requiresAuth?: boolean;
}

// Theme interface
export interface Theme {
  primary: string;
  secondary: string;
  success: string;
  danger: string;
  warning: string;
  info: string;
  light: string;
  dark: string;
}

// Event handler types
export type EventHandler<T = Event> = (event: T) => void;
export type FormEventHandler = EventHandler<Event>;
export type ChangeEventHandler = EventHandler<Event>;
export type ClickEventHandler = EventHandler<MouseEvent>;

// Utility types
export type Nullable<T> = T | null;
export type Optional<T> = T | undefined;
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// DOM element types
export type HTMLFormElement = HTMLFormElement;
export type HTMLInputElement = HTMLInputElement;
export type HTMLSelectElement = HTMLSelectElement;
export type HTMLTextAreaElement = HTMLTextAreaElement;
export type FormElement = HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement;

// Chart.js type extensions
declare global {
  interface Window {
    StrokeApp: {
      FormValidator: any;
      LoadingManager: any;
      FileUploadHandler: any;
      PredictionChart: any;
      ChartThemeManager: any;
      chartManager: any;
    };
    Chart: any;
    bootstrap: any;
  }
}