// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// https://astro.build/config
export default defineConfig({
	markdown: {
		remarkPlugins: [remarkMath],
		rehypePlugins: [rehypeKatex],
	},
	integrations: [
		starlight({
			title: 'Academic Archive',
			customCss: [
				'./src/styles/tufte.css',
				'katex/dist/katex.min.css'
			],
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/withastro/starlight' }],
			sidebar: [
				{
					label: 'Cloud & Data Center (CDCT)',
					items: [
						{
							label: 'Textbook Notes',
							items: [{ autogenerate: { directory: 'CDCT/Notes' } }]
						},
						{
							label: 'Engineering Practicals',
							items: [{ autogenerate: { directory: 'CDCT/Practicals' } }]
						}
					],
				},
				{
					label: 'Foundation of Blockchain (FOB)',
					items: [
						{ label: 'Textbook Notes', items: [{ autogenerate: { directory: 'FOB/Notes' } }] },
						{ label: 'Engineering Practicals', items: [{ autogenerate: { directory: 'FOB/Practicals' } }] }
					],
				},
				{
					label: 'Hands on Practice using IoT (IOT)',
					items: [
						{ label: 'Textbook Notes', items: [{ autogenerate: { directory: 'IOT/Notes' } }] },
						{ label: 'Engineering Practicals', items: [{ autogenerate: { directory: 'IOT/Practicals' } }] }
					],
				},
				{
					label: 'AI Product Design (AIPD)',
					items: [
						{ label: 'Textbook Notes', items: [{ autogenerate: { directory: 'AIPD/Notes' } }] },
						{ label: 'Engineering Practicals', items: [{ autogenerate: { directory: 'AIPD/Practicals' } }] }
					],
				},
				{
					label: 'AI with Prompt Engineering (AIPE)',
					items: [
						{ label: 'Textbook Notes', items: [{ autogenerate: { directory: 'AIPE/Notes' } }] },
						{ label: 'Engineering Practicals', items: [{ autogenerate: { directory: 'AIPE/Practicals' } }] }
					],
				},
			],
		}),
	],
});
