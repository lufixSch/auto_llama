import { env } from '$env/dynamic/private';

export async function handle({ event, resolve }) {
	if (!event.url.pathname.startsWith('/api')) {
		return await resolve(event);
	}

	// Check for authorization
	const authHeader = event.request.headers.get('Authorization');

	if (!authHeader || !authHeader.startsWith('Bearer ')) {
		return new Response('Unauthorized', { status: 401 });
	}
	const token = authHeader.substring('Bearer '.length);
	if (token !== env.SECRET) {
		return new Response('Unauthorized', { status: 401 });
	}

	return await resolve(event);
}
