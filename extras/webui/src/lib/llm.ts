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

	/** Generate a description for a chat */
	public async generateDescription(message: string) {
		return await this.client.chat.completions.create({
			messages: [
				{
					role: 'system',
					content:
						'You are a helpful AI that generates titles for chats. Keep the title short and to the point. Respond only with the title. Do not include the chat itself in the response. You will receive a single message as input.'
				},
				{ role: 'user', content: `Describe the following chat: ${message}` }
			],
			model: 'gpt-3.5-turbo',
			max_tokens: 100
		});
	}
}

const llm = new LLMInterface(PUBLIC_OPEN_AI_ENDPOINT, PUBLIC_OPEN_AI_KEY);
export default llm;
