export type OgcTemporalInterval = [string | null, string | null];

export interface IOgcTemporalExtent {
  interval?: OgcTemporalInterval[];
  trs?: string;
}

export interface IOgcExtent {
  temporal?: IOgcTemporalExtent;
}

export interface IOgcCollection {
  id?: string;
  title?: string;
  extent?: IOgcExtent;
}
