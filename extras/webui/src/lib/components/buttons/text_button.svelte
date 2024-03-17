<script lang="ts">
	import { cn } from '$lib/utils/cn';
	import { createEventDispatcher } from 'svelte';

	export let className: string = '';
	export let style: 'plain' | 'lit' = 'plain';
	export let type: 'submit' | 'reset' | 'button' = 'button';
	export let disabled: boolean = false;

	let click = createEventDispatcher();
</script>

<button
	{type}
	class={'p-[3px] relative ' + className}
	on:click={(e) => click('click', e)}
	{disabled}
>
	<div
		class={cn('absolute inset-0 rounded-lg', {
			'bg-zinc-200 dark:bg-zinc-800': style === 'plain' || disabled,
			'bg-amber-600 dark:bg-amber-500': style === 'lit' && !disabled
		})}
	/>
	<div
		class={cn(
			'py-1 px-4 bg-zinc-50 dark:bg-zinc-950 rounded-[6px] relative group transition duration-200',
			{
				'hover:bg-transparent': !disabled
			}
		)}
	>
		<slot />
	</div>
</button>
