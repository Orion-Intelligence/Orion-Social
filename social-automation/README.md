# Orion Social Automation – Session Manager

A production-quality TypeScript/Playwright module that manages persistent browser sessions for social-media platforms. Log in manually once, then reuse the authenticated session for automated actions.

## Quick Start

```bash
# 1. Install dependencies
cd Orion-Social/social-automation
npm install

# 2. Install Playwright browsers (one-time)
npx playwright install chromium

# 3. Log in to a platform (opens a visible browser)
npm run social:login -- --platform facebook

# 4. Check session status
npm run social:status -- --platform facebook
```

## Architecture

```
social-automation/
├── src/
│   ├── index.ts               # Public API barrel export
│   ├── config.ts              # Centralised configuration (env vars)
│   ├── errors.ts              # Typed error hierarchy
│   ├── logger.ts              # Structured logger (never logs credentials)
│   ├── cli/
│   │   ├── login.ts           # CLI: manual login command
│   │   └── status.ts          # CLI: session status command
│   ├── platforms/
│   │   ├── types.ts           # SocialPlatform interface
│   │   ├── registry.ts        # Platform lookup + registration
│   │   ├── facebook.ts        # Facebook adapter
│   │   ├── x.ts               # X (Twitter) adapter
│   │   ├── instagram.ts       # Instagram adapter
│   │   └── linkedin.ts        # LinkedIn adapter
│   └── session/
│       ├── manager.ts         # Core session management API
│       └── shutdown.ts        # Graceful SIGINT/SIGTERM handler
├── tests/                     # Unit tests (no real accounts needed)
├── profiles/                  # ⚠️ SENSITIVE – never commit (gitignored)
│   ├── facebook/
│   ├── x/
│   ├── instagram/
│   └── linkedin/
├── package.json
├── tsconfig.json
└── vitest.config.ts
```

## How Sessions Work

1. **First login**: `npm run social:login -- --platform facebook` launches Chromium with a **persistent browser context** stored in `profiles/facebook/`. You log in manually in the visible browser window.

2. **Authentication detection**: The platform adapter's `isAuthenticated()` method polls the page state (URL patterns, authenticated-only DOM elements) to detect when login succeeds. The browser closes automatically.

3. **Session reuse**: Subsequent calls to `getSocialContext('facebook')` open the same persistent profile. Playwright automatically restores cookies, localStorage, and IndexedDB — no re-login needed.

4. **Session validation**: Every time you open a session, the adapter verifies authentication is still valid. If the session has expired, a `SessionExpiredError` is thrown with a clear re-login instruction.

## CLI Commands

### Login
```bash
npm run social:login -- --platform <name>
```
Opens a visible browser for manual login. Supported platforms: `facebook`, `x`, `instagram`, `linkedin`.

### Status
```bash
npm run social:status -- --platform <name>
```
Reports safe session information:
```
— Session Status —
  Platform:      Facebook
  Authenticated: yes
  Profile:       configured
  Profile path:  /path/to/profiles/facebook
```

## Programmatic API

```typescript
import {
  manualLogin,
  getSocialContext,
  getSocialPage,
  getSocialBrowser,
  getSessionStatus,
} from '@orion/social-automation';

// Open an authenticated page
const page = await getSocialPage('facebook');
// ... perform automated actions ...
await page.context().close();

// Check status
const status = await getSessionStatus('x');
console.log(status.authenticated); // true/false
```

## Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `ORION_SOCIAL_PROFILE_DIR` | `./profiles` | Base directory for browser profiles |
| `ORION_SOCIAL_HEADLESS` | `false` | Run browsers headless (reuse only) |
| `ORION_SOCIAL_LOGIN_TIMEOUT_MS` | `300000` | Max wait for manual login (5 min) |
| `ORION_SOCIAL_AUTH_POLL_MS` | `3000` | Interval between auth checks |
| `ORION_SOCIAL_NAV_TIMEOUT_MS` | `30000` | Navigation timeout |
| `ORION_SOCIAL_DEBUG` | _(unset)_ | Set to `1` for debug logging |

## Adding a New Platform

1. Create `src/platforms/myplatform.ts`:
   ```typescript
   import type { Page } from 'playwright';
   import type { SocialPlatform } from './types.js';

   export class MyPlatform implements SocialPlatform {
     readonly name = 'myplatform';
     readonly displayName = 'My Platform';
     readonly loginUrl = 'https://myplatform.com/login';

     async isAuthenticated(page: Page): Promise<boolean> {
       // Navigate and check for authenticated-only elements
       await page.goto('https://myplatform.com/', { waitUntil: 'domcontentloaded', timeout: 15_000 });
       return page.evaluate(() => {
         // Check URL, DOM elements, etc.
         return !window.location.href.includes('/login');
       });
     }
   }
   ```

2. Register in `src/platforms/registry.ts`:
   ```typescript
   import { MyPlatform } from './myplatform.js';
   // Add to the platforms map:
   ['myplatform', new MyPlatform()],
   ```

3. Add tests in `tests/`.

## Security Considerations

> ⚠️ **Browser profiles contain sensitive authentication material** including cookies, localStorage data, and session tokens. Handle them as you would handle passwords.

- **Never commit** `profiles/` to Git (already in `.gitignore`)
- **Never log** passwords, cookies, or tokens (enforced by the logger module)
- **Never extract** cookies or tokens from profiles programmatically
- **File permissions**: Ensure `profiles/` is only readable by the current user
- Profiles are stored **locally only** — they are not synced, uploaded, or shared
- The `social:status` command only reports safe metadata (authenticated yes/no)

## Troubleshooting

### Expired session
```
SessionExpiredError: Session for "facebook" has expired or is invalid.
Please re-authenticate: npm run social:login -- --platform facebook
```
**Fix**: Run the login command again to refresh the session.

### Browser not installed
```
BrowserLaunchError: Failed to launch browser: Executable doesn't exist
```
**Fix**: Run `npx playwright install chromium`.

### Login timeout
```
LoginTimeoutError: Login for "facebook" was not completed within the allowed time.
```
**Fix**: Increase `ORION_SOCIAL_LOGIN_TIMEOUT_MS` or complete login faster.

### MFA/2FA prompts
The browser stays open during login. Complete any MFA/2FA/CAPTCHA prompts manually. The system polls for authentication and will detect when you're logged in.

## Development

```bash
# Type-check
npm run typecheck

# Run tests
npm run test

# Build
npm run build

# Lint
npm run lint
```
