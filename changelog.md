# Changelog

All notable changes to this project are documented in this file.

## [0.2.0] – 2025-07-30
### Added
- **Detail page** `/colonias/[id]` in frontend: card header, colony info panel and styled cats table.  
- **“Add Cat” form** at `/colonias/[id]/gatos/nueva`: fields for sexo, edad, esterilizado, fecha, color y notas, con validación y feedback.  
- **TailwindCSS styling** applied to list, forms and detail views: cards, tables, buttons, inputs.  
- **Leaflet map** in `/colonias` list with markers for each colony, SSR-safe dynamic import and `fitBounds` for auto-zoom.  
- **SSR fix** for Leaflet: component marked `ssr = false` and dynamic import of `leaflet` in `onMount`.  

### Fixed
- CSS import conflicts resolved via `svelte-add tailwindcss`.  
- Validation logic refined in “New Colony” and “Add Cat” forms.

## [0.1.0] – 2025-07-29
### Added
- **Data models** (`Colonia`, `Gato`, `Evento`) defined with SQLModel.  
- **Alembic migrations** set up; initial migration to create tables.  
- **FastAPI endpoints**:
  - `GET /health`
  - `GET/POST /colonias`
  - `GET/POST /gatos`
  - `GET/POST /eventos`  
- **.env** configuration and database connection via `psycopg`.  
- **Basic SvelteKit frontend** scaffolded with:
  - List of colonies (`/colonias`) fetching from API.
  - “New Colony” form at `/colonias/nueva`.  
- **Validation and feedback** added to “New Colony” form.  

---

> **Next versions:**  
> - 0.3.0: Map centered in colony detail  
> - 0.4.0: Docker Compose setup  
