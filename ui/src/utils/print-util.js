import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";
import { fetchLegendImage } from "@/utils/legend-utils";
import northArrow from "@/assets/images/north_arrow.png";

/**
 * Generates a PDF representation of the map, including custom settings, overlays, legends, and optional metadata.
 *
 * @param {Object} settings - Configuration for the PDF export.
 * @param {string} settings.format - PDF size format (e.g., 'a4', 'a3').
 * @param {string} settings.orientation - Orientation of the PDF ('portrait' or 'landscape').
 * @param {string} settings.title - Title text to be included in the PDF.
 * @param {boolean} settings.showDateTime - Whether to include the current date and time.
 * @param {boolean} settings.showLegend - Whether to include legends of visible layers.
 * @param {boolean} settings.showLogo - Whether to include an organizational logo.
 * @param {boolean} settings.showNorth - Whether to include a north arrow indicator.
 * @param {boolean} settings.showScale - Whether to include a map scale.
 * @param {string} settings.remarks - Additional remarks to include in the PDF.
 * @param {Object} mapRef - Reference to the OpenLayers map object.
 * @param {Array} layers - List of map layers with visibility and legend data.
 * @param {Object} user - User data for accessing legend resources or API endpoints.
 * @param {Object} config - Configuration settings, including an optional organizational logo.
 * @param {Object} position - Geospatial data for fetching legends specific to layers.
 * @returns {Promise<void>} Resolves when the PDF is successfully created and downloaded; rejects on error.
 *
 */
export const printMapToPdf = (settings, mapRef, layers, user, config, position) => {
  return new Promise((resolve, reject) => {
    try {
      // We need the visible layers to determine which legends need to be fetched.
      const visibleLayers = layers?.filter((l) => !l.is_base && l.is_visible === true);

      const margin = 0;

      const dims = {
        a0: [1189, 841],
        a1: [841, 594],
        a2: [594, 420],
        a3: [420, 297],
        a4: [297, 210],
      };

      const resolution = 150;

      let dim = dims[settings.format].map((d) => d - margin * 2);
      if (settings.orientation === "portrait") {
        dim = dim.reverse();
      }

      const map = mapRef;
      const view = map.getView();

      const width = Math.round((dim[0] * resolution) / 25.4);
      const height = Math.round((dim[1] * resolution) / 25.4);
      const size = map.getSize();
      const viewResolution = view.getResolution();

      map.once("rendercomplete", () => {
        const mapCanvas = document.createElement("canvas");
        mapCanvas.width = width;
        mapCanvas.height = height;
        const mapContext = mapCanvas.getContext("2d");
        Array.prototype.forEach.call(document.querySelectorAll(".ol-layer canvas"), function (canvas) {
          if (canvas.width > 0) {
            mapContext.globalAlpha = 1;
            const transform = canvas.style.transform;
            // Get the transform parameters from the style's transform matrix
            const matrix = transform
              .match(/^matrix\(([^(]*)\)$/)[1]
              .split(",")
              .map(Number);
            // Apply the transform to the export map context
            CanvasRenderingContext2D.prototype.setTransform.apply(mapContext, matrix);
            mapContext.drawImage(canvas, 0, 0);
          }
        });

        mapContext.globalAlpha = 1;
        mapContext.setTransform(1, 0, 0, 1, 0, 0);

        html2canvas(document.querySelector(".scale")).then((scale) => {
          mapCanvas.toBlob(async (blob) => {
            const IMAGE_SCALE_FACTOR = 5;
            const IMAGE_SPACING = 5; // Space between images
            const PADDING = 2; // Padding space

            const LOGO_WIDTH = 14;
            const LOGO_SPACING = settings.showLogo ? 14 + IMAGE_SPACING : PADDING;
            const NORTH_IMAGE_DIMENSIONS = [62, 120];

            const url = window.URL || window.webkitURL;
            const imgSrc = url.createObjectURL(blob);

            const img = new Image();
            img.src = imgSrc;

            const pdf = new jsPDF(settings.orientation, undefined, settings.format);

            pdf.addImage(img, "JPEG", margin, margin, dim[0], dim[1]);

            const boxX = 0;
            const boxWidth = dim[0];
            const boxHeight = settings.showLogo || (settings.title && settings.showDateTime) ? 18 : 12;
            const boxY = dim[1] - boxHeight;

            // Draw the box background (white)
            pdf.setFillColor(255, 255, 255);
            pdf.rect(boxX, boxY, boxWidth, boxHeight, "F");

            // Draw the box border (black)
            pdf.setLineWidth(0.5); // Border thickness in mm
            pdf.setDrawColor(0, 0, 0);
            pdf.rect(boxX, boxY, boxWidth, boxHeight);

            pdf.setFontSize(16);
            pdf.setTextColor(0, 0, 0);

            // Add Title
            if (settings.title) {
              pdf.text("Titel: " + settings.title, boxX + LOGO_SPACING, boxY + IMAGE_SPACING + PADDING);
            }

            // Add Date
            if (settings.showDateTime) {
              const date = new Date().toLocaleString();
              const dateY = settings.title ? boxY + 15 : boxY + IMAGE_SPACING + PADDING;
              pdf.text("Datum: " + date, boxX + LOGO_SPACING, dateY);
            }

            // Add Remark
            if (settings.remarks) {
              const remarkY = settings.showNorth
                ? NORTH_IMAGE_DIMENSIONS[1] / IMAGE_SCALE_FACTOR + 3 * IMAGE_SPACING
                : IMAGE_SPACING;
              pdf.setFontSize(14);
              pdf.text(settings.remarks, IMAGE_SPACING, remarkY);
            }

            // Add legend
            if (settings.showLegend) {
              let positionY = IMAGE_SPACING;
              let positionX = dim[0];
              let remainingHeight = dim[1] - positionY;
              let maxWidthCurrentColumn = 0;

              // Step 1: Collect all the image data
              const images = [];

              for (let i = 0; i < visibleLayers.length; i++) {
                const { url, error } = await fetchLegendImage(visibleLayers[i], position, user);

                if (error) {
                  console.error(`Er ging iets fout bij het ophalen van de legenda van laag ${visibleLayers[i].id}`);
                  continue;
                }

                // Load the image to get its properties
                const img = new Image();
                img.src = url;

                // Use a promise to wait for the image to load
                await new Promise((resolve, reject) => {
                  img.onload = () => {
                    // Push image data to the array
                    images.push({
                      img,
                      width: img.width,
                      height: img.height,
                    });
                    resolve();
                  };
                  img.onerror = (err) => {
                    console.error("Failed to load image:", err);
                    reject(err);
                  };
                });
              }

              // Step 2: Sort the images array by width (descending order)
              images.sort((a, b) => b.width - a.width);

              // Step 3: Add sorted images to the PDF
              for (let i = 0; i < images.length; i++) {
                const { img, width, height } = images[i];

                // Calculate positions and dimensions for the PDF
                if (remainingHeight - height / IMAGE_SCALE_FACTOR - 2 * IMAGE_SPACING <= 0) {
                  remainingHeight = dim[1];
                  positionX -= maxWidthCurrentColumn / IMAGE_SCALE_FACTOR + IMAGE_SPACING;
                  positionY = IMAGE_SPACING;
                }

                pdf.addImage(
                  img,
                  "JPEG",
                  positionX - width / IMAGE_SCALE_FACTOR - IMAGE_SPACING,
                  positionY,
                  width / IMAGE_SCALE_FACTOR,
                  height / IMAGE_SCALE_FACTOR,
                );

                positionY = positionY + height / IMAGE_SCALE_FACTOR + IMAGE_SPACING;
                remainingHeight -= height / IMAGE_SCALE_FACTOR + IMAGE_SPACING;
                if (maxWidthCurrentColumn < width) {
                  maxWidthCurrentColumn = width;
                }
              }
            }

            // Add logo
            if (settings.showLogo && config?.organization_logo) {
              pdf.addImage(config.organization_logo, "PNG", boxX + PADDING, boxY + PADDING, LOGO_WIDTH, LOGO_WIDTH);
            }

            // Add north arrow
            if (settings.showNorth) {
              pdf.addImage(
                northArrow,
                "PNG",
                IMAGE_SPACING,
                IMAGE_SPACING,
                NORTH_IMAGE_DIMENSIONS[0] / IMAGE_SCALE_FACTOR,
                NORTH_IMAGE_DIMENSIONS[1] / IMAGE_SCALE_FACTOR,
              );
            }

            // Add scale
            if (settings.showScale) {
              pdf.addImage(
                scale.toDataURL(),
                "JPEG",
                dim[0] - scale.width / IMAGE_SCALE_FACTOR - IMAGE_SPACING,
                dim[1] - IMAGE_SPACING * 2,
                scale.width / IMAGE_SCALE_FACTOR,
                scale.height / IMAGE_SCALE_FACTOR,
              );
            }

            pdf.save(`atlas-${new Date().toISOString()}.pdf`);

            map.setSize(size);
            view.setResolution(viewResolution);
            document.body.style.cursor = "auto";

            resolve();
          });
        });
      });

      // Set print size
      const printSize = [width, height];
      map.setSize(printSize);
      const scaling = Math.min(width / size[0], height / size[1]);
      view.setResolution(viewResolution / scaling);
    } catch (e) {
      console.error(e);
      reject(e);
    }
  });
};
