<script lang="ts">
	import { cn } from '$lib/utils/cn';

	export let className: string = '';
	export let style: 'plain' | 'lit' = 'plain';
	export let type: 'submit' | 'reset' | 'button' = 'button';
</script>

<button {type} class={'p-[3px] relative ' + className}>
	<div
		class={cn('absolute inset-0 rounded-lg', {
			'bg-zinc-200 dark:bg-zinc-800': style === 'plain',
			'g-amber-600 dark:bg-amber-500': style === 'lit'
		})}
	/>
	<div
		class="py-1 bg-zinc-50 dark:bg-zinc-950 rounded-[6px] relative group transition duration-200 hover:bg-transparent"
	>
		<slot />
	</div>
</button>
