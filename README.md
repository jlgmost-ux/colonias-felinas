# Proyecto Colonias Felinas

> **Estado:** fase inicial · julio 2025  
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

- Registrar **colonias** y **gatos** de forma estandarizada.  
- Compartir datos bajo licencias libres.  
- Medir el **progreso CER** con paneles de analítica.

---

## 3 · Alcance del MVP (v0.1)

| Módulo | Qué hará | Para qué servirá |
|--------|----------|------------------|
| **Catastro** | Alta / consulta de colonias con localización y tamaño aproximado. | Saber dónde y cuántos. |
| **Censo** | Alta / consulta de gatos (sexo, edad, esterilizado, etc.). | Seguir individuos. |
| **Eventos** | Registrar capturas, esterilizaciones, bajas y controles sanitarios. | Historial CER. |
| **Analítica (fase posterior)** | • Paneles de tendencia CER (esterilizaciones realizadas, ratio M/F, colonias activas)<br>• Mapas de densidad de colonias y “puntos calientes” de sobrepoblación | Priorizar intervenciones y evaluar impacto |

---

## 4 · Tecnologías confirmadas

- **Backend** → FastAPI (Python)  
- **Base de datos** → PostgreSQL + PostGIS (geo-queries)  
- **Frontend** → SvelteKit (SPA / PWA)  
- **Contenedores** → Docker Compose (entorno reproducible)

---

## 5 · Identificación automática (idea preliminar)

En fases posteriores se estudiará cómo **identificar ejemplares sin duplicados**, combinando:

- **Reconocimiento visual** mediante modelos ML entrenados con fotografías.  
- **Lectores RFID** (ISO-11784/11785) instalados, por ejemplo, en comederos o durante capturas.

El objetivo es detectar gatos nuevos (posibles extraviados o recién llegados) y mantener estadísticas coherentes.

---

## 6 · Próximos pasos

1. Publicar **esquema de datos** inicial (colonias, gatos, eventos).  
2. Configurar PostGIS y migraciones básicas.  
3. Exponer endpoint “Crear colonia”.  
4. Sembrar datos de prueba.  
5. Mostrar primeras colonias en un mapa.

---

## 7 · Participar

El proyecto es personal por ahora, pero se mantendrá **público** bajo licencias libres para que cualquiera pueda revisarlo o bifurcarlo. Cuando el MVP sea estable se invitará a protectoras piloto.

---

## 8 · Licencias

- **Código:** MIT  
- **Esquemas y documentación:** CC BY-SA 4.0
