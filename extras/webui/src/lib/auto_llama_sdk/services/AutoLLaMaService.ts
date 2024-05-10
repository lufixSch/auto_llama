/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AgentResponses } from '../models/AgentResponses';
import type { AgentsInfo } from '../models/AgentsInfo';
import type { Article } from '../models/Article';
import type { Body_parse_file_context_parse_file_post } from '../models/Body_parse_file_context_parse_file_post';
import type { ListResponse } from '../models/ListResponse';
import type { Version } from '../models/Version';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AutoLLaMaService {
    /**
     * List Memory
     * @returns ListResponse Successful Response
     * @throws ApiError
     */
    public static listMemoryMemoryGet(): CancelablePromise<ListResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/memory/',
        });
    }
    /**
     * Set Memory
     * @param memoryName
     * @returns any Successful Response
     * @throws ApiError
     */
    public static setMemoryMemoryPost(
        memoryName: (string | null),
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/memory/',
            query: {
                'memory_name': memoryName,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Search Memory
     * @param query
     * @param memoryName
     * @param maxTokens
     * @param maxItems
     * @returns any Successful Response
     * @throws ApiError
     */
    public static searchMemoryMemoryFindPost(
        query: string,
        memoryName?: (string | null),
        maxTokens: number = 500,
        maxItems: number = 10,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/memory/find',
            query: {
                'query': query,
                'memory_name': memoryName,
                'max_tokens': maxTokens,
                'max_items': maxItems,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * List Agents
     * @returns AgentsInfo Successful Response
     * @throws ApiError
     */
    public static listAgentsAgentGet(): CancelablePromise<AgentsInfo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/agent/',
        });
    }
    /**
     * Run Agent
     * @param agentName
     * @param requestBody
     * @returns AgentResponses Successful Response
     * @throws ApiError
     */
    public static runAgentAgentAgentNamePost(
        agentName: string,
        requestBody: Record<string, any>,
    ): CancelablePromise<AgentResponses> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/agent/{agent_name}',
            path: {
                'agent_name': agentName,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Parse File
     * @param formData
     * @returns Article Successful Response
     * @throws ApiError
     */
    public static parseFileContextParseFilePost(
        formData: Body_parse_file_context_parse_file_post,
    ): CancelablePromise<Article> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/context/parse_file',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Root
     * Base route with status message
     * @returns Version Successful Response
     * @throws ApiError
     */
    public static rootGet(): CancelablePromise<Version> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/',
        });
    }
}
