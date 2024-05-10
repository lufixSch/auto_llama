/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OpenAIChatChoice } from './OpenAIChatChoice';
import type { OpenAIChatStreamChoice } from './OpenAIChatStreamChoice';
import type { Usage } from './Usage';
/**
 * OpenAI chat completion response
 */
export type OpenAIChatCompletionResponse = {
    id: string;
    object: OpenAIChatCompletionResponse.object;
    created: number;
    /**
     * **UNSUPORTED**
     */
    model?: string;
    /**
     * **UNSUPORTED**
     */
    system_fingerprint?: string;
    /**
     * **UNSUPORTED**
     */
    usage?: Usage;
    choices: Array<(OpenAIChatChoice | OpenAIChatStreamChoice)>;
};
export namespace OpenAIChatCompletionResponse {
    export enum object {
        TEXT_COMPLETION = 'text_completion',
        CHAT_COMPLETION = 'chat.completion',
    }
}

