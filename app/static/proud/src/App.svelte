<script lang="ts">
    let email = '';
    let password = '';
    let rememberMe = false;

    async function handleLogin(event: Event) {
        event.preventDefault();
        console.log({ email, password, rememberMe });
        try {
            const response = await fetch('http://localhost:8000/api/auth/login/', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    password,
                    remember_me: rememberMe
                })
            }
        );
        } catch (error) {
            console.error('Erro ao fazer login:', error);
        }
    }
</script>

<header class="header">
    <nav class="nav">
        <a href="./src/Counter.svelte" class="nav-item">Users</a>
        <a href="./src/Counter.svelte" class="nav-item">Members</a>
        <div class="logo">proud.</div>
        <a href="./src/Counter.svelte" class="nav-item">Products</a>
        <a href="./src/Counter.svelte" class="nav-item">Newsletters</a>
    </nav>
</header>
<div class="login-container">
    <!-- Left: Login Form -->
    <div class="login-form">
        <h1>SIGN IN</h1>
        <form on:submit={handleLogin}>
            <input
                type="text"
                placeholder="E-mail"
                bind:value={email}
                required
            />
            <input
                type="password"
                placeholder="Password"
                bind:value={password}
                required
            />
            <div class="options">
                <label>
                <input
                    type="checkbox"
                    bind:checked={rememberMe}
                />
                Remember me
                </label>
                <a href="./src/Counter.svelte" class="recover-password">recover password</a>
            </div>
            <button type="submit">Continue</button>
        </form>
        <div class="footer">
            <p>No account? <a href="./src/lib/SignUP.svelte" class="recover-password">Create one.</a></p>
        </div>
    </div>

    <!-- Right: Background Image -->
    <div class="background-image"></div>
</div>