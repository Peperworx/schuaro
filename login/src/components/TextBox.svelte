<script>
    import './TextBox.scss'
    export let placeholder;
    export let name;
    export let id;
    export let type;
</script>

<div class="floating-label">
    
    <input name="{name}" type="{type}" id="{id}" placeholder="{placeholder}">
    <div class="fl-div">
        <label for="{id}">{placeholder}</label>
    </div>
    
</div>