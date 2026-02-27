declare module "fetch-dot" {
  export default function fetchDot<TObj extends object, TResult = unknown>(
    notation: string,
    obj: TObj,
  ): TResult | undefined;
}
