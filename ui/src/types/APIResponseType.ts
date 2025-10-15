/**
 * Generic API response type for paginated results
 */
export interface APIResponseType<T> {
  results: T[];
  count: number;
  next: string | null;
  previous: string | null;
}