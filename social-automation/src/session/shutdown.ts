import type { BrowserContext } from 'playwright';
import { logger } from '../logger.js';

const activeContexts = new Set<BrowserContext>();

let registered = false;

export function trackContext(context: BrowserContext): void {
  activeContexts.add(context);
  ensureHandlersRegistered();
}

export function untrackContext(context: BrowserContext): void {
  activeContexts.delete(context);
}

async function closeAll(): Promise<void> {
  const pending = [...activeContexts];
  activeContexts.clear();

  await Promise.allSettled(
    pending.map(async (ctx) => {
      try {
        await ctx.close();
      } catch {
        
      }
    }),
  );
}

function ensureHandlersRegistered(): void {
  if (registered) {
    return;
  }
  registered = true;

  const shutdown = (signal: string) => {
    logger.info(`Received ${signal}, closing browser contexts…`);
    closeAll()
      .catch(() => {  })
      .finally(() => process.exit(0));
  };

  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('uncaughtException', (err) => {
    logger.error('Uncaught exception – shutting down', {
      error: err.message,
    });
    closeAll()
      .catch(() => {  })
      .finally(() => process.exit(1));
  });
}
