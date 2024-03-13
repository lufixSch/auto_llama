import fs from 'fs';
import { DATA_PATH } from '$env/static/private';
import type { Character } from '$lib/characters';

export function getBasePath() {
	return DATA_PATH + '/characters';
}

export function getPath(id: string) {
	return DATA_PATH + '/characters/char-' + id + '.json';
}

export function readCharacter(id: string) {
	const character = JSON.parse(fs.readFileSync(getPath(id), 'utf-8'));
	return character;
}

export function overwriteCharacter(id: string, character: Character) {
	fs.writeFileSync(getPath(id), JSON.stringify(character));
}

export function overwriteIndex(data: { [key: string]: string }) {
	fs.writeFileSync(getBasePath() + '/index.json', JSON.stringify(data));
}

export function getIndex() {
	// Read index and create file if not existing
	try {
		const indexData = JSON.parse(
			fs.readFileSync(getBasePath() + '/index.json', { encoding: 'utf-8' })
		);
		return indexData as { [key: string]: string };
	} catch {
		const indexData = {};
		fs.writeFileSync(getBasePath() + '/index.json', JSON.stringify(indexData), { flag: 'wx' });
		return indexData as { [key: string]: string };
	}
}
