import type { PageLoad } from './$types';
import { api } from '$lib/api';

export const load: PageLoad = async () => {
  const colonias = await api<Array<any>>('/colonias');
  return { colonias };
};
