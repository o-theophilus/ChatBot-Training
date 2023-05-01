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

<section>
	<div class="chat_area">
		<div class="scroller">
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
		<div class="user_input">
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
	section {
		--var1: 20px;
		--var2: 8px;

		height: 100vh;
		padding: var(--var1);
	}

	section,
	.message_area {
		display: flex;
		flex-direction: column;
		gap: var(--var2);
	}

	.chat_area {
		display: flex;
		flex-direction: column-reverse;

		border-radius: var(--var2);
		height: 100%;
		padding: var(--var1) calc(var(--var1) * 2);

		overflow-y: auto;
		background-color: rgb(207, 207, 207);
	}

	.user_input {
		display: flex;
		gap: var(--var2);
	}

	textarea,
	button {
		border-radius: var(--var2);
		border: 2px solid gray;
		padding: var(--var1);
	}

	textarea {
		display: block;
		resize: none;
		width: 100%;
		height: 120px;
	}

	button:hover {
		background-color: rgb(193, 193, 193);
		cursor: pointer;
	}
</style>
