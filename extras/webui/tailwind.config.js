/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			height: {
				page: 'calc(100% - 2.75rem)'
			}
		}
	},
	plugins: [require('@tailwindcss/forms')]
};
