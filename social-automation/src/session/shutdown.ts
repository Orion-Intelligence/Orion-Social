import type { BrowserContext } from 'playwright';


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

  const shutdown = (_signal: string) => {

    closeAll()
      .catch(() => {  })
      .finally(() => process.exit(0));
  };

  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('uncaughtException', (_err) => {

    closeAll()
      .catch(() => {  })
      .finally(() => process.exit(1));
  });
}
