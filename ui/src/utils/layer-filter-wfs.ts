import WFS from "ol/format/WFS";
import { addProjection, get as getProjection } from "ol/proj";
import Projection from "ol/proj/Projection";
import CqlParser from "geostyler-cql-parser";
import {
  and,
  bbox,
  equalTo,
  greaterThan,
  greaterThanOrEqualTo,
  like,
  isNull,
  lessThan,
  lessThanOrEqualTo,
  not,
  notEqualTo,
  or,
} from "ol/format/filter";
import type Filter from "ol/format/filter/Filter";
import { ELayerFilterSource, EPanelFilterOperator } from "@/types/mapStore";
import type { ILayerFilters, IPanelFilterValue } from "@/types/mapStore";

type IComparisonFilterFactory = (propertyName: string, value: string | number) => Filter;

interface IInExpressionListPredicate {
  type: "InExpressionListPredicate";
  left: string;
  right: Array<string | number>;
  hasNot: boolean | null;
}

interface ILikePredicate {
  type: "LikePredicate";
  left: string;
  right: string;
  hasNot: boolean | null;
}

const cqlParser = new CqlParser();

/**
 * Registers the RD New projection when a spatial filter needs to serialize a geometry.
 * @returns Nothing.
 */
const ensureRdProjection = (): void => {
  if (!getProjection("EPSG:28992")) {
    addProjection(new Projection({ code: "EPSG:28992", units: "m" }));
  }
};

/**
 * Determines whether a feature property uses a text type.
 * @param type - The DescribeFeatureType local type.
 * @returns Whether empty strings have to be considered alongside null values.
 */
const isTextType = (type?: string): boolean => !type || type.toLowerCase().replace(/^(xsd|xs):/, "") === "string";

const comparisonFilterFactories: Partial<Record<EPanelFilterOperator, IComparisonFilterFactory>> = {
  [EPanelFilterOperator.Equals]: equalTo,
  [EPanelFilterOperator.NotEquals]: notEqualTo,
  [EPanelFilterOperator.GreaterThan]: greaterThan as unknown as IComparisonFilterFactory,
  [EPanelFilterOperator.GreaterThanOrEqual]: greaterThanOrEqualTo as unknown as IComparisonFilterFactory,
  [EPanelFilterOperator.LessThan]: lessThan as unknown as IComparisonFilterFactory,
  [EPanelFilterOperator.LessThanOrEqual]: lessThanOrEqualTo as unknown as IComparisonFilterFactory,
};

const geoStylerComparisonFilterFactories: Partial<Record<string, IComparisonFilterFactory>> = {
  "<": lessThan as unknown as IComparisonFilterFactory,
  "<=": lessThanOrEqualTo as unknown as IComparisonFilterFactory,
  ">": greaterThan as unknown as IComparisonFilterFactory,
  ">=": greaterThanOrEqualTo as unknown as IComparisonFilterFactory,
};

/**
 * Creates an OpenLayers filter for a single panel filter value.
 * @param propertyName - The feature property to filter.
 * @param filterValue - The selected operator, values, and property type.
 * @returns An OpenLayers filter, or null when the value is incomplete.
 */
const getPanelFilter = (propertyName: string, filterValue: IPanelFilterValue): Filter | null => {
  if (filterValue.operator === EPanelFilterOperator.Empty) {
    const nullFilter = isNull(propertyName);
    return isTextType(filterValue.type) ? or(nullFilter, equalTo(propertyName, "")) : nullFilter;
  }

  if (filterValue.operator === EPanelFilterOperator.NotEmpty) {
    const notNullFilter = not(isNull(propertyName));
    return isTextType(filterValue.type) ? and(notNullFilter, notEqualTo(propertyName, "")) : notNullFilter;
  }

  const filterFactory = comparisonFilterFactories[filterValue.operator];
  const values = filterValue.values.filter((value) => value !== "");
  if (!filterFactory || values.length === 0) return null;

  const comparisons = values.map((value) => filterFactory(propertyName, value));
  if (comparisons.length === 1) return comparisons[0];

  return filterValue.operator === EPanelFilterOperator.NotEquals ? and(...comparisons) : or(...comparisons);
};

/**
 * Creates a case-insensitive wildcard filter for the table search value.
 * @param searchProperties - The text properties that are searchable.
 * @param searchValue - The text entered by the user.
 * @returns An OpenLayers filter, or null when no search is active.
 */
const getSearchFilter = (searchProperties: string[], searchValue: string): Filter | null => {
  if (!searchValue || searchProperties.length === 0) return null;

  const filters = searchProperties.map((propertyName) => like(propertyName, `*${searchValue}*`, "*", ".", "!", false));
  return filters.length === 1 ? filters[0] : or(...filters);
};

/**
 * Combines filters using a logical AND while avoiding invalid single-child AND expressions.
 * @param filters - The filter expressions to combine.
 * @returns The combined filter, a single input filter, or null for no filters.
 */
const combineFilters = (filters: Filter[]): Filter | null => {
  if (filters.length === 0) return null;
  return filters.length === 1 ? filters[0] : and(...filters);
};

/**
 * Checks whether a GeoStyler parser value represents a CQL IN predicate.
 * @param value - The parsed GeoStyler filter value.
 * @returns Whether the value is an IN predicate.
 */
const isInExpressionListPredicate = (value: unknown): value is IInExpressionListPredicate =>
  typeof value === "object" && value !== null && (value as { type?: string }).type === "InExpressionListPredicate";

/**
 * Checks whether a GeoStyler parser value represents a CQL LIKE predicate.
 * @param value - The parsed GeoStyler filter value.
 * @returns Whether the value is a LIKE predicate.
 */
const isLikePredicate = (value: unknown): value is ILikePredicate =>
  typeof value === "object" && value !== null && (value as { type?: string }).type === "LikePredicate";

/**
 * Converts a CQL LIKE pattern to the wildcard syntax expected by OpenLayers.
 * @param value - The CQL LIKE pattern.
 * @returns The escaped OpenLayers wildcard pattern.
 */
const getCqlLikePattern = (value: string): string =>
  value.replace(/!/g, "!!").replace(/\*/g, "!*").replace(/\./g, "!.").replace(/%/g, "*").replace(/_/g, ".");

/**
 * Converts a GeoStyler CQL parser AST node to an OpenLayers filter.
 * @param filter - The parsed GeoStyler filter node.
 * @param matchCase - Whether LIKE comparisons are case-sensitive.
 * @returns An OpenLayers filter, or null for unsupported AST nodes.
 */
const getGeoStylerFilter = (filter: unknown, matchCase = true): Filter | null => {
  if (isInExpressionListPredicate(filter)) {
    const comparisons = filter.right.map((value) => equalTo(filter.left, value));
    const inFilter = comparisons.length === 1 ? comparisons[0] : or(...comparisons);
    return filter.hasNot ? not(inFilter) : inFilter;
  }

  if (isLikePredicate(filter)) {
    const likeFilter = like(filter.left, getCqlLikePattern(filter.right), "*", ".", "!", matchCase);
    return filter.hasNot ? not(likeFilter) : likeFilter;
  }

  if (!Array.isArray(filter) || typeof filter[0] !== "string") return null;

  const [operator, propertyName, value] = filter;
  if (operator === "&&" || operator === "||") {
    const filters = filter
      .slice(1)
      .map((child) => getGeoStylerFilter(child, matchCase))
      .filter((child): child is Filter => !!child);
    if (filters.length === 0) return null;
    return operator === "&&" ? combineFilters(filters) : filters.length === 1 ? filters[0] : or(...filters);
  }

  if (operator === "!") {
    const child = getGeoStylerFilter(propertyName, matchCase);
    return child ? not(child) : null;
  }

  if (typeof propertyName !== "string") return null;
  if (operator === "==") {
    return value === null ? isNull(propertyName) : equalTo(propertyName, value as string | number);
  }
  if (operator === "!=" || operator === "<>") {
    return value === null ? not(isNull(propertyName)) : notEqualTo(propertyName, value as string | number);
  }
  if (operator === "*=" && typeof value === "string") {
    return like(propertyName, getCqlLikePattern(value), "*", ".", "!", matchCase);
  }

  const filterFactory = geoStylerComparisonFilterFactories[operator];
  return filterFactory && (typeof value === "string" || typeof value === "number")
    ? filterFactory(propertyName, value)
    : null;
};

/**
 * Parses a GeoServer legend CQL expression and converts it to an OpenLayers filter.
 * @param cqlFilter - The CQL expression returned in a legend rule.
 * @returns An OpenLayers filter, or null when the expression is unsupported.
 */
const getLegendFilter = (cqlFilter: string): Filter | null => {
  const normalizedCql = cqlFilter.trim().replace(/^\[([\s\S]*)\]$/, "$1");
  const isCaseInsensitive = /\bILIKE\b/i.test(normalizedCql);
  const parsedFilter = cqlParser.read(normalizedCql.replace(/\bILIKE\b/gi, "LIKE"));
  return getGeoStylerFilter(parsedFilter, !isCaseInsensitive);
};

/**
 * Builds a composable OpenLayers filter from the active layer, map extent, and extra filters.
 * @param layerFilters - All active map-layer filters.
 * @param layerId - The layer whose filters should be used.
 * @param extent - Optional viewport extent for a BBOX filter.
 * @param additionalFilters - Additional spatial or temporal filters for the request.
 * @returns A combined OpenLayers filter, or null when no filter is active.
 */
export const getLayerFilterExpression = (
  layerFilters: ILayerFilters,
  layerId: string,
  extent?: number[],
  additionalFilters: Filter[] = [],
): Filter | null => {
  const filters = [...additionalFilters];
  if (extent) filters.unshift(bbox("geom", extent, "EPSG:28992"));

  const layerFilter = layerFilters[layerId];
  if (!layerFilter) return combineFilters(filters);

  if (layerFilter.source === ELayerFilterSource.Legend) {
    const legendFilters = (layerFilter.legendFilters ?? [])
      .map(getLegendFilter)
      .filter((filter): filter is Filter => filter !== null);
    if (legendFilters.length > 0) {
      filters.push(legendFilters.length === 1 ? legendFilters[0] : or(...legendFilters));
    }
    return combineFilters(filters);
  }

  filters.push(
    ...Object.entries(layerFilter.filters ?? {})
      .map(([propertyName, filterValue]) => getPanelFilter(propertyName, filterValue))
      .filter((filter): filter is Filter => filter !== null),
  );
  const searchFilter = getSearchFilter(layerFilter.searchProperties ?? [], layerFilter.searchValue ?? "");
  if (searchFilter) filters.push(searchFilter);

  return combineFilters(filters);
};

/**
 * Serializes the active layer filters as a WFS 2.0 Filter Encoding XML value.
 * @param layerFilters - All active map-layer filters.
 * @param layerId - The layer whose filters should be used.
 * @param extent - Optional viewport extent for a BBOX filter.
 * @param additionalFilters - Additional spatial or temporal filters for the request.
 * @returns The XML FILTER parameter value, or null when no filter is active.
 */
export const getLayerFilter = (
  layerFilters: ILayerFilters,
  layerId: string,
  extent?: number[],
  additionalFilters: Filter[] = [],
): string | null => {
  const filter = getLayerFilterExpression(layerFilters, layerId, extent, additionalFilters);
  ensureRdProjection();
  if (!filter) return null;

  const request = new WFS({ version: "2.0.0" }).writeGetFeature({
    featureTypes: ["layer"],
    featureNS: "urn:atlas:filter",
    featurePrefix: "atlas",
    filter: filter,
    srsName: "EPSG:28992",
  });
  const filterElement = (request as Document).getElementsByTagNameNS("http://www.opengis.net/fes/2.0", "Filter")[0];
  if (!filterElement) return null;
  return new XMLSerializer().serializeToString(filterElement);
};
