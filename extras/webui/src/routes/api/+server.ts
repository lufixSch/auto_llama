import { json } from '@sveltejs/kit';
import * as pkg from '../../../package.json';

/** Get current version of the API */
export function GET() {
	return json({ message: 'Welcome to the AutoLLaMa WebUI API', version: pkg.version });
}
