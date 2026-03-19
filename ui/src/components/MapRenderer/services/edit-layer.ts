import { EditLayerMode } from "@/types/map";
import { useEditLayerStore } from "@/stores/edit_layer_store";
import Feature from "ol/Feature";
import { MultiLineString, MultiPoint, MultiPolygon } from "ol/geom";

type EditLayerStore = ReturnType<typeof useEditLayerStore>;

interface ToolResult {
  tool: string;
  sketch: Feature;
}

interface FinalizeMultipartOptions {
  event: KeyboardEvent;
  editLayerStore: EditLayerStore;
  tool: string;
  clearTool: () => void;
}

interface HandleToolUsedOptions {
  editLayerStore: EditLayerStore;
  result: ToolResult;
  clearTool: () => void;
}

const isMultipartGeometryTool = (tool: string) => {
  return ["MultiPoint", "MultiLineString", "MultiPolygon"].includes(tool);
};

const getMultipartGeometry = (tool: string, geometry: any) => {
  switch (tool) {
    case "MultiPoint":
      return geometry.getType() === "MultiPoint" ? geometry.clone() : new MultiPoint([geometry.getCoordinates()]);
    case "MultiLineString":
      return geometry.getType() === "MultiLineString"
        ? geometry.clone()
        : new MultiLineString([geometry.getCoordinates()]);
    case "MultiPolygon":
      return geometry.getType() === "MultiPolygon" ? geometry.clone() : new MultiPolygon([geometry.getCoordinates()]);
    default:
      return geometry.clone();
  }
};

const appendGeometryToDraftFeature = (editLayerStore: EditLayerStore, tool: string, sketch: Feature) => {
  const sketchGeometry = sketch.getGeometry();

  if (!sketchGeometry) {
    return;
  }

  const nextGeometry = getMultipartGeometry(tool, sketchGeometry);

  if (!editLayerStore.draftFeature) {
    const draftFeature = sketch.clone();
    draftFeature.setGeometry(nextGeometry);
    editLayerStore.setDraftFeature(draftFeature);
    return;
  }

  const draftFeature = editLayerStore.draftFeature.clone();
  const currentDraftGeometry = editLayerStore.draftFeature.getGeometry();

  if (!currentDraftGeometry) {
    return;
  }

  const currentGeometry = getMultipartGeometry(tool, currentDraftGeometry);

  switch (tool) {
    case "MultiPoint":
      draftFeature.setGeometry(new MultiPoint([...currentGeometry.getCoordinates(), ...nextGeometry.getCoordinates()]));
      break;
    case "MultiLineString":
      draftFeature.setGeometry(
        new MultiLineString([...currentGeometry.getCoordinates(), ...nextGeometry.getCoordinates()]),
      );
      break;
    case "MultiPolygon":
      draftFeature.setGeometry(
        new MultiPolygon([...currentGeometry.getCoordinates(), ...nextGeometry.getCoordinates()]),
      );
      break;
  }

  editLayerStore.setDraftFeature(draftFeature);
};

const createRedrawnFeature = (editLayerStore: EditLayerStore, geometry: any) => {
  const sourceFeature = editLayerStore.modifiedFeature || editLayerStore.highlightedFeatureAndLayer?.feature;

  if (!sourceFeature) {
    return null;
  }

  const redrawnFeature = sourceFeature.clone();
  redrawnFeature.setGeometry(geometry.clone());

  if (sourceFeature.getId()) {
    redrawnFeature.setId(sourceFeature.getId());
  }

  return redrawnFeature;
};

const finishRedrawingFeature = ({ editLayerStore, result, clearTool }: HandleToolUsedOptions) => {
  if (!editLayerStore.highlightedFeatureAndLayer) {
    return false;
  }

  const geometry = result.sketch.getGeometry();
  const redrawnFeature = geometry ? createRedrawnFeature(editLayerStore, geometry) : null;

  if (!redrawnFeature) {
    return false;
  }

  editLayerStore.setHighlightedFeatureAndLayer({
    feature: redrawnFeature,
    layer: editLayerStore.highlightedFeatureAndLayer.layer,
  });
  editLayerStore.setDraftFeature(null);
  editLayerStore.setIsRedrawingFeature(false);
  clearTool();

  return true;
};

const finalizeMultipartFeatureOnEnter = ({ event, editLayerStore, tool, clearTool }: FinalizeMultipartOptions) => {
  if (event.key !== "Enter") {
    return false;
  }

  if (
    (editLayerStore.editLayerMode !== EditLayerMode.ADD && !editLayerStore.isRedrawingFeature) ||
    !isMultipartGeometryTool(tool) ||
    !editLayerStore.draftFeature ||
    editLayerStore.isDrawingFeaturePart
  ) {
    return false;
  }

  const finalizedFeature = editLayerStore.draftFeature.clone();

  if (editLayerStore.isRedrawingFeature && editLayerStore.highlightedFeatureAndLayer) {
    const geometry = finalizedFeature.getGeometry();
    const redrawnFeature = geometry ? createRedrawnFeature(editLayerStore, geometry) : null;

    if (!redrawnFeature) {
      return false;
    }

    editLayerStore.setHighlightedFeatureAndLayer({
      feature: redrawnFeature,
      layer: editLayerStore.highlightedFeatureAndLayer.layer,
    });
    editLayerStore.setIsRedrawingFeature(false);
  } else {
    editLayerStore.setFeature(finalizedFeature);
  }

  editLayerStore.setDraftFeature(null);
  clearTool();
  event.preventDefault();

  return true;
};

const onEditLayerToolStarted = (editLayerStore: EditLayerStore, tool: string) => {
  if (
    (editLayerStore.editLayerMode === EditLayerMode.ADD || editLayerStore.isRedrawingFeature) &&
    isMultipartGeometryTool(tool)
  ) {
    editLayerStore.setIsDrawingFeaturePart(true);
  }
};

const handleEditLayerToolUsed = ({ editLayerStore, result, clearTool }: HandleToolUsedOptions) => {
  switch (result.tool) {
    case "Point":
    case "Polygon":
    case "LineString":
    case "LinearRing":
    case "Circle":
      if (editLayerStore.isRedrawingFeature) {
        return finishRedrawingFeature({ editLayerStore, result, clearTool });
      }

      editLayerStore.setDraftFeature(null);
      editLayerStore.setFeature(result.sketch);
      clearTool();
      return true;
    case "MultiPoint":
    case "MultiLineString":
    case "MultiPolygon":
      appendGeometryToDraftFeature(editLayerStore, result.tool, result.sketch);
      return true;
    default:
      return false;
  }
};

export {
  createRedrawnFeature,
  finalizeMultipartFeatureOnEnter,
  finishRedrawingFeature,
  handleEditLayerToolUsed,
  isMultipartGeometryTool,
  onEditLayerToolStarted,
};
