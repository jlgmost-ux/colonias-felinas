<script lang="ts">
  import type { PageLoad } from "./$types";
  import Map from "$lib/Map.svelte";

  export let data: {
    colonias: Array<{
      id: string;
      nombre: string;
      lat: number;
      lon: number;
      n_gatos_est: number;
    }>;
  };

  // Preparamos el array de marcadores
  const markers = data.colonias.map((c) => ({
    lat: c.lat,
    lon: c.lon,
    popup: c.nombre,
  }));
</script>

<div class="max-w-4xl mx-auto p-6 space-y-6">
  <!-- Título y botón -->
  <div class="flex justify-between items-center">
    <h1 class="text-4xl font-bold text-red-600 mb-0">Colonias registradas</h1>
    <a
      href="/colonias/nueva"
      class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
    >
      + Nueva colonia
    </a>
  </div>

  <!-- 1) Mapa -->
  {#if markers.length > 0}
    <Map {markers} />
  {/if}

  <!-- 2) Tabla estilizada -->
  <div class="overflow-x-auto">
    <table
      class="min-w-full divide-y divide-gray-200 bg-white shadow rounded-lg overflow-hidden"
    >
      <thead class="bg-gray-50">
        <tr>
          <th
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >Nombre</th
          >
          <th
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >Lat</th
          >
          <th
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >Lon</th
          >
          <th
            class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
            >Gatos</th
          >
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        {#each data.colonias as c}
          <tr class="hover:bg-gray-100">
            <td class="px-6 py-4 whitespace-nowrap">
              <a
                href={`/colonias/${c.id}`}
                class="text-indigo-600 hover:underline"
              >
                {c.nombre}
              </a>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">{c.lat}</td>
            <td class="px-6 py-4 whitespace-nowrap">{c.lon}</td>
            <td class="px-6 py-4 whitespace-nowrap text-center"
              >{c.n_gatos_est}</td
            >
          </tr>
        {/each}
        {#if data.colonias.length === 0}
          <tr>
            <td colspan="4" class="px-6 py-4 text-center text-gray-500 italic">
              No hay colonias registradas.
            </td>
          </tr>
        {/if}
      </tbody>
    </table>
  </div>
</div>
