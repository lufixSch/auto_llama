import OpenAI from 'openai';
import { PUBLIC_OPEN_AI_ENDPOINT, PUBLIC_OPEN_AI_KEY } from '$env/static/public';
import type { Chat } from './chats';

export class LLMInterface {
	public client: OpenAI;

	constructor(apiEndpoint: string, apiKey: string) {
		this.client = new OpenAI({
			baseURL: apiEndpoint,
			apiKey: apiKey,
			dangerouslyAllowBrowser: true
		});
	}

	public async chat(chat: Chat) {
		const messages = chat.messages.map((m) => {
			return { role: m.role, content: m.content };
		});

		return await this.client.chat.completions.create({
			messages,
			model: 'gpt-3.5-turbo'
		});
	}

	public async chatStream(chat: Chat) {
		const messages = chat.messages.map((m) => {
			return { role: m.role, content: m.content };
		});

		return await this.client.chat.completions.create({
			messages,
			model: 'gpt-3.5-turbo',
			stream: true
		});
	}
}

const llm = new LLMInterface(PUBLIC_OPEN_AI_ENDPOINT, PUBLIC_OPEN_AI_KEY);
export default llm;
