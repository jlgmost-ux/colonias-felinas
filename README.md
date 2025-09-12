# Proyecto Colonias Felinas

> **Estado:** desarrollo activo · septiembre 2025  
> **Propósito:** unificar el censo y la gestión CER de colonias felinas en España.

---

## 1 · Problema y brechas actuales

1. **Datos dispersos** → cada ayuntamiento o protectora usa su propia hoja Excel o app privada.  
2. **Sin estándar** → los campos no coinciden, imposible sumar información.  
3. **Ausencia de analítica** → nadie sabe cuántos gatos hay realmente ni si el CER reduce la población.  
4. **Cumplimiento legal incierto** → la Ley 7/2023 exige registros fiables, pero las herramientas municipales son limitadas.

---

## 2 · Visión del proyecto

Crear una plataforma **abierta, gratuita y extensible** donde voluntarios, protectoras y técnicos municipales puedan:

- Registrar **colonias**, **gatos**, **asistencias** y **eventos CER** de forma estandarizada.  
- Compartir datos bajo licencias libres.  
- Medir el **progreso CER** con paneles de analítica.  
- Garantizar que cada usuario acceda solo a lo que le corresponde (roles y permisos).

---

## 3 · Alcance actual (v0.3)

| Módulo | Estado actual | Para qué sirve |
|--------|---------------|----------------|
| **Catastro** | Alta / consulta de colonias (protegido por login). | Saber dónde y cuántos. |
| **Censo** | Alta / consulta de gatos, vinculados a su colonia. | Seguir individuos. |
| **Eventos** | Registrar capturas, esterilizaciones, controles y bajas. | Historial CER. |
| **Usuarios y roles** | Sistema JWT con roles (`admin`, `coordinador`, `voluntario`). | Control de acceso. |
| **Asignaciones** | Admin asigna voluntarios/coordinadores a colonias. | Gestión de permisos. |
| **Asistencias (pase de lista)** | Registro de avistamientos (con foto, incidencias, notas, “gato desconocido”). | Seguimiento diario. |
| **Frontend** | Login, `/colonias` (admin), `/mis-colonias` (asignadas a voluntario/coordinador), integración de mapa Leaflet. | Primer uso real. |
| **Analítica (fase posterior)** | • Paneles de tendencia CER<br>• Mapas de densidad | Evaluar impacto CER. |

---

## 4 · Tecnologías confirmadas

| Capa | Herramienta |
|------|-------------|
| Backend | **FastAPI** · Python 3.10 |
| Base de datos | **PostgreSQL 16 + PostGIS** |
| ORM / Migraciones | **SQLModel + Alembic** |
| Autenticación | **JWT (access/refresh)** |
| Frontend | **SvelteKit** · TailwindCSS · Leaflet |
| Entorno local | Conda |
| Despliegue futuro | Docker Compose |

---

## 5 · Guía rápida de ejecución local

### 5.1 Backend

```bash
# activar entorno
conda activate colonias
cd backend

# aplicar/actualizar esquema
alembic upgrade head

# crear admin inicial
python seed_admin.py

# lanzar API (http://localhost:8000)
python -m uvicorn main:app --reload
```

### 5.2 Frontend

```bash
cd ../frontend
npm install           # solo la primera vez
npm run dev -- --open # abre http://localhost:5173
```

---

## 6 · Próximos pasos

| Estado | Hito |
|--------|------|
| ✅ | Modelos robustos y migraciones iniciales |
| ✅ | Autenticación con JWT, roles y asignaciones |
| ✅ | Endpoints de pase de lista (`/asistencias`) |
| ✅ | Login frontend con redirección por rol |
| 🔜 | Proteger todos los endpoints con permisos |
| 🔜 | Logout y mostrar usuario autenticado en la UI |
| 🔜 | Página de detalle `/colonias/[id]` con pase de lista desde frontend |
| 🔜 | Soporte offline y sincronización |
| 🔜 | Dockerizar backend + base de datos |
| 🔜 | CI/CD con GitHub Actions |

---

## 7 · Participar

El proyecto es personal por ahora, pero se mantendrá **público** bajo licencias libres para que cualquiera pueda revisarlo o bifurcarlo.  
Cuando el MVP sea estable se invitará a protectoras piloto.

---

## 8 · Licencias

- **Código:** MIT  
- **Esquemas y documentación:** CC BY-SA 4.0  

---

## 9 · Ideas e inspiración futura

- Identificación automática de ejemplares:
  - **Reconocimiento visual** con modelos ML entrenados con fotos.
  - **Lectores RFID** (ISO-11784/11785) en comederos o durante capturas.  
- Integración con plataformas municipales para envío automático de datos.  
- Exportación de informes estadísticos (PDF/Excel).  
- Dashboard público con métricas agregadas.  
- Gamificación para voluntarios (ranking de asistencias, recompensas).  
- Notificaciones automáticas (avisos de incidencias, recordatorios).  
