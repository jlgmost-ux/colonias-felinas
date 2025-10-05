import { getTurnos, getUsers } from '$lib/api';

export async function load({ params }) {
    const coloniaId = params.id;

    const [turnos, users] = await Promise.all([
        getTurnos(coloniaId),
        getUsers(coloniaId)
    ]);

    return { coloniaId, turnos, users };
}
