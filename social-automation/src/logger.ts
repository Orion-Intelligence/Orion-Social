
export const logger = {
  info(message: string, meta?: Record<string, unknown>): void {
    const ts = new Date().toISOString();
    const suffix = meta ? ` ${JSON.stringify(meta)}` : '';
    console.log(`[${ts}] [social-automation] INFO  ${message}${suffix}`);
  },

  warn(message: string, meta?: Record<string, unknown>): void {
    const ts = new Date().toISOString();
    const suffix = meta ? ` ${JSON.stringify(meta)}` : '';
    console.warn(`[${ts}] [social-automation] WARN  ${message}${suffix}`);
  },

  error(message: string, meta?: Record<string, unknown>): void {
    const ts = new Date().toISOString();
    const suffix = meta ? ` ${JSON.stringify(meta)}` : '';
    console.error(`[${ts}] [social-automation] ERROR ${message}${suffix}`);
  },

  debug(message: string, meta?: Record<string, unknown>): void {
    if (process.env['ORION_SOCIAL_DEBUG'] === '1') {
      const ts = new Date().toISOString();
      const suffix = meta ? ` ${JSON.stringify(meta)}` : '';
      console.debug(`[${ts}] [social-automation] DEBUG ${message}${suffix}`);
    }
  },
};
