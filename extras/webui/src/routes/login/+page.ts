import auth from '$lib/auth';

export const ssr = false;
export const prerender = false;

export function load() {
	auth.logout();
}
