<script lang="ts">
    import { crearTurno, eliminarTurno, type Turno, type User } from "$lib/api";

    export let data: {
        coloniaId: string;
        turnos: Turno[];
        users: User[];
    };

    let { coloniaId, turnos, users } = data;

    // Campos del formulario
    let user_id = "";
    let fecha = "";
    let notas = "";
    let error = "";
    let creando = false;

    async function addTurno() {
        console.log({ colonia_id: coloniaId, user_id, fecha, notas });
        if (!user_id || !fecha) {
            error = "Debe seleccionar un usuario y una fecha";
            return;
        }

        creando = true;
        error = "";

        try {
            // Convertir la fecha del input a formato ISO estándar (YYYY-MM-DDT00:00:00)
            const fechaISO = new Date(fecha).toISOString().split("T")[0]; // o incluir hora si lo prefieres
            const nuevo = await crearTurno({
                colonia_id: coloniaId,
                user_id,
                fecha: fechaISO,
                notas,
            });
            turnos = [...turnos, nuevo];
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
        } catch {
            alert("No se pudo eliminar el turno");
        }
    }
</script>

<div class="max-w-4xl mx-auto p-6">
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

    <!-- Formulario para crear turno -->
    <div class="bg-gray-100 p-4 rounded-lg shadow mb-6">
        <h2 class="font-semibold mb-2">Añadir nuevo turno</h2>
        {#if error}
            <p class="text-red-600 mb-2">{error}</p>
        {/if}

        <div class="flex flex-wrap gap-2 items-center">
            <!-- Selector de usuario -->
            <select
                bind:value={user_id}
                class="border p-2 rounded flex-1 min-w-[180px]"
            >
                <option value="">Selecciona usuario</option>
                {#each users as u}
                    <option value={u.id}>
                        {u.email}
                    </option>
                {/each}
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

    <!-- Tabla de turnos -->
    {#if turnos.length}
        <table class="min-w-full bg-white shadow rounded-lg">
            <thead>
                <tr class="bg-gray-200 text-gray-700">
                    <th class="p-2 text-left">Fecha</th>
                    <th class="p-2 text-left">Usuario</th>
                    <th class="p-2 text-left">Notas</th>
                    <th class="p-2"></th>
                </tr>
            </thead>
            <tbody>
                {#each turnos as t (t.id)}
                    <tr class="border-t">
                        <td class="p-2">{t.fecha.slice(0, 10)}</td>
                        <td class="p-2">
                            {#if users.find((u) => u.id === t.user_id)}
                                {users.find((u) => u.id === t.user_id)?.email}
                            {:else}
                                {t.user_id}
                            {/if}
                        </td>
                        <td class="p-2">{t.notas || "—"}</td>
                        <td class="p-2 text-right">
                            <button
                                on:click={() => removeTurno(t.id)}
                                class="text-red-600 hover:underline"
                            >
                                Eliminar
                            </button>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    {:else}
        <p class="text-gray-500 mt-4">
            No hay turnos registrados para esta colonia.
        </p>
    {/if}
</div>
