<script>
	import { fly } from 'svelte/transition';
	import { bounceInOut } from 'svelte/easing';

	import '../reset.css';
	import Boubble from './boubble.svelte';

	let form = {
		history: []
	};
	let error = {
		openai_api_key: 'You can find your API key at https://platform.openai.com/account/api-keys'
	};

	let role = `You are a christian priest that adviser, encourages, morivate,
prays and py arecommends bible verse accorging to the users situation.
Then ask a follow up question probing further about the persons
situation`;

	const validate = () => {
		error = {};
		if (!form.message) {
			error.message = 'cannot be empty';
		}
		if (!form.openai_api_key) {
			error.openai_api_key =
				'cannot be empty, You can find your API key at https://platform.openai.com/account/api-keys';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		if (add_role) {
			form.history.push({
				role: 'system',
				content: role
			});
		}
		form.history.push({
			role: 'user',
			content: form.message
		});

		show_settings = false;
		add_role = false;
		form.message = '';
		scroll();

		const resp = await fetch(`${import.meta.env.VITE_API_URL}/chat`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(form)
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				form.history = data.data.history;
				scroll();
			} else {
				show_settings = true;
				error = data.message;
			}
		}
	};
	const scroll = () => {
		const chat_area = document.querySelector('.chat_area');
		chat_area.scrollTop = chat_area.scrollHeight;
		// chat_area.scrollIntoView({ behavior: 'smooth' });
	};
	
	let show_settings = true;
	let add_role = true;
</script>

<section>
	<h2>Live Demo</h2>
	<div class="setting_area">
		{#if show_settings}
			{#if error.openai_api_key}
				<span class="error">{error.openai_api_key}</span>
			{/if}
			<input
				id="openai_api_key"
				type="text"
				bind:value={form.openai_api_key}
				placeholder="OpenAI API key"
			/>
		{/if}
		{#if add_role}
			<br />
			Chatbot Role:
			<textarea
				placeholder="ChatBot Role"
				id="message"
				bind:value={role}
				on:keydown={(e) => {
					if (e.key === 'Enter') {
						e.preventDefault();
						validate();
					}
				}}
			/>
		{/if}
	</div>

	<div class="chat_area">
		<div class="scroller">
			<Boubble role="assistant">how do you feel?</Boubble>
			{#each form.history as h}
				<div transition:fly|local={{ delay: 0, duration: 200, easing: bounceInOut, y: 100 }}>
					<Boubble role={h.role}>
						{h.content}
					</Boubble>
				</div>
			{/each}
		</div>
	</div>

	<div class="message_area">
		{#if error.message}
			<span class="error">{error.message}</span>
		{/if}
		<div class="user_input">
			<textarea
				placeholder="message"
				id="message"
				bind:value={form.message}
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

		/* margin: auto; */
		height: 100vh;
		/* max-width: 600px; */
		padding: var(--var1);
	}

	section,
	.message_area,
	.setting_area {
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

	input,
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
		/* aspect-ratio: 1/1; */
		background-color: rgb(193, 193, 193);
		cursor: pointer;
	}

	.error {
		color: red;
	}
</style>
