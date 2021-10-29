<template>
  <div>
    <nav-bar></nav-bar>
    <div style="padding: 1em">
      <slot />
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";

export default {
  components: {
    NavBar,
  },
};
</script>