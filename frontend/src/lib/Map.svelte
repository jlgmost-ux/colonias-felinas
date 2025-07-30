<script context="module" lang="ts">
    export const ssr = false;
</script>

<script lang="ts">
    import { onMount } from "svelte";
    let mapEl: HTMLDivElement;
    export let markers: { lat: number; lon: number; popup?: string }[] = [];

    onMount(async () => {
        const L = (await import("leaflet")).default;
        const map = L.map(mapEl);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: "&copy; OpenStreetMap contributors",
        }).addTo(map);

        const group = L.featureGroup();
        markers.forEach((m) => {
            const marker = L.marker([m.lat, m.lon]).bindPopup(m.popup ?? "");
            marker.addTo(map);
            group.addLayer(marker);
        });

        if (markers.length) {
            map.fitBounds(group.getBounds().pad(0.2));
        } else {
            map.setView([0, 0], 2);
        }
    });
</script>

<div bind:this={mapEl} class="w-full h-64 rounded-lg shadow-md"></div>
