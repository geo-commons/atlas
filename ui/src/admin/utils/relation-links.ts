export interface IRelationOption {
  id?: number | string;
  value?: number | string;
  label?: string;
  name?: string;
  title?: string;
}

export interface IRelationLink {
  id: number | string;
  label: string;
}

const getId = (value: unknown): number | string | null => {
  if (typeof value === "number" || typeof value === "string") {
    return value;
  }

  if (value && typeof value === "object" && "id" in value) {
    const id = value.id;
    return typeof id === "number" || typeof id === "string" ? id : null;
  }

  return null;
};

const getLabel = (value: IRelationOption | undefined, fallback: number | string): string => {
  return value?.label || value?.title || value?.name || String(fallback);
};

export const getRelationLinks = (value: unknown, options: IRelationOption[] = []): IRelationLink[] => {
  const selectedValues = Array.isArray(value) && value.every(Array.isArray) ? value[1] || [] : value;
  const values = Array.isArray(selectedValues) ? selectedValues : [selectedValues];

  return values.reduce<IRelationLink[]>((links, selectedValue) => {
    const id = getId(selectedValue);
    if (id === null || links.some((link) => String(link.id) === String(id))) {
      return links;
    }

    const matchingOption = options.find((option) => String(option.id ?? option.value) === String(id));
    const selectedOption =
      selectedValue && typeof selectedValue === "object" ? (selectedValue as IRelationOption) : matchingOption;

    return [...links, { id, label: getLabel(selectedOption || matchingOption, id) }];
  }, []);
};
