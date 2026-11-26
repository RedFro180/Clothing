# Lockdown checklist: only you can change or publish the site

Do these once, in order, and keep this file. Each step says **where** to click.

**The idea:** your accounts are the locks. The website itself has nothing to log into: no admin page online, no database, no passwords, and the settings editor runs on your own computer. So anyone who wants to change the site has to get into **GitHub**, **Cloudflare**, your **domain registrar**, or your **email**. Lock those, and make publishing require **you, by hand**.

## 1. Email first (it can reset everything else)
- [ ] Use an email you only use for the business, with a long unique password.
- [ ] Turn on 2-step verification, ideally with a **security key or passkey**. Turn off SMS codes if the provider allows (SIM-swap risk).
- [ ] Save the recovery codes offline (printed, or in a password manager).

## 2. Password manager
- [ ] Use one, such as 1Password or Bitwarden. Every account gets a unique, generated password.

## 3. GitHub (where the code lives)
- [ ] Settings → Password and authentication → **2FA on**, with a passkey or security key.
- [ ] Repo → Settings → General → keep it **Private**.
- [ ] Repo → Settings → Collaborators → **only you**.
- [ ] **AI and app access.** You gave the **Claude GitHub App** write access so I could push. That means an AI *can* change files in the repo while it's connected. To keep it so only you can:
  - [ ] When you're not actively working with me, go to github.com → Settings → Applications → **Installed GitHub Apps → Claude → Configure**, and set Repository access to **none** (or uninstall). Turn it back on only for a session.
  - [ ] Check the same page for any other apps or "Authorized OAuth Apps" you don't recognise, and remove them.
  - [ ] I only push to `claude/...` branches, never `main`. With step 4 below, nothing I push can go live without you.
- [ ] **Branch protection on `main`:** require a pull request, require the **Site safety check** to pass, block force-pushes and deletions. `.github/CODEOWNERS` already names you as the required reviewer. **Note:** for *private* repos, GitHub's branch rules generally need a paid plan (Team; Pro is unclear in GitHub's docs). On the free plan, step 4 is your real gate ([GitHub docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), [community thread](https://github.com/orgs/community/discussions/174419)).

## 4. Cloudflare Pages (what makes it live): the real "only I can publish" switch
- [ ] My Profile → Authentication → **2FA on** (security key if possible).
- [ ] Pages project → Settings → Builds & deployments:
  - [ ] Production branch: **`main`** only.
  - [ ] **Turn off automatic production deployments.** Then nothing goes live until **you** press "Deploy" in Cloudflare, even if someone or something changes GitHub.
  - [ ] Preview deployments: off, or protect them with **Cloudflare Access** (Zero Trust → Access → add your email only) so only you can see previews.
- [ ] Security → Settings → **Configure AI bot policies** (Cloudflare replaced the single "Block AI bots" switch with separate Search / Training / Agent controls in 2026): set **Search: Allow**, **Training: Disallow AI Training** (not "Block": Block also removes Googlebot from search), **Agents: Allow**. Turn on **Bot Fight Mode**. ([Cloudflare docs](https://developers.cloudflare.com/bots/additional-configurations/block-ai-bots/), [Cloudflare blog](https://blog.cloudflare.com/accountable-mixed-use-ai-crawlers/))
- [ ] Manage account → Members → **only you**.
- [ ] Bookmark **Deployments → Rollback**. If anything ever looks wrong, roll back first, then investigate.

## 5. Domain name
- [ ] Registrar: 2FA on, **registrar lock / transfer lock on**, auto-renew on. Losing the domain is the worst-case hijack.
- [ ] Turn on **DNSSEC** (one click if the domain is on Cloudflare).

## 6. Other services
- [ ] Formspree, PostHog, Shopify, TikTok Shop, Instagram: **2FA on**, only you as a member.
- [ ] Never paste passwords or keys into chats, AI tools or the repo. The PostHog key and form address are public by design; nothing else is.

## What's already built into the site
- **Settings editor:** `tools/admin.html` runs only on your computer. There's no online admin to break into.
- **Security headers** (`site/_headers`):
  - only your own files plus PostHog and Formspree can load
  - the page can't be embedded in another site
  - no camera, microphone or location access
  - HTTPS forced
- **No injection:** no part of the page is ever built from what a visitor types.
- **Order protection:** limits, bot trap, rate limit, order numbers, a recorded final-sale agreement, and prices always taken from the catalog.
- **AI crawlers:** `robots.txt` blocks AI *training* crawlers (OpenAI GPTBot, Anthropic ClaudeBot, Google-Extended, Common Crawl, ByteDance, Meta, Apple-Extended, Amazon and others) and allows AI *search/shopping* bots (OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User) so products can be found and linked in AI assistants (user decision 2026-11-26). The `noai` / `noimageai` tags stay.
- **Automatic check:** every push runs the GitHub **Site safety check** (settings checker, abuse tests, 50 simulated shoppers). A red ✗ means don't deploy.

## Honest limits
- **Public means copyable.** Anything public can be viewed and copied by a person with a browser. Nothing can stop that. Your protection for designs is copyright and trademark, not the website.
- **robots.txt is voluntary.** Cloudflare's bot blocking enforces it for most bots, but it isn't perfect.
- **Payments:** checkout security (fraud, card data) belongs to Shopify or Stripe once you take payments. Never handle card numbers yourself.
