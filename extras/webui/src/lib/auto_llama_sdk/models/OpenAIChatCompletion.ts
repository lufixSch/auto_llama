/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OpenAIMessage } from './OpenAIMessage';
import type { OpenAIResponseFormat } from './OpenAIResponseFormat';
import type { OpenAITool } from './OpenAITool';
/**
 * OpenAI chat completion parameters
 */
export type OpenAIChatCompletion = {
    /**
     * **UNSUPORTED**
     */
    model?: string;
    /**
     * **UNSUPORTED**
     */
    frequency_penalty?: (number | null);
    /**
     * **UNSUPORTED**
     */
    logit_bias?: (Record<string, number> | null);
    /**
     * **UNSUPORTED**
     */
    logprobs?: (boolean | null);
    /**
     * **UNSUPORTED**
     */
    top_logprobs?: (number | null);
    max_tokens?: (number | null);
    /**
     * **UNSUPORTED**
     */
    'n'?: number;
    /**
     * **UNSUPORTED**
     */
    presence_penalty?: number;
    /**
     * **UNSUPORTED**
     */
    response_format?: (OpenAIResponseFormat | null);
    /**
     * **UNSUPORTED**
     */
    seed?: (number | null);
    stop?: (string | Array<string>);
    stream?: boolean;
    /**
     * **UNSUPORTED**
     */
    temperature?: number;
    /**
     * **UNSUPORTED**
     */
    top_p?: number;
    /**
     * **UNSUPORTED**
     */
    user?: string;
    messages: Array<OpenAIMessage>;
    /**
     * **UNSUPORTED**
     */
    tools?: Array<OpenAITool>;
    /**
     * **UNSUPORTED**
     */
    tool_choice?: ('none' | 'auto' | Record<string, Record<string, string>>);
};

