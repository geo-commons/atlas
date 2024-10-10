export enum EDialogTypes {
  Import = "import-dialog",
  Export = "export-dialog",
  Create = "create-object-dialog",
}

export type ShowDialogType = { show: boolean; type: EDialogTypes };
