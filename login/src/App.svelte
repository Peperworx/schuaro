<script>
	import TextBox from "./components/TextBox.svelte";
	import Button from './components/Button.svelte'
	import './App.scss'
	
</script>


<form id="login">
	<h1>Schuaro</h1>
	<h2>login</h2>
	<TextBox type="text" placeholder="username" name="username"/>
	<TextBox type="password" placeholder="password" name="password"/>
	
	<Button type="submit" content="Submit"/>
</form>
