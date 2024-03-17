import fs from 'fs';
import { json } from '@sveltejs/kit';
import * as pkg from '../../../package.json';
import { building } from '$app/environment';
import { env } from '$env/dynamic/private';

if (!building) {
	if (!fs.existsSync(env.DATA_PATH)) {
		fs.mkdirSync(env.DATA_PATH, { recursive: true });
	}
}

/** Get current version of the API */
export function GET() {
	return json({ message: 'Welcome to the AutoLLaMa WebUI API', version: pkg.version });
}
