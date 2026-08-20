import type { BrowserContext } from 'playwright';
import { logger } from '../logger.js';

/**
 * Set of active browser contexts that should be cleaned up on process
 * termination (SIGINT / SIGTERM / uncaught exceptions).
 */
const activeContexts = new Set<BrowserContext>();

let registered = false;

/** Register a context so it will be cleaned up on shutdown. */
export function trackContext(context: BrowserContext): void {
  activeContexts.add(context);
  ensureHandlersRegistered();
}

/** Remove a context from the tracked set (e.g. after intentional close). */
export function untrackContext(context: BrowserContext): void {
  activeContexts.delete(context);
}

/** Close all tracked contexts. Called during graceful shutdown. */
async function closeAll(): Promise<void> {
  const pending = [...activeContexts];
  activeContexts.clear();

  await Promise.allSettled(
    pending.map(async (ctx) => {
      try {
        await ctx.close();
      } catch {
        // Best-effort; the process is terminating.
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
      .catch(() => { /* swallow */ })
      .finally(() => process.exit(0));
  };

  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('uncaughtException', (err) => {
    logger.error('Uncaught exception – shutting down', {
      error: err.message,
    });
    closeAll()
      .catch(() => { /* swallow */ })
      .finally(() => process.exit(1));
  });
}
