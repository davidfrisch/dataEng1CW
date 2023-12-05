

export const STATUS_UPLOAD = {
    SUCCESS: 0,
    ALREADY_EXIST: 1,
    ERROR: 2
}

if(!process.env.SHARE_DIR) {
    process.exit(1)
}
export const SHARE_DIR = process.env.SHARE_DIR 

if (!process.env.FLASK_URL) {
    process.exit(1)
}

export const FLASK_URL = process.env.FLASK_URL
