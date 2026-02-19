import type { ComputedRef } from "vue";
import { computed } from "vue";
import defaultMapsThumbnail from "@/assets/images/default_map_thumbnail.png";
import { formatDateValue } from "@/utils/date-formatter";

export enum PortalCardObjectType {
  Map = "map",
  Table = "table",
  Metadataset = "metadataset",
}

export enum LayoutMode {
  Grid = "grid",
  List = "list",
}

export enum SortOrder {
  TitleAsc = "title",
  TitleDesc = "-title",
  LastUpdatedDesc = "-last_updated",
  LastUpdatedAsc = "last_updated",
}

export interface PortalCardProps {
  thumbnail: string | null;
  title: string;
  summary: string | null;
  objectUrl: string;
  objectType: PortalCardObjectType;
  showThumbnail: boolean;
  lastUpdated: string | null;
  category: string | null;
}

export const usePortalCard = (props: {
  thumbnail: string | null;
  objectType?: PortalCardObjectType;
  lastUpdated: string | null;
}): {
  formattedLastUpdated: ComputedRef<string | null>;
  getImageUrl: ComputedRef<string>;
} => {
  const formattedLastUpdated = computed(() => {
    if (!props.lastUpdated) return null;
    return formatDateValue(props.lastUpdated);
  });

  const getImageUrl = computed(() => {
    if (props.thumbnail) return props.thumbnail;
    if (props.objectType === PortalCardObjectType.Map) return defaultMapsThumbnail;
    return "";
  });

  return { formattedLastUpdated, getImageUrl };
};
