
# 🚀 RALPH PLAN — ORBITA: L'App Definitiva di Trip-Planning

> **Nome in codice:** ORBITA
> **Core Value Proposition:** "L'unica app che trasforma qualunque ispirazione o conferma in un piano prenotabile e resiliente, e lo mantiene vero anche quando il viaggio cambia."
> **Questo file traccia l'avanzamento. Segna i task come completati `[x]` quando la DoD è soddisfatta.**

---

## LEGACY — Fasi Completate (0-12)

<details>
<summary>✅ Click per espandere le fasi legacy già completate</summary>

### Fase 0: Repo & Ambiente
- [x] Init repo, Vite (React+TS), SCSS (BEM), Linter/Prettier.

### Fase 1: Fondazioni
- [x] Supabase client, Auth Context, Leaflet mappa base, CSS variables.

### Fase 2: Data Layer
- [x] Tabelle `trips`/`trip_pois`, OsmService, Google Scraper, DataAggregationService.

### Fase 3: API & Core Logic
- [x] TripContext/Zustand, hooks CRUD POI, toast errori.

### Fase 4: UI Componenti & Pagine
- [x] Layout, SearchPanel, MapPlanner, DayColumn, PoiDetailsModal.

### Fase 4.5: UI/UX Polish
- [x] Design System (Inter, spacing, colori), Component Polish, Layout Polish.

### Fase 5: QA & Backpressure
- [x] Typecheck, Responsiveness, Smoke test.

### Fase 6: Deploy & Osservabilità
- [x] Build produzione, Supabase policies. (Deploy Vercel pendente)

### Fase 7-8: Next Features & Core Fixes
- [x] Profiles, PWA, Share Link, Cost Estimation, DB persistence, Search fix.

### Fase 9: Product Expansion
- [x] HomePage, AccountPage, ExplorePage, SettingsPage.

### Fase 10-11: System Consistency & New Features
- [x] Explore fix, DB refresh, Favorites, Avatar thumb.

### Fase 12: Final Polish
- [ ] UX Review con `ui-ux-pro-max`. *(Incorporata in ORBITA Phase A)*

</details>

---

# 🌌 ORBITA — PIANO DI TRASFORMAZIONE

> Ogni Fase ha un **Agente Supervisore** e ogni subtask ha il proprio **Agente Esecutore** con le skill specifiche.

> **🛡️ PROTOCOLLO GIT SENTINEL (v2 — Staging Strategy):**
>
> **Branch Flow:** `feat/* → staging → main`
>
> | Branch | Scopo | Vercel Deploy |
> |--------|-------|---------------|
> | `main` | Produzione stabile, pubblica | `orbita-web.vercel.app` / `orbita-bridge.vercel.app` |
> | `staging` | Integration & preview (condivisibile) | Preview URL auto-generato da Vercel |
> | `feat/*` | Sviluppo feature singola | Preview URL auto-generato da Vercel |
>
> **Regole:**
> 1. **Mai committare direttamente su `main` o `staging`.** Sempre branch `feat/*`.
> 2. **Branch da `staging`:** `git checkout staging && git checkout -b feat/nome-fase`.
> 3. **Commit Atomici:** Conventional Commits (`feat:`, `fix:`, `chore:`).
> 4. **Merge feat → staging:** Squash merge dopo DoD verificata. Vercel genera preview URL.
> 5. **Merge staging → main:** Solo dopo validazione completa della fase + approvazione utente. Questo triggera il deploy in produzione.
> 6. **orbita-bridge (API):** Ambiente singolo (no staging separato per API).
> 7. **📝 COMMIT CHECKPOINT (Mandatory):** Ogni volta che un pezzo funzionale del task è verificato (DoD parziale o totale soddisfatta), è **OBBLIGATORIO** fare commit + push immediato con documentazione strutturata:
>    - **Commit message:** Conventional Commits con body che elenca i DoD items achieved.
>    - **Formato:** `<type>(<scope>): <descrizione breve>`
>      ```
>      feat(ai-smoke-1.1): parser agent live test passing
>
>      DoD achieved:
>      - [x] Response success: true
>      - [x] Items contain restaurant + attraction types
>      - [x] Coordinates in valid Japan range
>      - [x] Supervision confidence >= 0.7
>      ```
>    - **Quando:** Dopo OGNI milestone verificato — non accumulare lavoro senza commit.
>    - **Perché:** Traceability, rollback granulare, progresso visibile su GitHub.
>    - **Push:** Sempre push sul branch `feat/*` corrente dopo il commit.
>
> **Agente Responsabile:** `@devops-engineer`

---

## Phase A0 — Golden Stack & Monorepo Migration
> **🎯 Supervisore:** `@devops-engineer` (skills: `scaffolding`, `deployment-procedures`)
> **Obiettivo:** Ristrutturare la repo per ospitare Frontend, API Proxy e Configurazione AI in un unico posto gestibile.

### A0.1. Monorepo Restructuring (Turborepo) ✅
- [x] Migrazione struttura a Monorepo:
  - [cite_start]Spostare l'attuale root (`src`, `vite.config`, etc.) in `apps/orbita-web`[cite: 35].
  - Creare `apps/orbita-bridge` (Next.js API) per fare da proxy sicuro verso Flowise/Supabase.
  - Creare `packages/ui` (Shared UI components) e `packages/config` (TSConfig, ESLint condivisi).
  - **Agente:** `@devops-engineer` | Skills: `scaffolding`, `monorepo-turborepo`
  - DoD: `pnpm build` compila sia web che bridge. Repo pulita.

### A0.1.5 — Git Baseline & Repository Hygiene ✅
- [x] Setup Git Monorepo:
  - Creare/Aggiornare `.gitignore` root per escludere `node_modules`, `.turbo`, `.next`, `dist`, `.env*.local` in tutti i workspace.
  - Inizializzare git (se necessario) e collegare al remote GitHub. -> link gia' aperto nel browser: https://github.com/cmpdpucc/trip-planner
  - Eseguire il primo "Grand Commit" di migrazione.
  - **Agente:** `@devops-engineer` | Skills: `version-control`, `git-flow`
  - DoD: Repo pulita, branch `main` allineato con la struttura monorepo, storico avviato.

### A0.2. OpenRouter Gateway & Bridge Foundation ✅
- [x] Setup API Proxy (OpenRouter via OpenAI SDK):
  - Pivotato da Google Gemini SDK (errori 500) a **OpenRouter** con `openai` SDK standard.
  - Endpoint `POST /api/test-ai` in `apps/orbita-bridge` funzionante con `openrouter/free` (auto-routing).
  - API Key `orbita-dev` creata su OpenRouter, salvata in `.env.local` (gitignored).
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`
  - DoD: Risposta AI verificata dal bridge (`liquid/lfm-2.5-1.2b-instruct:free`). ✅
- [x] Infrastruttura Flowise preparata:
  - `infrastructure/flowise/` con `Dockerfile`, `docker-compose.yml`, `README.md`.
  - `render.yaml` alla root per auto-deploy su Render.com.
  - **Agente:** `@devops-engineer` | Skills: `deployment-procedures`
  - DoD: File di deploy pronti e committati su `main`. ✅

### A0.3. AI Gateway — Custom Implementation (replaces Flowise deployment)
**Status**: 🟢 Complete  
**Decision**: Skip Flowise, implement custom agents in `orbita-bridge` with OpenRouter + Zod
**Rationale**: 
- Flowise requires 512MB+ RAM (Render free tier fails) [cite: previous debug logs]
- Custom implementation fits Vercel serverless (free, 100MB RAM per function)
- Direct control over multi-agent patterns, no Flowise overhead

---

#### A0.3.1. Parser Agent Foundation
**Supervisore**: `@backend-specialist` (skills: `api-patterns`, `nodejs-best-practices`)
**Obiettivo**: Implement `/api/agents/parse` endpoint with Zod structured output

**Task**:
- [x] Create `apps/orbita-bridge/app/api/agents/parse/route.ts`
  - Accept `{ input: string, context?: object }` POST body
  - Call OpenRouter with `google/gemini-2.0-flash-exp:free` model
  - Use Zod `ParseResultSchema` for structured output
  - Return `{ success: boolean, data: ParseResult, usage: object }`
  - **Agente**: `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`, `clean-code`
  - **DoD**: 
    - Endpoint returns valid JSON matching `ParseResultSchema`
    - Input validation with max 10k chars
    - Error handling with proper status codes (400, 422, 500)
    - No hardcoded API keys (use `process.env.OPENROUTER_API_KEY`)

- [x] Define Zod Schemas in `apps/orbita-bridge/lib/schemas/trip.ts`
  - `TripItemSchema`: name, type, lat, lng, date, cost, confidence_score
  - `ParseResultSchema`: items[], trip_title?, start_date?, end_date?
  - **Agente**: `@backend-specialist` | Skills: `clean-code`, `api-patterns`
  - **DoD**:
    - Schemas align with existing Supabase schema (trip_pois table)
    - All fields typed, no `any`
    - Confidence score 0-1 with `.min(0).max(1)` validation

- [x] Environment Setup
  - Add `OPENROUTER_API_KEY` to `.env.local` (gitignored)
  - Add `openai` SDK dependency: `pnpm add openai zod`
  - **Agente**: `@devops-engineer` | Skills: `deployment-procedures`
  - **DoD**: 
    - Dependencies installed in `apps/orbita-bridge/package.json`
    - `.env.local` in `.gitignore`
    - README updated with env var requirements

---

#### A0.3.2. Supervisor Loop (G0 Pattern)
**Supervisore**: `@backend-specialist` (skills: `api-patterns`, `clean-code`)
**Obiettivo**: Add self-checking loop to prevent hallucinations

**Task**:
- [x] Implement `parseWithSupervisor()` wrapper in `parse/route.ts`
  - Step 1: Parser Agent generates JSON
  - Step 2: Supervisor Agent validates (LLM checks: schema-compliant, realistic, complete)
  - Step 3: Retry with feedback if confidence < 0.7 (max 2 retries)
  - **Agente**: `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - **DoD**:
    - Supervisor returns `{ valid: boolean, issues: string[], confidence: number }`
    - Retry loop implemented with max 2 attempts
    - Returns error after max retries with detailed feedback
    - Logs each iteration for debugging

---

#### A0.3.3. Enrichment Agent
**Supervisore**: `@backend-specialist` (skills: `api-patterns`, `nodejs-best-practices`)
**Obiettivo**: Implement `/api/agents/enrich` endpoint with Tavily Search

**Task**:
- [x] Create `apps/orbita-bridge/app/api/agents/enrich/route.ts`
  - Accept `{ poi_name: string, lat: number, lng: number }` POST body
  - Call Tavily API for search results (max 3 results)
  - LLM extracts structured info: opening_hours, price, rating, reviews
  - Return `EnrichedPOISchema` with source URLs
  - **Agente**: `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - **DoD**:
    - Tavily API integration functional
    - LLM parsing returns structured JSON (Zod validated)
    - Source URLs included for provenance
    - Error handling for API failures (fallback: return partial data)

- [x] Environment Setup for Tavily
  - Add `TAVILY_API_KEY` to env vars
  - Free tier: 1000 searches/month
  - **Agente**: `@devops-engineer` | Skills: `deployment-procedures`
  - **DoD**: 
    - API key secured in env
    - Rate limit monitoring (log usage)

---

#### A0.3.4. Frontend Service Layer
**Supervisore**: `@frontend-specialist` (skills: `react-patterns`, `clean-code`)
**Obiettivo**: Create type-safe service layer for calling AI agents from frontend

**Task**:
- [x] Create `apps/orbita-web/src/services/aiService.ts`
  - `parseUserInput(text: string): Promise<ParseResult>`
  - `enrichPOI(poi: {name, lat, lng}): Promise<EnrichedPOI>`
  - Type-safe with Zod schemas imported from bridge (via shared package?)
  - **Agente**: `@frontend-specialist` | Skills: `react-patterns`, `nextjs-best-practices`, `clean-code`
  - **DoD**:
    - Functions return typed responses
    - Error handling with user-friendly messages
    - Loading states handled
    - No API URLs hardcoded (use env vars or relative paths)

- [x] Create React Hooks
  - `useParser()`: hook for parser agent with loading/error states
  - `useEnrichment()`: hook for enrichment agent
  - **Agente**: `@frontend-specialist` | Skills: `react-patterns`
  - **DoD**:
    - Hooks return `{ data, loading, error, execute }` pattern
    - Memoization for performance (React.useCallback)
    - TypeScript types exported

---

#### A0.3.5. Database Extensions for Provenance
**Supervisore**: `@database-architect` (skills: `database-design`)
**Obiettivo**: Extend Supabase schema for AI guardrails

**Task**:
- [x] Create Supabase migration for new tables
  - `sources` table: id, url, type, fetched_at, confidence_score
  - `price_snapshots` table: item_id, price, currency, source_id, snapshot_at
  - `verification_logs` table: item_id, agent, result, confidence, verified_at
  - **Agente**: `@database-architect` | Skills: `database-design`
  - **DoD**:
    - Migration script in `supabase/migrations/`
    - Foreign keys link to `trip_items` table
    - Indexes on frequently queried columns (item_id, snapshot_at)
    - RLS policies defined for user access

- [x] Extend `trip_pois` table with AI metadata
  - Add columns: `source_id` (FK to sources), `confidence_score`, `verified_at`, `ai_generated`
  - **Agente**: `@database-architect` | Skills: `database-design`
  - **DoD**:
    - Migration reversible (rollback plan)
    - Existing data preserved (nullable columns)
    - RLS policies updated

---

#### A0.3.6. Testing Suite
**Supervisore**: `@test-engineer` (skills: `testing-patterns`, `tdd-workflow`)
**Obiettivo**: Unit tests for AI agents

**Task**:
- [x] Unit tests for Parser Agent
  - Test: valid input → valid ParseResult
  - Test: invalid input → proper error
  - Test: supervisor loop triggers on low confidence
  - Mock OpenRouter API responses
  - **Agente**: `@test-engineer` | Skills: `testing-patterns`, `nodejs-best-practices`
  - **DoD**:
    - Tests in `apps/orbita-bridge/__tests__/agents/parse.test.ts`
    - Coverage > 80% for critical paths
    - Mocks for external APIs (OpenRouter, Tavily)

- [x] Integration tests for end-to-end flow
  - Test: user input → parsed items → saved to DB
  - **Agente**: `@qa-automation-engineer` | Skills: `webapp-testing`, `testing-patterns`
  - **DoD**:
    - Playwright test simulating user journey
    - Test data cleanup after each run

---

#### A0.3.7. Deployment Configuration
**Supervisore**: `@devops-engineer` (skills: `deployment-procedures`)
**Obiettivo**: Deploy `orbita-bridge` to Vercel Serverless

**Task**:
- [x] Vercel Configuration
  - Connect GitHub repo to Vercel
  - Set root directory: `apps/orbita-bridge`
  - Add environment variables: `OPENROUTER_API_KEY`, `TAVILY_API_KEY`, `NEXT_PUBLIC_SUPABASE_URL`, etc.
  - **Agente**: `@devops-engineer` | Skills: `deployment-procedures`
  - **DoD**:
    - Auto-deploy on `git push` to `main`
    - Environment variables secured (not in repo)
    - Build succeeds without errors
    - Preview deployments work on PRs

- [x] Monitoring Setup
  - Add Vercel Analytics
  - Log AI agent usage (tokens, latency) to Supabase or logging service
  - **Agente**: `@devops-engineer` | Skills: `deployment-procedures`
  - **DoD**:
    - Dashboard shows API call stats
    - Alerts for high error rates or cost spikes


## Phase A — Architecture & Foundation Rewrite
> **🎯 Supervisore:** `@orchestrator` (skills: `parallel-agents`, `behavioral-modes`)
> **Obiettivo:** Ridisegnare l'architettura per supportare il modello "sistema d'azione" a oggetti verificabili.

### A1. Architecture Decision Records (ADR)
- [ ] Definire ADR per transizione da SPA monolitica a architettura modulare event-driven.
  - **Agente:** `@project-planner` | Skills: `architecture`, `plan-writing`
  - DoD: ADR documentati in `/docs/adr/` con trade-off espliciti.

### A2. Data Model Revolution — "Verifiable Objects"
- [ ] Ridisegnare schema DB: ogni entità viaggio è un "oggetto verificabile" con `source`, `rules`, `constraints`, `status`, `verified_at`, `confidence_score`.
  - **Agente:** `@database-architect` | Skills: `database-design`
  - DoD: Schema SQL in `supabase/migrations/` con entity: `trips`, `trip_items` (POI/volo/hotel/attività), `bookings`, `documents`, `collaborators`, `expenses`.
- [ ] Creare tabelle per il sistema di provenance: `sources`, `price_snapshots`, `verification_logs`.
  - **Agente:** `@database-architect` | Skills: `database-design`
  - DoD: Ogni prezzo/orario ha source e timestamp tracciabile.
- [ ] Migrare dati legacy (`trip_pois` → `trip_items` con nuova struttura).
  - **Agente:** `@backend-specialist` | Skills: `database-design`, `nodejs-best-practices`
  - DoD: Migration script + rollback testati, zero data loss.

### A3. API Layer — Unified Backend Services
- [ ] Progettare API layer con pattern "Service → Repository → DB" per tutti i domain.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - DoD: Service interfaces definite per: `TripService`, `BookingService`, `DocumentService`, `CollaborationService`, `ExpenseService`.
- [ ] Implementare Supabase Edge Functions per operazioni server-side (parsing, proxy API esterne, webhook).
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - DoD: Edge functions deployate e funzionanti.

### A4. State Management Overhaul
- [ ] Refactoring stato globale: separare `tripStore`, `uiStore`, `collaborationStore`, `bookingStore`, `offlineStore`.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`
  - DoD: Stores separati, zero `any` types, devtools funzionanti.

### A5. Design System 2.0 — "Cockpit Rilassante"
- [ ] Ridisegnare design system completo: palette "premium but calm", spacing, elevation, motion tokens.
  - **Agente:** `@frontend-specialist` | Skills: `ui-ux-pro-max`, `frontend-design`
  - DoD: CSS custom properties documentate, Storybook/demo page con tutti i componenti.
- [ ] Implementare dark mode nativo + temi "Giorno/Notte/Auto".
  - **Agente:** `@frontend-specialist` | Skills: `frontend-design`
  - DoD: Toggle funzionante, zero flash al caricamento.

---

## Phase B — Inbox-to-Plan Engine (Powered by Custom AI Gateway)
> **🎯 Supervisore:** `@orchestrator` (skills: `parallel-agents`)
> **Obiettivo:** Trasformare input in piani usando custom AI agents in `orbita-bridge` (OpenRouter + Zod) — implementati in A0.3.

### B1. AI Pipelines ✅ *Superseded by A0.3.1 (Parser Agent) & A0.3.3 (Enrichment Agent)*
> I workflow AI sono ora custom endpoints in `orbita-bridge`, non più Flowise Blueprints.
> - Parser: `POST /api/agents/parse` → vedi A0.3.1
> - Enrichment: `POST /api/agents/enrich` → vedi A0.3.3
> - Supervisor Loop: → vedi A0.3.2

### B2. The Bridge (Direct AI Gateway) ✅ *Superseded by A0.3.4 (Frontend Service Layer)*
> `orbita-bridge` **è** l'AI gateway diretto — nessun proxy a servizi esterni.
> - Service layer frontend: `aiService.ts` + React hooks → vedi A0.3.4
> - Type-safe con Zod schemas condivisi tra bridge e web

### B3. UI "Drop Zone" & Verification
- [ ] UI Frontend per input AI:
  - Area drag&drop / paste in `apps/orbita-web`.
  - Visualizzazione stato "AI Thinking..." (Spinner con step: "Leggo...", "Ragiono...", "Formatto...").
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `ui-ux-pro-max`
  - DoD: L'utente incolla un testo grezzo e vede apparire le card dei POI.

## Phase C — Map-to-Decide (Pianificazione Visiva & Collaborativa)
> **🎯 Supervisore:** `@product-manager` (skills: `plan-writing`, `brainstorming`)
> **Obiettivo:** UX map-first con timeline interattiva, collaborazione real-time e ottimizzazione spaziale.

### C1. Interactive Timeline + Map (Il "Cockpit")
- [ ] Riscrivere `MapPlanner` → `OrbitaMap`: mappa full-viewport con overlay timeline laterale manipolabile.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `frontend-design`, `ui-ux-pro-max`
  - DoD: Mappa + timeline a split-view, ogni blocco draggable con resize, constraint visibili.
- [ ] Implementare drag&drop bidirezionale: Timeline ↔ Mappa (drop su mappa = assegna posizione, drop su timeline = assegna giorno/ora).
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`
  - DoD: Drag funziona in entrambe le direzioni con animazione fluida.
- [ ] Simulazione tempi/costi live: al drag, ricalcola tempo di spostamento e costo giornaliero.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `performance-profiling`
  - DoD: Tempo e costo aggiornati in <200ms durante il drag.

### C2. Route Optimization Engine
- [ ] Creare `RoutingService` avanzato: OSRM/Valhalla per calcolo rotte multi-modal (auto, piedi, bici, trasporto pubblico).
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`
  - DoD: Rotte renderizzate su mappa con tempo stimato per segmento.
- [ ] Implementare ottimizzazione ordine visite (TSP semplificato) per minimizzare tempo di percorrenza giornaliero.
  - **Agente:** `@backend-specialist` | Skills: `nodejs-best-practices`
  - DoD: Bottone "Ottimizza percorso" riordina i POI del giorno e mostra il risparmio.

### C3. Real-Time Collaboration
- [ ] Implementare Supabase Realtime per sync collaborativo: cursor presence, "chi ha cambiato cosa", conflict resolution.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `database-design`
  - DoD: 2 utenti vedono le modifiche dell'altro in <1s, change history visibile.
- [ ] UI collaborazione: avatar presenze, sidebar "Activity Feed", notifiche in-app per modifiche.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `frontend-design`
  - DoD: Avatar visibili su mappa/timeline, feed aggiornato in real-time.
- [ ] Gestione permessi: Owner, Editor, Viewer con invito via link/email.
  - **Agente:** `@backend-specialist` | Skills: `database-design`, `api-patterns`
  - DoD: RLS policies per ruoli, UI invito funzionante.

### C4. Split Spese Nativo
- [ ] Creare `ExpenseService`: CRUD spese legate a trip_items, divisione equa/custom tra collaboratori.
  - **Agente:** `@backend-specialist` | Skills: `database-design`, `api-patterns`
  - DoD: Tabella `expenses` con splitType (equal/percentage/custom), calcolo saldi.
- [ ] UI spese: card spesa per item, dashboard saldi "chi deve a chi", summary esportabile.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `ui-ux-pro-max`
  - DoD: Dashboard funzionante, bottone export PDF/CSV.

---

## Phase D — Plan-to-Book (Unified Cart & Checkout)
> **🎯 Supervisore:** `@product-owner` (skills: `plan-writing`, `brainstorming`)
> **Obiettivo:** Carrello unico multi-provider, checkout senza uscire dall'ecosistema, condizioni trasparenti.

### D1. Provider Integration Layer
- [ ] Progettare `ProviderAdapter` interface: standard per integrare API di voli, hotel, treni, attività, assicurazioni.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - DoD: Adapter interface con metodi `search()`, `book()`, `cancel()`, `getStatus()`.
- [ ] Implementare primi adapter: Flights (Amadeus/Kiwi), Hotels (Booking affiliate), Activities (Viator/GetYourGuide).
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - DoD: Ricerca funzionante per almeno 1 provider per categoria.

### D2. Unified Cart
- [ ] Creare `CartService` + `CartStore`: carrello multi-item con pricing aggregato, fee breakdown, condizioni cancellazione per item.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `database-design`
  - DoD: Carrello persiste su DB, mostra totale + breakdown per provider.
- [ ] UI Carrello: sidebar/modal con items raggruppati per giorno, policy leggibili, "Partner Shield" indicator.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `ui-ux-pro-max`
  - DoD: Carrello visivamente polished, cancellation terms leggibili.

### D3. Checkout & Booking Flow
- [ ] Implementare checkout multi-step: conferma dati → pagamento → conferme normalizzate nel Vault.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - DoD: Flow completo demo (sandbox/test mode con dati simulati).
- [ ] "Partner Shield": se redirect necessario, alert pre-redirect con prezzo/condizioni bloccati + deep-link di ritorno.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `frontend-design`
  - DoD: Modal informativo pre-redirect, return URL gestito.

### D4. Price & Policy Clarity
- [ ] Ogni item mostra: prezzo originale, fee, condizioni cancellazione, fonte, ultimo aggiornamento, "confidence" score.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `frontend-design`
  - DoD: Card item con sezione collapsible "Dettagli & Condizioni".
- [ ] Price watch: notifica se prezzo di un item nel carrello cambia prima del checkout.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`
  - DoD: Cron/webhook che confronta prezzi e invia notifica push.

---

## Phase E — Trip Vault (Offline-First & Documenti)
> **🎯 Supervisore:** `@orchestrator` (skills: `parallel-agents`, `behavioral-modes`)
> **Obiettivo:** Cache cifrata locale di tutto il necessario, zero dipendenza da rete in viaggio.

### E1. Offline-First Architecture
- [ ] Implementare Service Worker avanzato con cache strategy "Network-first per sync, Cache-first per lettura".
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `performance-profiling`
  - DoD: App caricabile e navigabile offline, sync automatico al ritorno online.
- [ ] IndexedDB storage per: itinerario completo, documenti, QR codes, contatti emergenza.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`
  - DoD: Dati accessibili offline, cifratura AES-256 a riposo.

### E2. Document Vault
- [ ] Creare `VaultService`: upload, storage (Supabase Storage), categorizzazione automatica di documenti (passaporto, biglietto, conferma, assicurazione).
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `database-design`
  - DoD: Upload + preview + download funzionanti, tagging automatico.
- [ ] UI Vault: sezione "Documenti" con card per tipo, QR preview, ricerca, 1-tap export (PDF bundle / Apple Wallet / Google Wallet).
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `ui-ux-pro-max`
  - DoD: Vista documenti esteticamente premium, export funzionante.

### E3. Emergency Access Mode
- [ ] Modalità "Emergenza": schermata con numeri prenotazione, contatti hotel, ambasciata, assicurazione — accessibile con un tap anche se l'app è in crash parziale.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `mobile-design`
  - DoD: Pagina statica cached con info critiche, funziona anche con JS disabilitato.

---

## Phase F — Disruption Autopilot
> **🎯 Supervisore:** `@product-manager` (skills: `plan-writing`, `brainstorming`)
> **Obiettivo:** Quando il viaggio cambia (volo cancellato, ritardo, meteo), l'app propone soluzioni e aggiorna tutto.

### F1. Real-Time Alert System
- [ ] Integrare flight status API (FlightAware/AviationStack) per push notification: ritardi, cancellazioni, cambio gate, nastro bagagli.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - DoD: Notifiche push entro 2min dall'evento, più veloci della compagnia aerea.
- [ ] Weather alert integration per destinazione: previsioni a 48h integrate nella timeline.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`
  - DoD: Icona meteo su ogni giorno/slot della timeline.

### F2. Replan Engine
- [ ] "Disruption Autopilot": dato un evento (volo spostato +3h), ricalcola automaticamente: transfer hotel, check-in time, attività del giorno.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - DoD: Proposta di piano aggiornato con diff visuale "prima/dopo".
- [ ] Proposta rebooking: se volo cancellato, mostra alternative disponibili con differenza prezzo/tempo.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`
  - DoD: Lista alternative ordinate per "minor disruption", 1-click rebook.
- [ ] Notifica ai collaboratori: aggiornamento automatico del piano condiviso + messaggio "Il piano è cambiato".
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `database-design`
  - DoD: Tutti i collaboratori vedono il nuovo piano in <30s.

### F3. Disruption History & Hybrid Support
- [ ] Log completo disruption: cosa è cambiato, quando, azione presa (auto o manuale).
  - **Agente:** `@backend-specialist` | Skills: `database-design`
  - DoD: Timeline eventi consultabile nell'app.
- [ ] "Hybrid Support": triage AI per problemi comuni + escalation a supporto umano reale con SLA espliciti (< 15 min in disruption attiva).
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - DoD: Chat in-app con routing AI/umano, log legato all'item prenotato.

---

## Phase G — AI con Guardrails Verificabili
> **🎯 Supervisore:** `@security-auditor` (skills: `vulnerability-scanner`, `red-team-tactics`)
> **Obiettivo:** L'AI suggerisce SOLO usando fonti citate e regole. Zero allucinazioni silenziose. L'AI controlla se stessa prima di rispondere.

### G0. Supervisor Loop Check ✅ *Moved to A0.3.2*
> Il self-checking loop è implementato direttamente in `parseWithSupervisor()` dentro `orbita-bridge`.
> - Parser Agent genera JSON → Supervisor Agent valida (schema-compliant, realistico, completo)
> - Retry con feedback se confidence < 0.7 (max 2 tentativi)
> - Vedi **A0.3.2** per dettagli implementativi e DoD.

### G1. AI Guardrails Engine
- [ ] Implementare `GuardrailService`: ogni suggestion AI ha `source_url`, `confidence_score`, `last_verified_at`. Se manca, marcato "⚠️ Da verificare".
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - DoD: Nessuna info AI mostrata senza provenance metadata.
- [ ] Vincoli "hard": budget massimo, mobilità ridotta, dieta, allergie — l'AI non può ignorarli.
  - **Agente:** `@backend-specialist` | Skills: `nodejs-best-practices`
  - DoD: Test che verifica violazione vincoli = errore, non suggerimento.

### G2. Trust Layer (Recensioni Verificabili)
- [ ] Aggregare recensioni multi-fonte pesando: prenotazione verificata > geolocalizzazione > reputazione account > anonimo.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `database-design`
  - DoD: Score composito visibile, badge "Verificato".
- [ ] UI "Ispirazione vs Decisione": separare contenuto aspirazionale (foto, video) da dato decisionale (prezzo, orari, reviews verificate).
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `ui-ux-pro-max`
  - DoD: Tab/toggle che separa le due viste nel dettaglio POI.

---

## Phase H — Privacy, Security & Regional Modes
> **🎯 Supervisore:** `@security-auditor` (skills: `vulnerability-scanner`, `red-team-tactics`)
> **Obiettivo:** Privacy by default, zero vendita dati, supporto pagamenti/lingue/canali regionali.

### H1. Privacy by Default
- [ ] Audit completo permessi: localizzazione opzionale, nessun tracking cross-app, zero vendita dati.
  - **Agente:** `@security-auditor` | Skills: `vulnerability-scanner`
  - DoD: Privacy policy generata, permessi minimi verificati.
- [ ] Cifratura end-to-end per documenti nel Vault.
  - **Agente:** `@security-auditor` | Skills: `vulnerability-scanner`, `red-team-tactics`
  - DoD: Documenti cifrati at-rest e in-transit, key management documentato.
- [ ] GDPR/CCPA compliance: export dati utente 1-click, cancellazione account con purge completo.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - DoD: Endpoint `/me/export` e `/me/delete` funzionanti e testati.

### H2. Regional Modes
- [ ] Supporto pagamenti regionali: rate/cuotas (LATAM), Mada (ME), wallet locali.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`
  - DoD: Almeno 1 payment gateway regionale integrato in sandbox.
- [ ] Canali comunicazione regionali: conferme via WhatsApp, WeChat, SMS in base alla regione.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - DoD: WhatsApp Business API integrato per conferme.
- [ ] i18n completa: almeno IT, EN, ES, AR, ZH-CN con RTL support.
  - **Agente:** `@frontend-specialist` | Skills: `i18n-localization`, `react-patterns`
  - DoD: Cambio lingua funzionante, layout RTL corretto per AR.

### H3. Security Hardening
- [ ] Penetration test completo su API e frontend.
  - **Agente:** `@penetration-tester` | Skills: `red-team-tactics`
  - DoD: Report vulnerabilità con 0 critical/high aperte.
- [ ] RLS audit completo su tutte le nuove tabelle.
  - **Agente:** `@security-auditor` | Skills: `vulnerability-scanner`, `database-design`
  - DoD: Ogni tabella ha policy RLS testate.

---

## Phase I — Pricing Fair-by-Design
> **🎯 Supervisore:** `@product-owner` (skills: `plan-writing`, `brainstorming`)
> **Obiettivo:** Funzioni di sicurezza SEMPRE gratuite. Monetizzazione etica su comfort/premium.

### I1. Tier System
- [ ] Definire tier: **Free** (offline, export, documenti, 3 viaggi attivi) → **Pro** (viaggi illimitati, ottimizzazione avanzata, concierge AI, price-lock) → **Team** (collaborazione avanzata, split spese, branding).
  - **Agente:** `@product-owner` | Skills: `plan-writing`, `brainstorming`
  - DoD: Pricing page documentata, feature matrix chiara.
- [ ] Implementare subscription logic (Stripe) con transparent billing, no auto-renew traps.
  - **Agente:** `@backend-specialist` | Skills: `api-patterns`, `nodejs-best-practices`
  - DoD: Stripe integration, cancel 1-click, email reminder prima di rinnovo.

### I2. Pricing UI
- [ ] Pricing page premium: card tier con comparison matrix, toggle annual/monthly, FAQ.
  - **Agente:** `@frontend-specialist` | Skills: `ui-ux-pro-max`, `frontend-design`
  - DoD: Pagina visivamente premium, zero dark patterns.

---

## Phase J — Mobile-First & Cross-Platform
> **🎯 Supervisore:** `@orchestrator` (skills: `parallel-agents`, `behavioral-modes`)
> **Obiettivo:** App che si sente nativa su ogni device.

### J1. Responsive Redesign
- [ ] Breakpoint system (375px / 768px / 1024px+) con mixins SCSS.
  - **Agente:** `@frontend-specialist` | Skills: `frontend-design`
  - DoD: Mixins documentati, 0 overflow a 375px.
- [ ] Bottom Navigation mobile, slide-up sheets, gesture support (swipe per giorni).
  - **Agente:** `@frontend-specialist` | Skills: `mobile-design`, `react-patterns`
  - DoD: Navigazione mobile nativa-like.
- [ ] Touch targets ≥ 44px, tap areas ottimizzate.
  - **Agente:** `@frontend-specialist` | Skills: `mobile-design`
  - DoD: Lighthouse Accessibility > 95.

### J2. PWA Enhancement
- [ ] Full PWA: installabile, splash screen, push notifications, background sync.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `performance-profiling`
  - DoD: App installabile da Chrome/Safari, notifiche push funzionanti.

### J3. React Native Shell (Future)
- [ ] Predisporre React Native wrapper per accesso a: camera (scan documenti), contatti, calendario nativo.
  - **Agente:** `@mobile-developer` | Skills: `mobile-design`
  - DoD: PoC con webview + bridge nativo per camera.

---

## Phase K — Performance, SEO & Observability
> **🎯 Supervisore:** `@performance-optimizer` (skills: `performance-profiling`)
> **Obiettivo:** App velocissima, indicizzabile, monitorata.

### K1. Performance Optimization
- [ ] Bundle splitting: lazy-load per route, code-split per feature (mappa, editor, checkout).
  - **Agente:** `@performance-optimizer` | Skills: `performance-profiling`
  - DoD: Initial bundle < 200KB gzipped, LCP < 2s.
- [ ] Ottimizzare rendering mappa: virtualizzazione markers, cluster dinamico, tile preloading.
  - **Agente:** `@performance-optimizer` | Skills: `performance-profiling`
  - DoD: Mappa fluida con 500+ markers.
- [ ] Image optimization: WebP/AVIF auto-conversion, lazy loading, CDN.
  - **Agente:** `@performance-optimizer` | Skills: `performance-profiling`
  - DoD: Nessuna immagine > 100KB in viewport critico.

### K2. SEO & Discoverability
- [ ] SSR/SSG per pagine pubbliche (landing, trip pubblici, prezzi) via framework upgrade o prerendering.
  - **Agente:** `@seo-specialist` | Skills: `seo-fundamentals`, `geo-fundamentals`
  - DoD: Core Web Vitals verdi, meta tags dinamici, structured data.
- [ ] Sitemap, robots.txt, Open Graph per share social dei trip pubblici.
  - **Agente:** `@seo-specialist` | Skills: `seo-fundamentals`
  - DoD: Link condiviso mostra preview card su social.

### K3. Observability & Monitoring
- [ ] Sentry integration per error tracking, performance monitoring, session replay.
  - **Agente:** `@devops-engineer` | Skills: `deployment-procedures`, `server-management`
  - DoD: Dashboard errori attiva, alert su spike.
- [ ] Analytics privacy-friendly (Plausible/Umami) per metriche prodotto.
  - **Agente:** `@devops-engineer` | Skills: `deployment-procedures`
  - DoD: Dashboard metriche senza cookie tracking.

---

## Phase L — Testing & Quality Assurance
> **🎯 Supervisore:** `@test-engineer` (skills: `testing-patterns`, `tdd-workflow`, `webapp-testing`)
> **Obiettivo:** Coverage completa, CI/CD robusto, zero regressioni.

### L1. Unit & Integration Tests
- [ ] Test suite per tutti i service: `ParserService`, `RoutingService`, `CartService`, `VaultService`, `GuardrailService`.
  - **Agente:** `@test-engineer` | Skills: `testing-patterns`, `tdd-workflow`
  - DoD: Coverage > 80% sui service critici.
- [ ] Component tests per UI complessi: `OrbitaMap`, `Timeline`, `Cart`, `Vault`.
  - **Agente:** `@test-engineer` | Skills: `testing-patterns`, `react-patterns`
  - DoD: Snapshot + interaction tests per ogni componente.

### L2. E2E Tests
- [ ] Playwright suite per core journeys: "Incolla link → Piano generato → Checkout → Documento nel Vault".
  - **Agente:** `@qa-automation-engineer` | Skills: `webapp-testing`
  - DoD: Suite E2E in CI, green su ogni PR.
- [ ] Test disruption flow: "Volo cancellato → Alert → Replan → Notifica collaboratori".
  - **Agente:** `@qa-automation-engineer` | Skills: `webapp-testing`
  - DoD: Flow testato end-to-end con mocked API.

### L3. CI/CD Pipeline
- [ ] GitHub Actions: lint → typecheck → unit tests → build → E2E → deploy preview.
  - **Agente:** `@devops-engineer` | Skills: `deployment-procedures`
  - DoD: Pipeline completa, deploy automatico su merge a main.

---

## Phase M — Documentation & Launch
> **🎯 Supervisori:** `@documentation-writer`, `@devops-engineer` (skills: `documentation-templates`)
> **Obiettivo:** Documentazione completa per utenti, sviluppatori e contributor.

### M1. Developer Documentation
- [ ] README completo: setup, architettura, contributing guide, ADR index.
  - **Agente:** `@documentation-writer` | Skills: `documentation-templates`
  - DoD: Nuovo dev operativo in <30 min.
- [ ] API documentation per Edge Functions ed endpoint interni.
  - **Agente:** `@documentation-writer` | Skills: `documentation-templates`
  - DoD: Swagger/OpenAPI spec generata.

### M2. User-Facing Content
- [ ] Onboarding flow in-app: tutorial interattivo per nuovi utenti (3 step max).
  - **Agente:** `@frontend-specialist` | Skills: `ui-ux-pro-max`, `frontend-design`
  - DoD: Onboarding completo con skip, non riappare dopo completamento.
- [ ] Help center: FAQ, video tutorial per feature principali.
  - **Agente:** `@documentation-writer` | Skills: `documentation-templates`
  - DoD: Almeno 10 articoli + 3 video tutorial.

### M3. Unified CD Pipeline
- [ ] Configurazione Vercel (Web & Bridge):
  - Connect Git Repo.
  - Root directory: `apps/orbita-web` e `apps/orbita-bridge`.
  - Env Vars: `NEXT_PUBLIC_SUPABASE_URL`, `OPENROUTER_API_KEY`, `TAVILY_API_KEY`.
  - **Agente:** `@devops-engineer` | Skills: `deployment-procedures`
  - DoD: Push su main -> Deploy automatico di Frontend e AI Gateway.
  - *Nota: deploy dettagliato in A0.3.7 (Deployment Configuration)*

---

> **📊 Totale Fasi:** 13 (A-M) | **Agenti Coinvolti:** 13/20 | **Skills Attivate:** 25+
> **Priorità di esecuzione:** A → B → C → E → G → D → F → H → I → J → K → L → M
