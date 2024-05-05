import fs from 'fs';
import { env } from '$env/dynamic/private';
import type { Config } from '../config';

export function getPath() {
	return env.DATA_PATH + '/config.json';
}

export function writeDefault() {
	const config: Config = {
		isUserInstruct: false,
		OpenAIEndpoint: env.OPEN_AI_ENDPOINT || 'http://localhost:8000/v1',
		OpenAIKey: env.OPEN_AI_KEY || 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	};

	fs.writeFileSync(getPath(), JSON.stringify(config), { flag: 'wx' });
	return config;
}

export function overwriteWithEnv() {
	const config = readConfig();
	config.OpenAIEndpoint = env.OPEN_AI_ENDPOINT || 'http://localhost:8000/v1';
	config.OpenAIKey = env.OPEN_AI_KEY || 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
	fs.writeFileSync(getPath(), JSON.stringify(config));
	return config;
}

export function readConfig(): Config {
	try {
		const config = JSON.parse(fs.readFileSync(getPath(), 'utf-8'));
		return config;
	} catch {
		return writeDefault();
	}
}

export function writeConfig(config: Config) {
	fs.writeFileSync(getPath(), JSON.stringify(config));
}
