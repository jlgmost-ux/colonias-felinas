// frontend/src/routes/colonias/[id]/+page.ts
import type { PageLoad } from './$types';
import { api } from '$lib/api';

export const load: PageLoad = async ({ params }) => {
    const { id } = params;

    // 1) Obtenemos la colonia
    const colonia = await api<{
        id: string;
        nombre: string;
        lat: number;
        lon: number;
        n_gatos_est: number;
        fecha_alta: string;
        notas?: string;
    }>(`/colonias/${id}`);

    // 2) Obtenemos los gatos de esa colonia
    const gatos = await api<Array<{
        id: string;
        sexo: string;
        edad_estimada: number | null;
        esterilizado: boolean;
        fecha_registro: string;
        color?: string;
        notas?: string;
    }>>(`/gatos?colonia_id=${id}`);

    return { colonia, gatos };
};
