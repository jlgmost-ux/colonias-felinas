# Proyecto Colonias Felinas

> **Estado:** desarrollo activo · octubre 2025  
> **Propósito:** facilitar y unificar la gestión de colonias felinas mediante una herramienta abierta, sencilla y centrada en los voluntarios.

---

## 1 · Problema y brechas actuales

1. **Datos dispersos** → cada ayuntamiento o protectora usa su propia hoja o app.  
2. **Sin estándar** → los registros no coinciden, impidiendo consolidar información.  
3. **Sin coordinación** → los turnos de alimentación y seguimiento se organizan manualmente (WhatsApp, notas, etc.).  
4. **Cumplimiento legal incierto** → la Ley 7/2023 exige censos y gestión CER, pero las herramientas municipales son limitadas.

---

## 2 · Visión del proyecto

Una plataforma **abierta, gratuita y extensible** donde voluntarios, protectoras y ayuntamientos puedan:

- Registrar **colonias**, **gatos**, **turnos** y **eventos CER** de forma estandarizada.  
- Coordinar de manera sencilla **los días de alimentación** entre cuidadores.  
- Registrar avistamientos o incidencias desde el móvil.  
- Compartir datos con transparencia bajo licencias libres.  
- Medir el **progreso del método CER** de manera colaborativa.

> ⚙️ La prioridad actual es crear herramientas **útiles y fáciles** para los cuidadores — personas que, muchas veces sin formación técnica, sostienen el día a día de las colonias.

---

## 3 · Alcance actual (v0.4)

| Módulo | Estado actual | Para qué sirve |
|--------|---------------|----------------|
| **Colonias** | Alta / consulta de colonias con datos básicos. | Localizar puntos de alimentación y seguimiento. |
| **Gatos** | Alta / consulta de gatos asociados a cada colonia. | Llevar control de individuos y su historial. |
| **Eventos CER** | Registro de capturas, esterilizaciones, controles y bajas. | Documentar el avance del método CER. |
| **Usuarios y roles** | Sistema con roles (`admin`, `coordinador`, `voluntario`). | Controlar accesos y permisos. |
| **Asignaciones** | Relación entre usuarios y colonias (`UserColonia`). | Saber quién cuida qué colonia. |
| **Turnos de alimentación** | Calendario de días asignados a voluntarios, con creación, listado y eliminación desde web. | Coordinar las rondas de alimentación fácilmente. |
| **Frontend** | Navegación simple con vistas `/colonias` y `/colonias/[id]`; página de turnos con formulario interactivo. | Usabilidad adaptada a personas con baja experiencia digital. |
| **Asistencias (futuro)** | Pase de lista de gatos (avistamientos e incidencias). | Verificar presencia y bienestar. |
| **Analítica (futuro)** | Paneles y mapas con métricas CER. | Evaluar impacto real. |

---

## 4 · Tecnologías confirmadas

| Capa | Herramienta |
|------|-------------|
| Backend | **FastAPI** · Python 3.10 |
| Base de datos | **PostgreSQL 16 + PostGIS** |
| ORM / Migraciones | **SQLModel + Alembic** |
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

# crear usuario admin inicial
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

> 💡 Recuerda iniciar Docker si usas PostgreSQL en contenedor.  
> Si `localhost:8000` o `localhost:5173` no responden, comprueba que Docker esté activo.

---

## 6 · Próximos pasos

| Estado | Hito |
|--------|------|
| ✅ | Modelos completos y migraciones actualizadas (`TurnoAlimentacion`, `User`, `UserColonia`). |
| ✅ | Endpoints funcionales para calendario de turnos (`GET/POST/DELETE /turnos`). |
| ✅ | Listado de usuarios asignados a cada colonia (`GET /users?colonia_id`). |
| ✅ | Frontend operativo para crear y eliminar turnos con interfaz simplificada. |
| 🔜 | Proteger endpoints restantes con autenticación JWT y roles. |
| 🔜 | Implementar logout y mostrar usuario autenticado en la interfaz. |
| 🔜 | Desarrollar pase de lista de gatos (“Asistencias”) desde frontend. |
| 🔜 | Añadir soporte offline y sincronización móvil. |
| 🔜 | Dockerizar backend y base de datos. |
| 🔜 | Integrar CI/CD con GitHub Actions. |

---

## 7 · Enfoque de diseño

- **Prioridad humana** → pensado para voluntarios mayores o con pocos conocimientos digitales.  
- **Simplicidad** → menos clics, más legibilidad, sin pantallas innecesarias.  
- **Colaboración abierta** → código libre y documentación pública.  
- **Escalabilidad futura** → preparada para extender módulos sin romper compatibilidad.

---

## 8 · Participar

El proyecto es personal por ahora, pero se mantendrá **público y abierto** bajo licencias libres para revisión o bifurcación.  
Cuando el MVP sea estable se invitará a protectoras piloto para pruebas en campo.

---

## 9 · Licencias

- **Código:** MIT  
- **Esquemas y documentación:** CC BY-SA 4.0  

---

## 10 · Ideas e inspiración futura

- Identificación automática de gatos mediante **visión por computador**.  
- **Lectores RFID** en puntos de alimentación o durante capturas.  
- Integración con plataformas municipales para sincronizar censos.  
- Exportación de informes PDF/Excel para ayuntamientos.  
- Dashboard público con métricas CER.  
- Gamificación ligera (ranking de alimentadores, logros por colonia).  
- Notificaciones automáticas (avisos, recordatorios de turnos).  
