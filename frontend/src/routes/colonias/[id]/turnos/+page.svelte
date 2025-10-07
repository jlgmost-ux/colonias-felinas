<script lang="ts">
    import { crearTurno, eliminarTurno, type Turno, type User } from "$lib/api";

    export let data: {
        coloniaId: string;
        turnos: Turno[];
        users: User[];
    };

    let { coloniaId, turnos, users } = data;

    /* =========================
       🗓️ CALENDARIO (NUEVO)
    ========================= */
    let currentMonth = new Date().getMonth();
    let currentYear = new Date().getFullYear();

    function nextMonth() {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
    }
    function prevMonth() {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
    }
    function getDaysInMonth(year: number, month: number) {
        const days: (number | null)[] = [];
        const first = new Date(year, month, 1);
        const offset = (first.getDay() + 6) % 7; // L=0..D=6
        for (let i = 0; i < offset; i++) days.push(null);
        const last = new Date(year, month + 1, 0).getDate();
        for (let d = 1; d <= last; d++) days.push(d);
        return days;
    }
    function fmtDate(y: number, m: number, d: number) {
        return `${y}-${String(m + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
    }
    // mapa: fecha -> turno
    $: turnosMap = Object.fromEntries(
        turnos.map((t) => [t.fecha.slice(0, 10), t as Turno]),
    );

    // Modal para crear/editar desde el calendario
    let showModal = false;
    let selectedDate = "";
    let modalUser = "";
    let modalNotas = "";
    let modalTurnoId: string | null = null;
    let creandoModal = false;
    let errorModal = "";

    function openModal(date: string) {
        selectedDate = date;
        errorModal = "";
        const existente = turnosMap[date] as Turno | undefined;
        if (existente) {
            modalUser = existente.user_id;
            modalNotas = existente.notas ?? "";
            modalTurnoId = existente.id;
        } else {
            modalUser = "";
            modalNotas = "";
            modalTurnoId = null;
        }
        showModal = true;
    }

    async function guardarModal() {
        if (!modalUser) {
            errorModal = "Debe seleccionar un usuario";
            return;
        }
        try {
            creandoModal = true;
            // si ya existe, eliminar y recrear (sin endpoint de update)
            if (modalTurnoId) {
                await eliminarTurno(modalTurnoId);
                turnos = turnos.filter((t) => t.id !== modalTurnoId);
            }
            const nuevo = await crearTurno({
                colonia_id: coloniaId,
                user_id: modalUser,
                fecha: selectedDate,
                notas: modalNotas,
            });
            turnos = [...turnos, nuevo].sort((a, b) =>
                a.fecha.localeCompare(b.fecha),
            );
            showModal = false;
        } catch (e) {
            errorModal =
                e instanceof Error ? e.message : "Error guardando turno";
        } finally {
            creandoModal = false;
        }
    }

    async function eliminarModal() {
        if (!modalTurnoId) return;
        const ok = confirm("¿Seguro que deseas eliminar este turno?");
        if (!ok) return;
        try {
            await eliminarTurno(modalTurnoId);
            turnos = turnos.filter((t) => t.id !== modalTurnoId);
            showModal = false;
        } catch {
            errorModal = "No se pudo eliminar el turno";
        }
    }

    /* =========================
	   1) Formulario simple
	========================= */
    let user_id = "";
    let fecha = "";
    let notas = "";
    let error = "";
    let creando = false;

    async function addTurno() {
        if (!user_id || !fecha) {
            error = "Debe seleccionar un usuario y una fecha";
            return;
        }
        creando = true;
        error = "";

        try {
            const d = new Date(fecha);
            const f = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(
                d.getDate(),
            ).padStart(2, "0")}`;
            const nuevo = await crearTurno({
                colonia_id: coloniaId,
                user_id,
                fecha: f,
                notas,
            });
            turnos = [...turnos, nuevo].sort((a, b) =>
                a.fecha.localeCompare(b.fecha),
            );
            user_id = "";
            fecha = "";
            notas = "";
        } catch (e) {
            error = e instanceof Error ? e.message : "Error desconocido";
        } finally {
            creando = false;
        }
    }

    async function removeTurno(id: string) {
        const confirmar = confirm("¿Seguro que deseas eliminar este turno?");
        if (!confirmar) return;
        try {
            await eliminarTurno(id);
            turnos = turnos.filter((t) => t.id !== id);
            // reactividad para el Set
            if (selectedIds.has(id)) {
                selectedIds.delete(id);
                selectedIds = new Set(selectedIds);
            }
        } catch {
            alert("No se pudo eliminar el turno");
        }
    }

    /* =========================
	   2) Formulario recurrente
	========================= */
    let user_id_recurrente = "";
    let diasSemana: number[] = []; // valores nativos de getDay: 0..6 (0=Dom)
    let mesesDuracion: number = 0; // 0=mes actual; 1..3 meses adicionales
    let notas_recurrente = "";
    let creando_recurrente = false;

    const toggleDia = (num: number) => {
        diasSemana = diasSemana.includes(num)
            ? diasSemana.filter((d) => d !== num)
            : [...diasSemana, num];
    };

    async function generarTurnosRecurrentes() {
        if (!user_id_recurrente || diasSemana.length === 0) {
            error = "Selecciona usuario y al menos un día de la semana";
            return;
        }

        creando_recurrente = true;
        error = "";

        try {
            const hoy = new Date();
            hoy.setHours(0, 0, 0, 0);

            // fin = último día del mes actual + mesesDuracion
            const fin = new Date(
                hoy.getFullYear(),
                hoy.getMonth() + mesesDuracion + 1,
                0,
            );
            fin.setHours(0, 0, 0, 0);

            // claves ya existentes (fecha + usuario)
            const existenteKey = new Set(
                turnos.map((t) => `${t.fecha.slice(0, 10)}__${t.user_id}`),
            );

            let creados = 0;
            let conflictos = 0;
            const nuevosTurnos: Turno[] = [];

            for (let d = new Date(hoy); d <= fin; d.setDate(d.getDate() + 1)) {
                if (!diasSemana.includes(d.getDay())) continue;

                const yyyy = d.getFullYear();
                const mm = String(d.getMonth() + 1).padStart(2, "0");
                const dd = String(d.getDate()).padStart(2, "0");
                const fLocal = `${yyyy}-${mm}-${dd}`;
                const key = `${fLocal}__${user_id_recurrente}`;

                if (existenteKey.has(key)) {
                    conflictos++;
                    continue;
                }

                try {
                    const nuevo = await crearTurno({
                        colonia_id: coloniaId,
                        user_id: user_id_recurrente,
                        fecha: fLocal,
                        notas: notas_recurrente,
                    });
                    nuevosTurnos.push(nuevo);
                    existenteKey.add(key);
                    creados++;
                } catch {
                    conflictos++;
                }
            }

            if (creados) {
                turnos = [...turnos, ...nuevosTurnos].sort((a, b) =>
                    a.fecha.localeCompare(b.fecha),
                );
            }

            alert(
                `${creados} turnos creados correctamente.\n${conflictos} turnos en conflicto (ya existían o no se pudieron crear).`,
            );
        } catch (e) {
            error =
                e instanceof Error
                    ? e.message
                    : "Error generando turnos recurrentes";
        } finally {
            creando_recurrente = false;
        }
    }

    /* =========================
	   3) Tabla: selección + orden + paginación
	========================= */
    let selectedIds = new Set<string>();
    let deletingBulk = false;

    function toggleSelect(id: string, checked: boolean) {
        if (checked) selectedIds.add(id);
        else selectedIds.delete(id);
        // reactividad para Svelte
        selectedIds = new Set(selectedIds);
    }

    async function eliminarSeleccionados(rows: ViewRow[]) {
        const ids = rows.filter((r) => selectedIds.has(r.id)).map((r) => r.id);
        if (!ids.length) return;

        const confirmar = confirm(
            `¿Eliminar ${ids.length} turno(s) seleccionado(s)?`,
        );
        if (!confirmar) return;

        deletingBulk = true;
        try {
            await Promise.all(
                ids.map((id) => eliminarTurno(id).catch(() => null)),
            );
            turnos = turnos.filter((t) => !selectedIds.has(t.id));
            selectedIds.clear();
            selectedIds = new Set(selectedIds);
        } catch {
            alert("No se pudieron eliminar algunos turnos");
        } finally {
            deletingBulk = false;
        }
    }

    function monthLabel(ymd: string) {
        const [y, m, d] = ymd.split("-").map(Number);
        return new Intl.DateTimeFormat("es-ES", { month: "long" }).format(
            new Date(y, m - 1, d),
        );
    }
    function yearLabel(ymd: string) {
        return ymd.split("-")[0];
    }

    type SortKey = "fecha" | "mes" | "anio" | "usuario" | "notas";
    let sortKey: SortKey = "fecha";
    let sortAsc = true;

    function setSort(key: SortKey) {
        if (sortKey === key) sortAsc = !sortAsc;
        else {
            sortKey = key;
            sortAsc = true;
        }
    }

    // Chevron uniforme para todas las columnas
    function arrowFor(_key: SortKey) {
        return "↕";
    }

    type ViewRow = Turno & { email: string; mes: string; anio: string };

    function toViewRow(t: Turno): ViewRow {
        const email = users.find((u) => u.id === t.user_id)?.email ?? t.user_id;
        return {
            ...t,
            email,
            mes: monthLabel(t.fecha),
            anio: yearLabel(t.fecha),
        };
    }

    $: viewRows = turnos.map(toViewRow);

    $: sortedRows = [...viewRows].sort((a, b) => {
        let av = "";
        let bv = "";
        switch (sortKey) {
            case "fecha":
                av = a.fecha;
                bv = b.fecha;
                break;
            case "mes":
                av = a.mes;
                bv = b.mes;
                break;
            case "anio":
                av = a.anio;
                bv = b.anio;
                break;
            case "usuario":
                av = a.email;
                bv = b.email;
                break;
            case "notas":
                av = a.notas ?? "";
                bv = b.notas ?? "";
                break;
        }
        const cmp = av.localeCompare(bv, "es");
        return sortAsc ? cmp : -cmp;
    });

    function toggleSelectAll(rows: ViewRow[], checked: boolean) {
        for (const r of rows) {
            if (checked) selectedIds.add(r.id);
            else selectedIds.delete(r.id);
        }
        // reactividad
        selectedIds = new Set(selectedIds);
    }

    function isAllSelected(rows: ViewRow[]) {
        return rows.length > 0 && rows.every((r) => selectedIds.has(r.id));
    }

    /* =========================
	   4) Paginación (40 por página)
	========================= */
    let currentPage = 1;
    const pageSize = 40;

    $: totalPages = Math.max(1, Math.ceil(sortedRows.length / pageSize));
    $: paginatedRows = sortedRows.slice(
        (currentPage - 1) * pageSize,
        currentPage * pageSize,
    );

    function nextPageTable() {
        if (currentPage < totalPages) currentPage++;
    }
    function prevPageTable() {
        if (currentPage > 1) currentPage--;
    }
</script>

<div class="max-w-5xl mx-auto p-6">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-800">
            🗓️ Calendario de alimentación
        </h1>
        <a
            href={`/colonias/${coloniaId}`}
            class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded"
        >
            ← Volver a la colonia
        </a>
    </div>

    <!-- =========================
         CALENDARIO (NUEVO)
    ========================== -->
    <div class="bg-white shadow rounded-lg p-4 mb-6">
        <div class="flex justify-between items-center mb-2">
            <button
                on:click={prevMonth}
                class="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
                >←</button
            >
            <h2 class="font-semibold capitalize">
                {new Intl.DateTimeFormat("es-ES", {
                    month: "long",
                    year: "numeric",
                }).format(new Date(currentYear, currentMonth))}
            </h2>
            <button
                on:click={nextMonth}
                class="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
                >→</button
            >
        </div>
        <div
            class="grid grid-cols-7 text-center font-semibold text-gray-600 border-b mb-1"
        >
            <div>L</div>
            <div>M</div>
            <div>X</div>
            <div>J</div>
            <div>V</div>
            <div>S</div>
            <div>D</div>
        </div>
        <div class="grid grid-cols-7 gap-1 text-center">
            {#each getDaysInMonth(currentYear, currentMonth) as day}
                {#if day === null}
                    <div class="p-2"></div>
                {:else}
                    {@const dateStr = fmtDate(currentYear, currentMonth, day)}
                    {@const t = turnosMap[dateStr] as Turno | undefined}
                    <div
                        class={`p-2 rounded border text-sm cursor-pointer ${
                            t
                                ? "bg-green-100 border-green-400 text-green-800 hover:bg-green-200"
                                : "bg-gray-100 border-gray-300 text-gray-400 hover:bg-gray-200"
                        }`}
                        title={t
                            ? (users.find((u) => u.id === t.user_id)?.email ??
                              t.user_id)
                            : "Sin turno"}
                        on:click={() => openModal(dateStr)}
                    >
                        <div class="font-medium">{day}</div>
                        {#if t}
                            <div class="text-xs mt-1">
                                {(
                                    users.find((u) => u.id === t.user_id)
                                        ?.email ?? t.user_id
                                ).split("@")[0]}
                            </div>
                        {/if}
                    </div>
                {/if}
            {/each}
        </div>
    </div>

    {#if showModal}
        <div
            class="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
        >
            <div class="bg-white p-6 rounded-lg shadow-lg w-96">
                <h3 class="text-lg font-semibold mb-3 text-center">
                    {modalTurnoId ? "Editar turno" : "Asignar turno"}
                </h3>
                <p class="text-sm text-gray-600 mb-3 text-center">
                    Fecha: <strong>{selectedDate}</strong>
                </p>
                {#if errorModal}<p class="text-red-600 mb-2 text-sm">
                        {errorModal}
                    </p>{/if}
                <select
                    bind:value={modalUser}
                    class="border p-2 rounded w-full mb-3"
                >
                    <option value="">Selecciona usuario</option>
                    {#each users as u}<option value={u.id}>{u.email}</option
                        >{/each}
                </select>
                <textarea
                    class="border p-2 rounded w-full mb-3 text-sm"
                    placeholder="Notas (opcional)"
                    rows="2"
                    bind:value={modalNotas}
                ></textarea>
                <div class="flex justify-end gap-2">
                    {#if modalTurnoId}
                        <button
                            class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
                            on:click={eliminarModal}
                            disabled={creandoModal}>Eliminar</button
                        >
                    {/if}
                    <button
                        class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
                        on:click={() => (showModal = false)}>Cancelar</button
                    >
                    <button
                        class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-400"
                        on:click={guardarModal}
                        disabled={creandoModal}
                    >
                        {creandoModal ? "Guardando..." : "Guardar"}
                    </button>
                </div>
            </div>
        </div>
    {/if}

    <!-- =========================
         Formulario simple
    ========================== -->
    <div class="bg-gray-100 p-4 rounded-lg shadow mb-6">
        <h2 class="font-semibold mb-2">Añadir nuevo turno</h2>
        {#if error}<p class="text-red-600 mb-2">{error}</p>{/if}
        <div class="flex flex-wrap gap-2 items-center">
            <select
                bind:value={user_id}
                class="border p-2 rounded flex-1 min-w-[180px]"
            >
                <option value="">Selecciona usuario</option>
                {#each users as u}<option value={u.id}>{u.email}</option>{/each}
            </select>
            <input
                class="border p-2 rounded flex-1 min-w-[160px]"
                type="date"
                bind:value={fecha}
            />
            <input
                class="border p-2 rounded flex-1 min-w-[200px]"
                type="text"
                placeholder="Notas (opcional)"
                bind:value={notas}
            />
            <button
                on:click={addTurno}
                class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
                disabled={creando}
            >
                {creando ? "Guardando..." : "Añadir"}
            </button>
        </div>
    </div>

    <!-- =========================
         Formulario recurrente
    ========================== -->
    <div class="bg-gray-100 p-4 rounded-lg shadow mb-6">
        <h2 class="font-semibold mb-2">Añadir turnos semanales repetidos</h2>
        <div class="flex flex-wrap gap-2 items-center">
            <select
                bind:value={user_id_recurrente}
                class="border p-2 rounded flex-1 min-w-[180px]"
            >
                <option value="">Selecciona usuario</option>
                {#each users as u}<option value={u.id}>{u.email}</option>{/each}
            </select>
            <div class="flex gap-2 items-center">
                <label
                    ><input
                        type="checkbox"
                        checked={diasSemana.includes(1)}
                        on:change={() => toggleDia(1)}
                    /> L</label
                >
                <label
                    ><input
                        type="checkbox"
                        checked={diasSemana.includes(2)}
                        on:change={() => toggleDia(2)}
                    /> M</label
                >
                <label
                    ><input
                        type="checkbox"
                        checked={diasSemana.includes(3)}
                        on:change={() => toggleDia(3)}
                    /> X</label
                >
                <label
                    ><input
                        type="checkbox"
                        checked={diasSemana.includes(4)}
                        on:change={() => toggleDia(4)}
                    /> J</label
                >
                <label
                    ><input
                        type="checkbox"
                        checked={diasSemana.includes(5)}
                        on:change={() => toggleDia(5)}
                    /> V</label
                >
                <label
                    ><input
                        type="checkbox"
                        checked={diasSemana.includes(6)}
                        on:change={() => toggleDia(6)}
                    /> S</label
                >
                <label
                    ><input
                        type="checkbox"
                        checked={diasSemana.includes(0)}
                        on:change={() => toggleDia(0)}
                    /> D</label
                >
            </div>
            <select bind:value={mesesDuracion} class="border p-2 rounded">
                <option value={0}>Mes actual</option>
                <option value={1}>Mes actual +1</option>
                <option value={2}>Mes actual +2</option>
                <option value={3}>Mes actual +3</option>
            </select>
            <input
                class="border p-2 rounded flex-1 min-w-[200px]"
                type="text"
                placeholder="Notas (opcional)"
                bind:value={notas_recurrente}
            />
            <button
                on:click={generarTurnosRecurrentes}
                class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:bg-gray-400"
                disabled={creando_recurrente}
            >
                {creando_recurrente ? "Generando..." : "Generar turnos"}
            </button>
        </div>
    </div>

    <!-- Acciones tabla -->
    <div class="flex items-center gap-2 mb-3">
        <button
            class="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded disabled:bg-gray-400"
            on:click={() => eliminarSeleccionados(paginatedRows)}
            disabled={selectedIds.size === 0 || deletingBulk}
        >
            {deletingBulk
                ? "Eliminando..."
                : `Eliminar seleccionados (${selectedIds.size})`}
        </button>
    </div>

    <!-- Tabla -->
    {#if sortedRows.length}
        <div class="overflow-x-auto bg-white shadow rounded-lg">
            <table class="min-w-full">
                <thead>
                    <tr class="bg-gray-200 text-gray-700">
                        <th class="p-2 w-10 text-left">
                            <input
                                type="checkbox"
                                checked={isAllSelected(paginatedRows)}
                                on:change={(e) =>
                                    toggleSelectAll(
                                        paginatedRows,
                                        (e.target as HTMLInputElement).checked,
                                    )}
                            />
                        </th>
                        <th
                            class="p-2 text-left cursor-pointer select-none"
                            on:click={() => setSort("fecha")}
                        >
                            Fecha <span class="text-xs opacity-70"
                                >{arrowFor("fecha")}</span
                            >
                        </th>
                        <th
                            class="p-2 text-left cursor-pointer select-none"
                            on:click={() => setSort("mes")}
                        >
                            Mes <span class="text-xs opacity-70"
                                >{arrowFor("mes")}</span
                            >
                        </th>
                        <th
                            class="p-2 text-left cursor-pointer select-none"
                            on:click={() => setSort("anio")}
                        >
                            Año <span class="text-xs opacity-70"
                                >{arrowFor("anio")}</span
                            >
                        </th>
                        <th
                            class="p-2 text-left cursor-pointer select-none"
                            on:click={() => setSort("usuario")}
                        >
                            Usuario <span class="text-xs opacity-70"
                                >{arrowFor("usuario")}</span
                            >
                        </th>
                        <th
                            class="p-2 text-left cursor-pointer select-none"
                            on:click={() => setSort("notas")}
                        >
                            Notas <span class="text-xs opacity-70"
                                >{arrowFor("notas")}</span
                            >
                        </th>
                        <th class="p-2"></th>
                    </tr>
                </thead>
                <tbody>
                    {#each paginatedRows as r (r.id)}
                        <tr class="border-t hover:bg-gray-50">
                            <td class="p-2">
                                <input
                                    type="checkbox"
                                    checked={selectedIds.has(r.id)}
                                    on:change={(e) =>
                                        toggleSelect(
                                            r.id,
                                            (e.target as HTMLInputElement)
                                                .checked,
                                        )}
                                />
                            </td>
                            <td class="p-2">{r.fecha.slice(0, 10)}</td>
                            <td class="p-2 capitalize">{r.mes}</td>
                            <td class="p-2">{r.anio}</td>
                            <td class="p-2">{r.email}</td>
                            <td class="p-2">{r.notas || "—"}</td>
                            <td class="p-2 text-right">
                                <button
                                    class="text-red-600 hover:underline"
                                    on:click={() => removeTurno(r.id)}
                                >
                                    Eliminar
                                </button>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>

        <!-- paginación -->
        <div
            class="flex justify-between items-center mt-4 text-sm text-gray-600"
        >
            <button
                class="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
                on:click={prevPageTable}
                disabled={currentPage === 1}
            >
                « Anterior
            </button>
            <span
                >Mostrando {(currentPage - 1) * pageSize + 1}–{Math.min(
                    currentPage * pageSize,
                    sortedRows.length,
                )} de {sortedRows.length}</span
            >
            <button
                class="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
                on:click={nextPageTable}
                disabled={currentPage === totalPages}
            >
                Siguiente »
            </button>
        </div>
    {:else}
        <p class="text-gray-500 mt-4">
            No hay turnos registrados para esta colonia.
        </p>
    {/if}
</div>
