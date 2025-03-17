/**
 * List of allowed MIME types for file uploads.
 * Ensures that only images in JPEG and PNG formats are accepted.
 */
export const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"];

/**
 * Maximum file size allowed for uploads (in bytes).
 * Set to 10MB (10,000,000 bytes) to prevent excessively large files from being uploaded.
 */
export const MAX_FILE_SIZE = 10_048_577;
