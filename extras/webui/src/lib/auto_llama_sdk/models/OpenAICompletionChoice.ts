/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * OpenAI completion choice parameters (for streaming and no streaming)
 */
export type OpenAICompletionChoice = {
    /**
     * **UNSUPORTED** (always set to 'length')
     */
    finish_reason?: ('stop' | 'length' | 'content_filter' | 'tool_calls' | null);
    index: number;
    /**
     * **UNSUPORTED**
     */
    logprobs?: (Record<string, any> | null);
    text: string;
};

