# Changelog

All notable changes to this project are documented in this file.


## v0.3.0 – 2025-09-12

### Backend
- **Modelos**
  - Añadidos modelos `User` y `UserColonia` con roles (`admin`, `coordinador`, `voluntario`).
  - Añadido modelo `Asistencia` para registrar pases de lista:
    - `colonia_id`, `gato_id` (opcional), `descripcion_libre` (para gatos desconocidos).
    - `user_id` (voluntario que pasa lista).
    - `timestamp`, `incidencia`, `notas`, `foto_url`.
- **Migraciones**
  - Reestructuración completa de la base de datos (drop schema + init full schema).
  - Migración limpia con todos los modelos actuales (`Colonia`, `Gato`, `Evento`, `User`, `UserColonia`, `Asistencia`).
- **Semillas**
  - Script `seed_admin.py` para crear usuario administrador inicial (`admin@example.org / changeme`).
- **Autenticación**
  - Implementación de JWT (access y refresh tokens).
  - Endpoints: `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`.
  - Validación de roles y asignaciones a colonias.
- **Asignaciones**
  - Endpoints para asignar y quitar usuarios de colonias:
    - `POST /colonias/{colonia_id}/users/{user_id}`
    - `DELETE /colonias/{colonia_id}/users/{user_id}`
    - `GET /colonias/{colonia_id}/users`
- **Asistencias**
  - Endpoint `POST /asistencias/bulk` para registrar avistamientos (sólo presentes).
  - Endpoint `GET /asistencias` para listar registros (con filtros por colonia y fecha).
  - Validación de asignación: solo usuarios asignados (o admin/coordinador) pueden registrar.
- **Depuración**
  - Corrección de tipos en todos los modelos con `sa_type` para evitar problemas de Alembic (`AutoString`).
  - Ajustes en dependencias (`require_asignado` corregido para `bulk`).

### Frontend (SvelteKit)
- **Login**
  - Página `/login` con formulario básico.
  - Autenticación contra `/auth/login` usando `fetch` y `x-www-form-urlencoded`.
  - Almacena `access_token`, `refresh_token` y `role` en `localStorage`.
  - Redirección según rol:
    - `admin` → `/colonias`
    - `coordinador` o `voluntario` → `/mis-colonias`
- **Colonias**
  - `/colonias`: lista completa (para admin y coordinadores).
  - `/mis-colonias`: nueva página para voluntarios/coordinadores, muestra solo colonias asignadas.
  - Integración con endpoint `GET /mis-colonias`.
  - Añadido mapa con `Map.svelte` para mostrar colonias asignadas en `/mis-colonias`.

### Estado actual
- Backend y base de datos sincronizados, con roles, autenticación y asistencias funcionando.
- Frontend permite login y navegación diferenciada por rol.
- Voluntarios pueden ver sus colonias asignadas y admin todas.
- Preparado para próximos pasos:
  - Proteger endpoints restantes con autenticación/roles.
  - Implementar logout y mostrar usuario conectado en la UI.
  - Añadir página de detalle de colonia con pase de lista desde frontend.


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
