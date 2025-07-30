<script lang="ts">
    import { api } from "$lib/api";
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import { get } from "svelte/store";
    import { tick } from "svelte";

    // Obtenemos el ID de la colonia de la URL
    const { id: colonia_id } = get(page).params;

    // Campos del formulario
    let sexo = "M";
    let edad_estimada = "";
    let esterilizado = false;
    let fecha_registro = new Date().toISOString().slice(0, 10);
    let color = "";
    let notas = "";
    let success = false;

    // Validaciones reactivas
    $: edadNum = parseInt(edad_estimada);
    $: isValid =
        ["M", "F", "desconocido"].includes(sexo) &&
        !isNaN(edadNum) &&
        edadNum >= 0 &&
        /^\d{4}-\d{2}-\d{2}$/.test(fecha_registro);

    // Función de envío
    async function enviar() {
        try {
            await api("/gatos", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    id: crypto.randomUUID(),
                    colonia_id,
                    sexo,
                    edad_estimada: edadNum,
                    esterilizado,
                    fecha_registro,
                    color: color.trim() || undefined,
                    notas: notas.trim() || undefined,
                }),
            });
            success = true;
            await tick();
            setTimeout(() => goto(`/colonias/${colonia_id}`), 1000);
        } catch (e) {
            alert("Error al crear gato: " + e);
        }
    }
</script>

<div class="max-w-md mx-auto mt-8">
    <div class="bg-white shadow-lg rounded-lg overflow-hidden">
        <!-- Encabezado -->
        <div class="bg-indigo-600 p-4">
            <h1 class="text-2xl font-semibold text-white">Añadir gato</h1>
        </div>

        <!-- Cuerpo del card -->
        <div class="p-6">
            {#if success}
                <div
                    class="bg-green-100 border border-green-200 text-green-800 p-3 rounded mb-4"
                >
                    ¡Gato creado con éxito! Redirigiendo…
                </div>
            {/if}

            <form on:submit|preventDefault={enviar} class="space-y-4">
                <!-- Sexo -->
                <div>
                    <label
                        for="sexo"
                        class="block text-sm font-medium text-gray-700 mb-1"
                    >
                        Sexo
                    </label>
                    <select
                        id="sexo"
                        bind:value={sexo}
                        class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                    >
                        <option value="M">Macho</option>
                        <option value="F">Hembra</option>
                        <option value="desconocido">Desconocido</option>
                    </select>
                </div>

                <!-- Edad estimada -->
                <div>
                    <label
                        for="edad"
                        class="block text-sm font-medium text-gray-700 mb-1"
                    >
                        Edad estimada (meses)
                    </label>
                    <input
                        id="edad"
                        type="number"
                        bind:value={edad_estimada}
                        min="0"
                        required
                        class="mt-1 block w-24 border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                    />
                    {#if edad_estimada !== "" && (isNaN(edadNum) || edadNum < 0)}
                        <p class="text-red-600 text-xs mt-1">
                            Edad debe ser ≥ 0.
                        </p>
                    {/if}
                </div>

                <!-- Esterilizado -->
                <div>
                    <label class="inline-flex items-center">
                        <input
                            type="checkbox"
                            bind:checked={esterilizado}
                            class="border-gray-300 rounded shadow-sm focus:ring-indigo-500"
                        />
                        <span class="ml-2 text-gray-700">Esterilizado</span>
                    </label>
                </div>

                <!-- Fecha de registro -->
                <div>
                    <label
                        for="fecha"
                        class="block text-sm font-medium text-gray-700 mb-1"
                    >
                        Fecha de registro
                    </label>
                    <input
                        id="fecha"
                        type="date"
                        bind:value={fecha_registro}
                        required
                        class="mt-1 block w-auto border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                    />
                </div>

                <!-- Color -->
                <div>
                    <label
                        for="color"
                        class="block text-sm font-medium text-gray-700 mb-1"
                    >
                        Color (opcional)
                    </label>
                    <input
                        id="color"
                        type="text"
                        bind:value={color}
                        placeholder="p.ej. atigrado"
                        class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                    />
                </div>

                <!-- Notas -->
                <div>
                    <label
                        for="notas"
                        class="block text-sm font-medium text-gray-700 mb-1"
                    >
                        Notas (opcional)
                    </label>
                    <textarea
                        id="notas"
                        bind:value={notas}
                        rows="3"
                        class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                    ></textarea>
                </div>

                <!-- Botón Guardar -->
                <div class="pt-4">
                    <button
                        type="submit"
                        disabled={!isValid}
                        class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2 rounded-md disabled:opacity-50"
                    >
                        Guardar gato
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
