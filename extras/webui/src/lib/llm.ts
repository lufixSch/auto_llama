import OpenAI from 'openai';
import type { Chat } from './chats';
import { ChatType, type Character } from './characters';
import type { Config } from './config';

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
	// public client: OpenAI;

	// constructor(apiEndpoint: string, apiKey: string) {
	// 	this.client = new OpenAI({
	// 		baseURL: apiEndpoint,
	// 		apiKey: apiKey,
	// 		dangerouslyAllowBrowser: true
	// 	});
	// }

	public getClient(config: Config) {
		return new OpenAI({
			baseURL: config.OpenAIEndpoint,
			apiKey: config.OpenAIKey,
			dangerouslyAllowBrowser: true
		});
	}

	public async chat(chat: Chat, branch: number, params: Partial<LLMParams> = {}, config: Config) {
		const messages = chat.getBranch(branch).map((m) => {
			return { role: m.message.role, content: m.message.content };
		});

		return await this.getClient(config).chat.completions.create({
			messages,
			model: 'gpt-3.5-turbo',
			...params
		});
	}

	public async chatStream(chat: Chat, branch: number, params: Partial<LLMParams>, config: Config) {
		const messages = chat.getBranch(branch).map((m) => {
			return { role: m.message.role, content: m.message.content };
		});

		return await this.getClient(config).chat.completions.create({
			messages,
			model: 'gpt-3.5-turbo',
			stream: true,
			...params
		});
	}

	public async *response(chat: Chat, branch: number, character: Character, config: Config) {
		if (character.chatType === ChatType.instruct) {
			const messages = chat.formatInstruct(branch, character, config);
			console.log(messages);

			const stream = await this.getClient(config).chat.completions.create({
				messages,
				model: 'gpt-3.5-turbo',
				stream: true,
				max_tokens: character.params.max_new_tokens || defaultLLMParams.max_new_tokens,
				...(character.params || defaultLLMParams)
			});

			let completeResponse = '';

			try {
				for await (const chunk of stream) {
					completeResponse += chunk.choices[0].delta;
					yield { delta: chunk.choices[0].delta.content as string, text: completeResponse };
				}
			} finally {
				stream.controller.abort();
			}
		} else {
			let messages = chat.formatChat(branch, character, config);
			messages += `${character.names.assistant}:`;

			console.log(messages);

			const stream = await this.getClient(config).completions.create({
				prompt: messages,
				model: 'gpt-3.5-turbo',
				stream: true,
				stop: [
					`${character.names.user}: `,
					`${character.names.assistant}: `,
					`${character.names.system}: `
				],
				max_tokens: character.params.max_new_tokens || defaultLLMParams.max_new_tokens,
				...(character.params || defaultLLMParams)
			});

			let completeResponse = '';

			try {
				for await (const chunk of stream) {
					completeResponse += chunk.choices[0].text;
					yield { delta: chunk.choices[0].text, text: completeResponse };
				}
			} finally {
				stream.controller.abort();
			}
		}
	}

	/** Generate a description for a chat */
	public async generateDescription(
		message: string,
		config: Config,
		params: Partial<LLMParams> = defaultLLMParams
	) {
		return await this.getClient(config).chat.completions.create({
			messages: [
				{
					role: config.isUserInstruct ? 'user' : 'system',
					content:
						'You are a helpful AI that generates titles for chats. Keep the title short and to the point. Respond only with the title. Do not include the chat itself in the response. You will receive a single message as input.'
				},
				{ role: 'user', content: `Write a title for the following chat: ${message}` }
			],
			model: 'gpt-3.5-turbo',
			max_tokens: 50,
			stop: ['\n'],
			...params
		});
	}
}

const llm = new LLMInterface();
export default llm;
