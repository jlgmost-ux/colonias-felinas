const BASE = 'http://localhost:8000';

export async function api<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const res = await fetch(`${BASE}${path}`, opts);
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<T>;
}

/* ---------------------------------------------
   Turnos de Alimentación (Calendario)
--------------------------------------------- */

export interface Turno {
  id: string;
  colonia_id: string;
  user_id: string;
  fecha: string;
  hora?: string | null;
  notas?: string | null;
  created_at?: string;
}

// Listar turnos por colonia
export function getTurnos(coloniaId: string) {
  return api<Turno[]>(`/turnos?colonia_id=${coloniaId}`);
}

// Crear turno nuevo
export function crearTurno(data: {
  colonia_id: string;
  user_id: string;
  fecha: string;
  notas?: string;
}) {
  return api<Turno>('/turnos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
}

// Eliminar turno
export function eliminarTurno(turnoId: string) {
  return api<{ ok: boolean }>(`/turnos/${turnoId}`, {
    method: 'DELETE'
  });
}


/* ---------------------------------------------
   Usuarios (para asignación de turnos)
--------------------------------------------- */

export interface User {
  id: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export function getUsers(coloniaId?: string) {
  const query = coloniaId ? `?colonia_id=${coloniaId}` : '';
  return api<User[]>(`/users${query}`);
}