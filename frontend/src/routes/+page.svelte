<script>
	import { fly } from 'svelte/transition';
	import { bounceInOut } from 'svelte/easing';

	import './style.css';
	import Boubble from './boubble.svelte';

	let message = '';
	let error = '';
	let history = [];

	const validate = () => {
		error = '';
		if (!message) {
			error = 'cannot be empty';
		}

		!error && submit();
	};

	const submit = async () => {
		history.push({
			role: 'user',
			content: message
		});
		history = history;
		scroll();
		let temp = message;
		message = '';

		const resp = await fetch(`${import.meta.env.VITE_API_URL}/chat`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ message: temp })
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				history.push({
					role: 'bot',
					content: data.response
				});
				history = history;
				scroll();
			} else {
				error = data.message;
			}
		}
	};
	const scroll = () => {
		const chat_area = document.querySelector('.chat_area');
		chat_area.scrollTop = chat_area.scrollHeight;
		// chat_area.scrollIntoView({ behavior: 'smooth' });
	};
</script>

<section class="base">
	<div class="chat_area">
		<div>
			{#each history as h}
				<div transition:fly|local={{ delay: 0, duration: 200, easing: bounceInOut, y: 100 }}>
					<Boubble role={h.role}>
						{h.content}
					</Boubble>
				</div>
			{/each}
		</div>
	</div>

	<div class="message_area">
		{#if error}
			<span class="error">{error}</span>
		{/if}
		<div class="input_area">
			<textarea
				placeholder="message"
				id="message"
				bind:value={message}
				on:keydown={(e) => {
					if (e.key === 'Enter') {
						e.preventDefault();
						validate();
					}
				}}
			/>
			<button
				on:click={() => {
					validate();
				}}>Send</button
			>
		</div>
	</div>
</section>

<style>
	.chat_area {
		display: flex;
		flex-direction: column-reverse;
		/* flex-direction: column; */

		border-radius: var(--var2);
		height: 100%;
		padding: var(--var1) calc(var(--var1) * 2);

		overflow-y: auto;
		background-color: rgb(207, 207, 207);
	}

	.message_area {
		display: flex;
		flex-direction: column;
		gap: var(--var2);
	}

	.input_area {
		display: flex;
		gap: var(--var2);
	}

	textarea {
		width: 100%;
	}
</style>
