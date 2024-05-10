import type { Article } from './auto_llama_sdk/models/Article';
import type { Config } from './config';

type FetchType = typeof fetch;

export interface FileUploadOptions {
	summarize?: number;
	skip_appendix?: boolean;
	ocr?: boolean;
}

export default class AutoLLaMaAPI {
	private _fetch = fetch;

	constructor(fetcher: FetchType | null = null) {
		if (fetcher) this._fetch = fetcher;
	}

	static new() {
		return new AutoLLaMaAPI();
	}

	async parseFile(file: Blob, options: FileUploadOptions, config: Config): Promise<Article> {
		const formData = new FormData();
		formData.append('file', file);
		formData.append('data', JSON.stringify(options));

		const res = await this._fetch(`${config.OpenAIEndpoint}/context/parse_file`, {
			method: 'POST',
			body: formData
		});

		if (!res.ok) {
			throw new Error('Failed to parse file');
		}

		return await res.json();
	}
}
