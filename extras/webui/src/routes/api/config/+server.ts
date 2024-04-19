import fs from 'fs';
import { json } from '@sveltejs/kit';
import { building } from '$app/environment';
import {
	getPath,
	overwriteWithEnv,
	readConfig,
	writeConfig,
	writeDefault
} from '$lib/server/config';
import type { Config } from '$lib/config';

if (!building) {
	if (!fs.existsSync(getPath())) {
		writeDefault();
	} else {
		overwriteWithEnv();
	}
}

/** Read the configuration */
export function GET() {
	return json(readConfig());
}

/** Update the configuration */
export async function PUT({ request }) {
	const newConfig: Config = await request.json();
	writeConfig(newConfig);
	return json({ message: 'Configuration updated successfully' });
}
