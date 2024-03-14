import fs from 'fs';
import { json } from '@sveltejs/kit';
import * as pkg from '../../../package.json';
import { building } from '$app/environment';
import { DATA_PATH } from '$env/static/private';

if (!building) {
	if (!fs.existsSync(DATA_PATH)) {
		fs.mkdirSync(DATA_PATH);
	}
}

/** Get current version of the API */
export function GET() {
	return json({ message: 'Welcome to the AutoLLaMa WebUI API', version: pkg.version });
}
