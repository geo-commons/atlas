export enum EDialogTypes {
  Import = "import-dialog",
  Export = "export-dialog",
  ExportAll = "export-all-dialog",
  Create = "create-object-dialog",
}

export type ShowDialogType = { show: boolean; type: EDialogTypes };
