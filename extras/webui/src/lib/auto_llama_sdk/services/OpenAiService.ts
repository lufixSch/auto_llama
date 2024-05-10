/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OpenAIChatCompletion } from '../models/OpenAIChatCompletion';
import type { OpenAIChatCompletionResponse } from '../models/OpenAIChatCompletionResponse';
import type { OpenAICompletion } from '../models/OpenAICompletion';
import type { OpenAICompletionResponse } from '../models/OpenAICompletionResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class OpenAiService {
    /**
     * Openai Completion
     * @param requestBody
     * @returns OpenAICompletionResponse Successful Response
     * @throws ApiError
     */
    public static openaiCompletionV1CompletionsPost(
        requestBody: OpenAICompletion,
    ): CancelablePromise<OpenAICompletionResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/v1/completions',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Openai Chat Completion
     * @param requestBody
     * @returns OpenAIChatCompletionResponse Successful Response
     * @throws ApiError
     */
    public static openaiChatCompletionV1ChatCompletionsPost(
        requestBody: OpenAIChatCompletion,
    ): CancelablePromise<OpenAIChatCompletionResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/v1/chat/completions',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
