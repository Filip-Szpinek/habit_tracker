<script lang="ts">
    let {date, amount, completed = false} = $props();

</script>

<div class="w-full h-full bg-gray-900 rounded-sm"
     class:bg-green-600={completed}
     title="{date} : {amount}"
>

</div>