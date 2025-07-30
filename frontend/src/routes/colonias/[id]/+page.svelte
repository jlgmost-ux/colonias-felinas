<script lang="ts">
    export let data: {
        colonia: {
            id: string;
            nombre: string;
            lat: number;
            lon: number;
            n_gatos_est: number;
            fecha_alta: string;
            notas?: string;
        };
        gatos: Array<{
            id: string;
            sexo: string;
            edad_estimada: number | null;
            esterilizado: boolean;
            fecha_registro: string;
            color?: string;
            notas?: string;
        }>;
    };
</script>

<div class="max-w-4xl mx-auto p-6">
    <!-- Header -->
    <div class="bg-indigo-600 p-4 rounded-t-lg">
        <h1 class="text-2xl font-bold text-white">
            {data.colonia.nombre}
        </h1>
    </div>

    <!-- Detalles de la colonia -->
    <div class="bg-white shadow-md rounded-b-lg p-6 mb-6">
        <ul class="space-y-2 text-gray-700">
            <li><strong>ID:</strong> {data.colonia.id}</li>
            <li><strong>Latitud:</strong> {data.colonia.lat}</li>
            <li><strong>Longitud:</strong> {data.colonia.lon}</li>
            <li>
                <strong>Estimación:</strong>
                {data.colonia.n_gatos_est} gatos
            </li>
            <li><strong>Fecha alta:</strong> {data.colonia.fecha_alta}</li>
            {#if data.colonia.notas}
                <li><strong>Notas:</strong> {data.colonia.notas}</li>
            {/if}
        </ul>
    </div>

    <!-- Tabla de gatos -->
    <div class="overflow-x-auto mb-4">
        <table
            class="min-w-full divide-y divide-gray-200 bg-white shadow rounded-lg overflow-hidden"
        >
            <thead class="bg-gray-50">
                <tr>
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >Sexo</th
                    >
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >Edad (meses)</th
                    >
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >Esterilizado</th
                    >
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >Fecha registro</th
                    >
                    <th
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >Color</th
                    >
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                {#each data.gatos as g}
                    <tr class="hover:bg-gray-100">
                        <td class="px-6 py-4 whitespace-nowrap">{g.sexo}</td>
                        <td class="px-6 py-4 whitespace-nowrap"
                            >{g.edad_estimada ?? "—"}</td
                        >
                        <td class="px-6 py-4 whitespace-nowrap"
                            >{g.esterilizado ? "Sí" : "No"}</td
                        >
                        <td class="px-6 py-4 whitespace-nowrap"
                            >{g.fecha_registro}</td
                        >
                        <td class="px-6 py-4 whitespace-nowrap"
                            >{g.color ?? "—"}</td
                        >
                    </tr>
                {/each}
                {#if data.gatos.length === 0}
                    <tr>
                        <td
                            colspan="5"
                            class="px-6 py-4 text-center text-gray-500 italic"
                        >
                            No hay gatos registrados.
                        </td>
                    </tr>
                {/if}
            </tbody>
        </table>
    </div>

    <!-- Botón añadir gato -->
    <a
        href={`/colonias/${data.colonia.id}/gatos/nueva`}
        class="inline-block bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
    >
        + Añadir gato
    </a>
</div>
