import OpenAI from 'openai';
import { env } from '$env/dynamic/public';
import type { Chat } from './chats';
import { ChatType, type Character } from './characters';

export interface LLMParams {
	max_new_tokens: number;
	frequency_penalty: number;
	presence_penalty: number;
	temperature: number;
	top_p: number;
}

export const defaultLLMParams: LLMParams = {
	max_new_tokens: 512,
	temperature: 0.7,
	top_p: 0.9,
	frequency_penalty: 0.1,
	presence_penalty: 0
};

export type LLmResponse = AsyncGenerator<{ delta: string; text: string }, void, unknown>;

export class LLMInterface {
	public client: OpenAI;

	constructor(apiEndpoint: string, apiKey: string) {
		this.client = new OpenAI({
			baseURL: apiEndpoint,
			apiKey: apiKey,
			dangerouslyAllowBrowser: true
		});
	}

	public async chat(chat: Chat, branch: number) {
		const messages = chat.getBranch(branch).map((m) => {
			return { role: m.message.role, content: m.message.content };
		});

		return await this.client.chat.completions.create({
			messages,
			model: 'gpt-3.5-turbo'
		});
	}

	public async chatStream(chat: Chat, branch: number) {
		const messages = chat.getBranch(branch).map((m) => {
			return { role: m.message.role, content: m.message.content };
		});

		return await this.client.chat.completions.create({
			messages,
			model: 'gpt-3.5-turbo',
			stream: true
		});
	}

	public async *response(chat: Chat, branch: number, character: Character) {
		if (character.chatType === ChatType.instruct) {
			const messages = chat.formatInstruct(branch, character);

			const stream = await this.client.chat.completions.create({
				messages,
				model: 'gpt-3.5-turbo',
				stream: true
			});

			let completeResponse = '';
			for await (const chunk of stream) {
				completeResponse += chunk.choices[0].delta;
				yield { delta: chunk.choices[0].delta.content as string, text: completeResponse };
			}

			stream.controller.abort();
		} else {
			let messages = chat.formatChat(branch, character);
			messages += `${character.names.assistant}:`;

			const stream = await this.client.completions.create({
				prompt: messages,
				model: 'gpt-3.5-turbo',
				stream: true,
				stop: [
					`${character.names.user}:`,
					`${character.names.assistant}:`,
					`${character.names.system}:`
				],
				max_tokens: 512
			});

			let completeResponse = '';
			for await (const chunk of stream) {
				completeResponse += chunk.choices[0].text;
				yield { delta: chunk.choices[0].text, text: completeResponse };
			}

			stream.controller.abort();
		}
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
				{ role: 'user', content: `Write a title for the following chat: ${message}` }
			],
			model: 'gpt-3.5-turbo',
			max_tokens: 50,
			stop: ['\n']
		});
	}
}

const llm = new LLMInterface(env.PUBLIC_OPEN_AI_ENDPOINT, env.PUBLIC_OPEN_AI_KEY);
export default llm;
