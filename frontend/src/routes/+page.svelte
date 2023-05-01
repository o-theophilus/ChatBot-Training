<script>
	import { fly } from 'svelte/transition';
	import { bounceInOut } from 'svelte/easing';

	import './reset.css';
	import Boubble from './boubble.svelte';

	let system_role = `As a Christian priest chatbot, your role is to provide compassionate guidance, encouragement, motivation, and prayer support to users seeking spiritual guidance. You will also recommend relevant Bible verses based on the user's specific situation.
Your goal is to create a safe and supportive space for users to explore their spiritual needs and challenges. As such, you will actively listen to users' concerns and ask follow-up questions to gain a deeper understanding of their situation. Through your interactions, you will offer thoughtful insights, personalized advice, and empathetic support to help users navigate their spiritual journeys with grace and confidence.
With your knowledge of Christian teachings and your dedication to helping others, you will serve as a trusted ally and source of inspiration for those seeking a deeper connection with their faith.`;
	let key_error = 'You can find your API key at https://platform.openai.com/account/api-keys';
	let show_settings = true;
	let add_role = true;

	let form = {
		history: []
	};
	let error = {
		openai_api_key: key_error
	};

	const validate = () => {
		error = {};
		if (!form.openai_api_key) {
			error.openai_api_key = `cannot be empty, ${key_error}`;
		}
		if (!system_role) {
			error.system_role = 'cannot be empty';
		}
		if (!form.message) {
			error.message = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		if (add_role) {
			form.history.push({
				role: 'system',
				content: system_role
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
	};
</script>

<section>
	<div class="setting_area">
		{#if show_settings}
			<label for="role"> OpenAI API key: </label>
			{#if error.openai_api_key}
				<span class="error">{error.openai_api_key}</span>
			{/if}
			<input
				id="openai_api_key"
				type="text"
				bind:value={form.openai_api_key}
				placeholder="OpenAI API key"
				on:input={() => {
					if (form.openai_api_key) {
						error.openai_api_key = '';
					} else {
						error.openai_api_key = key_error;
					}
				}}
			/>
		{/if}
		{#if add_role}
			<br />
			<label for="role"> ChatBot Role: </label>
			{#if error.system_role}
				<span class="error">{error.system_role}</span>
			{/if}
			<textarea
				placeholder="ChatBot Role"
				id="role"
				bind:value={system_role}
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
		--var3: 80px;

		height: 100vh;
		padding: var(--var1);

		background-color: black;
		/* background-color: rgb(50, 50, 50); */
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

		height: 100%;
		padding: var(--var1) 0;

		overflow-y: auto;
	}

	.user_input {
		display: flex;
		gap: var(--var2);
	}

	label {
		color: greenyellow;
	}
	input,
	textarea {
		border: 2px solid white;
		padding: var(--var2);
		color: white;
		background-color: transparent;
	}

	textarea {
		display: block;
		resize: none;
		width: 100%;
		height: 120px;
	}

	button {
		cursor: pointer;
		width: var(--var3);
		flex-shrink: 0;
		background-color: white;
		border: none;
	}
	button:hover {
		background-color: rgb(195, 195, 195);
	}

	.error {
		color: red;
	}
</style>
