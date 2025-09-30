export interface AdminFormQuestion {
  label: string;
  id: string;
  name: string;
  type: string;
  required: boolean;
  visibility?: string;
  infoText?: string;
  maxLength?: number;
  multiLine?: boolean;
  placeholder?: string;
  options?: any[];
  disabled?: boolean;
  showIf?: boolean;
  step?: number;
  rows?: number;
  value?: any;
  uncheckedValue?: any;
  objectDisplayName?: string;
  containsColon?: boolean;
}

export interface AdminFormSection {
  label: string;
  questions: AdminFormQuestion[];
  disableInputs?: boolean;
}

export interface AdminFormConfig {
  [key: string]: AdminFormSection;
}
