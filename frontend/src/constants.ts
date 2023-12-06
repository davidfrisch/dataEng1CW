export const STATUS_UPLOAD = {
  SUCCESS: 0,
  ALREADY_EXIST: 1,
  ERROR: 2,
};

export const STATUS_COLORMAP = {
  [STATUS_UPLOAD.SUCCESS]: "#00ff00",
  [STATUS_UPLOAD.ALREADY_EXIST]: "#ffff00",
  [STATUS_UPLOAD.ERROR]: "#ff0000",
};

if (import.meta.env.VITE_BACKEND_URL === undefined) {
  throw new Error("VITE_BACKEND_URL is not defined");
}
export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

if (import.meta.env.VITE_SPARK_UI_URL === undefined) {
  throw new Error("VITE_SPARK_UI_URL is not defined");
}

export const SPARK_URL = import.meta.env.VITE_SPARK_UI_URL;
