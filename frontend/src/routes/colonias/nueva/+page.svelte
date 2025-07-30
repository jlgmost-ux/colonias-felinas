<script lang="ts">
  import { api } from "$lib/api";
  import { goto } from "$app/navigation";
  import { tick } from "svelte";

  let nombre = "";
  let lat = "";
  let lon = "";
  let n_gatos_est = "";
  let fecha_alta = new Date().toISOString().slice(0, 10);
  let success = false;

  $: latNum = parseFloat(lat);
  $: lonNum = parseFloat(lon);
  $: gatosNum = parseInt(n_gatos_est);
  $: isValid =
    nombre.trim().length >= 3 &&
    !isNaN(latNum) &&
    latNum >= -90 &&
    latNum <= 90 &&
    !isNaN(lonNum) &&
    lonNum >= -180 &&
    lonNum <= 180 &&
    !isNaN(gatosNum) &&
    gatosNum >= 0 &&
    gatosNum <= 1000 &&
    /^\d{4}-\d{2}-\d{2}$/.test(fecha_alta);

  async function enviar() {
    try {
      await api("/colonias", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nombre: nombre.trim(),
          lat: latNum,
          lon: lonNum,
          n_gatos_est: gatosNum,
          fecha_alta,
        }),
      });
      success = true;
      await tick();
      setTimeout(() => goto("/colonias"), 1500);
    } catch (e) {
      alert("Error al crear colonia: " + e);
    }
  }
</script>

<div class="max-w-md mx-auto mt-8">
  <div class="bg-white shadow-lg rounded-lg overflow-hidden">
    <div class="bg-blue-500 p-4">
      <h1 class="text-2xl font-semibold text-white">Nueva colonia</h1>
    </div>

    <div class="p-6">
      {#if success}
        <div
          class="bg-green-100 border border-green-200 text-green-800 p-3 rounded mb-4"
        >
          ¡Colonia creada con éxito! Redirigiendo…
        </div>
      {/if}

      <form on:submit|preventDefault={enviar} class="space-y-4">
        <!-- Nombre -->
        <div>
          <label
            for="nombre"
            class="block text-sm font-medium text-gray-700 mb-1"
          >
            Nombre
          </label>
          <input
            id="nombre"
            type="text"
            bind:value={nombre}
            required
            minlength="3"
            class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
            placeholder="Ej. Parque Central"
          />
          {#if nombre.trim().length > 0 && nombre.trim().length < 3}
            <p class="text-red-600 text-xs mt-1">Mínimo 3 caracteres.</p>
          {/if}
        </div>

        <!-- Lat/Lon -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label
              for="latitud"
              class="block text-sm font-medium text-gray-700 mb-1"
            >
              Latitud
            </label>
            <input
              id="latitud"
              type="number"
              bind:value={lat}
              step="0.0001"
              min="-90"
              max="90"
              required
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
            />
            {#if lat !== "" && (isNaN(latNum) || latNum < -90 || latNum > 90)}
              <p class="text-red-600 text-xs mt-1">Entre −90 y 90.</p>
            {/if}
          </div>
          <div>
            <label
              for="longitud"
              class="block text-sm font-medium text-gray-700 mb-1"
            >
              Longitud
            </label>
            <input
              id="longitud"
              type="number"
              bind:value={lon}
              step="0.0001"
              min="-180"
              max="180"
              required
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
            />
            {#if lon !== "" && (isNaN(lonNum) || lonNum < -180 || lonNum > 180)}
              <p class="text-red-600 text-xs mt-1">Entre −180 y 180.</p>
            {/if}
          </div>
        </div>

        <!-- Nº gatos estimado -->
        <div>
          <label
            for="gatos"
            class="block text-sm font-medium text-gray-700 mb-1"
          >
            Nº gatos estimado
          </label>
          <input
            id="gatos"
            type="number"
            bind:value={n_gatos_est}
            min="0"
            max="1000"
            required
            class="mt-1 block w-24 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          />
          {#if n_gatos_est !== "" && (isNaN(gatosNum) || gatosNum < 0 || gatosNum > 1000)}
            <p class="text-red-600 text-xs mt-1">0–1000</p>
          {/if}
        </div>

        <!-- Fecha de alta -->
        <div>
          <label
            for="fecha"
            class="block text-sm font-medium text-gray-700 mb-1"
          >
            Fecha de alta
          </label>
          <input
            id="fecha"
            type="date"
            bind:value={fecha_alta}
            required
            class="mt-1 block w-auto border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <!-- Botón guardar -->
        <div class="pt-4">
          <button
            type="submit"
            class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2 rounded-md disabled:opacity-50"
            disabled={!isValid}
          >
            Guardar colonia
          </button>
        </div>
      </form>
    </div>
  </div>
</div>
