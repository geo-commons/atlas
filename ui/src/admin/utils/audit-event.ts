export interface IAuditActionIndicator {
  label: string;
  severity: "success" | "danger" | "info";
  icon: string;
}

export interface IAuditDetail {
  field?: string;
  oldValue?: string;
  newValue?: string;
  value?: string;
}

export interface IAuditValueDisplay {
  isJson: boolean;
  value: string;
}

export const getAuditActionIndicator = (actionId: string): IAuditActionIndicator => {
  if (actionId === "+") {
    return { label: "Toegevoegd", severity: "success", icon: "pi pi-plus" };
  }

  if (actionId === "-") {
    return { label: "Verwijderd", severity: "danger", icon: "pi pi-trash" };
  }

  return { label: "Gewijzigd", severity: "info", icon: "pi pi-pencil" };
};

export const getAuditValueDisplay = (value: string): IAuditValueDisplay => {
  const trimmedValue = value.trim();
  if (!(trimmedValue.startsWith("{") || trimmedValue.startsWith("["))) {
    return { isJson: false, value };
  }

  try {
    return { isJson: true, value: JSON.stringify(JSON.parse(trimmedValue), null, 2) };
  } catch {
    try {
      const pythonStyleJson = trimmedValue
        .replaceAll("'", '"')
        .replace(/\bTrue\b/g, "true")
        .replace(/\bFalse\b/g, "false")
        .replace(/\bNone\b/g, "null");
      return { isJson: true, value: JSON.stringify(JSON.parse(pythonStyleJson), null, 2) };
    } catch {
      return { isJson: false, value };
    }
  }
};
