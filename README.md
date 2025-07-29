# Proyecto Colonias Felinas

> **Estado:** MVP en construcción · julio 2025  
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

- Registrar **colonias**, **gatos** y **eventos CER** de forma estandarizada.  
- Compartir datos bajo licencias libres.  
- Medir el **progreso CER** con paneles de analítica.

---

## 3 · Alcance del MVP (v0.1)

| Módulo | Qué hace hoy | Para qué sirve |
|--------|--------------|----------------|
| **Catastro** | Alta / consulta de colonias (endpoints `POST` y `GET`). | Saber dónde y cuántos. |
| **Censo** | Alta / consulta de gatos, vinculados a su colonia. | Seguir individuos. |
| **Eventos** | Registrar capturas, esterilizaciones, controles y bajas. | Historial CER. |
| **Frontend** | Página **/colonias** en SvelteKit que lista colonias. | Primer vistazo web. |
| **Analítica (fase posterior)** | • Paneles de tendencia CER<br>• Mapas de densidad | Priorizar intervenciones y evaluar impacto |

---

## 4 · Tecnologías confirmadas

| Capa | Herramienta |
|------|-------------|
| Backend | **FastAPI** · Python 3.10 |
| Base de datos | **PostgreSQL 16 + PostGIS** |
| ORM / Migraciones | **SQLModel + Alembic** |
| Frontend | **SvelteKit** · TypeScript |
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

# sembrar datos de prueba (3 colonias, ~8 gatos, eventos)
python seed_data.py

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

## 6 · Identificación automática (idea preliminar)

En fases posteriores se estudiará cómo **identificar ejemplares sin duplicados**, combinando:

- **Reconocimiento visual** mediante modelos ML entrenados con fotografías.  
- **Lectores RFID** (ISO-11784/11785) instalados, por ejemplo, en comederos o durante capturas.

El objetivo es detectar gatos nuevos (posibles extraviados o recién llegados) y mantener estadísticas coherentes.

---

## 7 · Próximos pasos

| Estado | Hito |
|--------|------|
| ✅ | Modelos, endpoints básicos y migraciones Alembic |
| ✅ | Seed de datos y página `/colonias` |
| 🔜 | Formulario “Nueva colonia” + detalle `/colonias/[id]` |
| 🔜 | Dockerizar backend + base de datos (`docker-compose.yml`) |
| 🔜 | TailwindCSS y mapa (Leaflet) |
| 🔜 | Autenticación básica (token Bearer) |


---

## 8 · Participar

El proyecto es personal por ahora, pero se mantendrá **público** bajo licencias libres para que cualquiera pueda revisarlo o bifurcarlo. Cuando el MVP sea estable se invitará a protectoras piloto.

---

## 9 · Licencias

- **Código:** MIT  
- **Esquemas y documentación:** CC BY-SA 4.0
