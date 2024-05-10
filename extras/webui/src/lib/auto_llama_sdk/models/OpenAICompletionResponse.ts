/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OpenAICompletionChoice } from './OpenAICompletionChoice';
import type { Usage } from './Usage';
/**
 * OpenAI stream completion response
 */
export type OpenAICompletionResponse = {
    id: string;
    object: OpenAICompletionResponse.object;
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
    choices: Array<OpenAICompletionChoice>;
};
export namespace OpenAICompletionResponse {
    export enum object {
        TEXT_COMPLETION = 'text_completion',
        CHAT_COMPLETION = 'chat.completion',
    }
}

