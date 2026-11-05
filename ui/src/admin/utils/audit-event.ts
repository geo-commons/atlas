export interface IAuditActionIndicator {
  label: string;
  severity: "success" | "danger" | "info";
  icon: string;
}

export interface IAuditDetail {
  context?: string;
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

export const getAuditDetails = (details: string): IAuditDetail[] => {
  return details
    .split("\n\n")
    .filter(Boolean)
    .flatMap((detail) => {
      const lines = detail.split("\n");
      const hasRelatedObject = lines[0].endsWith("gewijzigd") && lines.length > 2;
      const context = hasRelatedObject ? `${lines[0].replace(" gewijzigd", "")} · ${lines[1]}` : undefined;
      const changeLines = lines.slice(hasRelatedObject ? 2 : 0);

      const changes: IAuditDetail[] = [];
      for (let index = 0; index + 1 < changeLines.length; index += 2) {
        if (!changeLines[index + 1].includes(" → ")) {
          continue;
        }

        const [oldValue, newValue] = changeLines[index + 1].split(" → ", 2);
        changes.push({ context, field: changeLines[index], oldValue, newValue });
      }

      return changes.length ? changes : [{ context, value: changeLines.join("\n") }];
    });
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
      return { isJson: true, value: JSON.stringify(JSON.parse(trimmedValue.replaceAll("'", '"')), null, 2) };
    } catch {
      return { isJson: false, value };
    }
  }
};
