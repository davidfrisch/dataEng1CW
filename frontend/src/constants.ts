

if (import.meta.env.VITE_BACKEND_URL === undefined) {
    throw new Error("VITE_BACKEND_URL is not defined");
}
export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;