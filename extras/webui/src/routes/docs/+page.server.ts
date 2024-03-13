import fs from 'fs';
import markdownit from 'markdown-it';
import markdownitLatex from 'markdown-it-katex';

const md = markdownit();
md.use(markdownitLatex);

export const prerender = true;

export function load() {
	const content = fs.readFileSync('README.md', 'utf-8');
	console.log('Render');

	return {
		content: md.render(content)
	};
}
