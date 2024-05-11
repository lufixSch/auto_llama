import { generateId } from '$lib/utils/id';
import type { Article } from './auto_llama_sdk';
import type { Character } from './characters';
import type { Config } from './config';

export enum Roles {
	system = 'system',
	assistant = 'assistant',
	user = 'user'
}

export type ChatIndex = { [key: string]: string };

export interface Message {
	role: Roles;
	content: string;
	branches: number[];
	branchStart: number[];
}

export class Chat {
	messages: { [key: string]: Message } = {};
	branches: { source: number | null; messages: string[] }[] = [{ source: null, messages: [] }];
	files: { [key: string]: Article } = {};
	private _file_match = /!\[(.*?)\]\{.*?\}/g;

	constructor(public character: string) {}

	getBranch(branch: number): { id: string; message: Message }[] {
		return this.branches[branch].messages.map((id) => ({ id, message: this.messages[id] }));
	}

	createBranch(sourceBranch: number, messageId: string) {
		const msgIndex = this.branches[sourceBranch].messages.findIndex((id) => id === messageId);
		const branchId = this.branches.length;

		this.messages[messageId].branchStart.push(branchId);

		this.branches.push({
			source: sourceBranch,
			messages: this.branches[sourceBranch].messages.slice(0, msgIndex + 1)
		});
		this.branches[branchId].messages.forEach((msgId) =>
			this.messages[msgId].branches.push(branchId)
		);

		return branchId;
	}

	getBranchPath(branch: number) {
		const path: number[] = [branch];
		let current: number | null = branch;
		while (current !== null) {
			path.push(current);
			current = this.branches[current].source;
		}

		return path;
	}

	getBranchSet(branch: number) {
		const set = new Set<number>();
		let current: number | null = branch;
		while (current !== null) {
			set.add(current);
			current = this.branches[current].source;
		}

		return set;
	}

	newMessage(role: Roles, content: string, branch: number) {
		const id = generateId(8);
		const message: Message = { role, content, branches: [branch], branchStart: [] };
		this.messages[id] = message;
		this.branches[branch].messages.push(id);
		return id;
	}

	deleteMessage(id: string) {
		const msg = this.messages[id];
		msg.branches.forEach(
			(branch) =>
				(this.branches[branch].messages = this.branches[branch].messages.filter((i) => i !== id))
		);
		delete this.messages[id];
		return msg;
	}

	/** Format chat messages for generating a response in 'instruct' mode */
	formatInstruct(branch: number, char: Character, conf: Config) {
		const msg = this.getBranch(branch).reduce<{ role: Roles; content: string; name: string }[]>(
			(messages, { message }) => {
				// Insert empty user message between two assistant messages.
				// Some backends may otherwise only consider the last message
				if (
					messages.length > 0 &&
					messages[messages.length - 1].role === Roles.assistant &&
					message.role === Roles.assistant
				) {
					messages.push({ role: Roles.user, content: '', name: char.names.user });
				}

				const content = this.insertFileContent(message.content);

				messages.push({
					role: message.role,
					content: content,
					name: char.names[message.role]
				});

				return messages;
			},
			[]
		);

		if (char.greeting) {
			msg.unshift({ role: Roles.assistant, content: char.greeting, name: char.names.assistant });
		}

		if (char.instructPrompt) {
			msg.unshift({
				role: conf.isUserInstruct ? Roles.user : Roles.system,
				content: char.instructPrompt,
				name: char.names.system
			});
		}

		// Add empty user message at the end, if the last message is from the assistant
		if (msg[msg.length - 1].role == Roles.assistant) {
			msg.push({ role: Roles.user, content: '', name: char.names.user });
		}

		console.log(msg);
		return msg;
	}

	/** Format chat messages for generating a response in 'chat' mode */
	formatChat(branch: number, char: Character, conf: Config) {
		const msg = this.formatInstruct(branch, char, conf);

		return msg.reduce(
			(chat, message) => `${chat}${char.names[message.role]}: ${message.content}\n`,
			''
		);
	}

	/** Add new files to the chat */
	addFile(...files: Article[]) {
		files.forEach((file, i) => {
			this.files[`${i}/${file.source}`] = file;
		});
	}

	/** Remove file from the chat */
	removeFile(idx: number) {
		Object.keys(this.files).forEach((key) => {
			if (key.startsWith(`${idx}/`)) {
				delete this.files[key];
				return;
			}
		});
	}

	/* Find file references in chat and replace content */
	insertFileContent(message: string) {
		const matches = message.match(this._file_match);

		let res = message;
		matches?.forEach((match) => {
			const id = match.slice(2, match.indexOf(']'));
			console.log(id, this.files);
			res = res.replace(match, `![${id}]{${this.files[id].text}}`);
		});

		return res;
	}

	/* Return file reference for a given file */
	static emptyFileReference(id: string) {
		return `![${id}]{}`;
	}

	static fromJson(json: Chat): Chat {
		const chat = new Chat(json.character);
		chat.messages = json['messages'];
		chat.branches = json['branches'];
		chat.files = json['files'];
		return chat;
	}
}
