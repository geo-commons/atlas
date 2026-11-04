export interface IAuditActionIndicator {
  label: string;
  severity: "success" | "danger" | "info";
  icon: string;
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
