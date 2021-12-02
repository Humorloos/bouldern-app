<template>
  <div class="container">
<!--    <header>-->
<!--      <slot name="header"></slot>-->
<!--    </header>-->
    <main>
      <slot></slot>
    </main>
<!--    <footer>-->
<!--      <slot name="footer"></slot>-->
<!--    </footer>-->
  </div>
</template>

<script>
export default {
  name: 'page-layout',
  props: {msg: String},
  computed: {
    count() {
      return this.$store.state.counter.count
    }
  },
  methods: {
    increment() {
      this.$store.commit('increment')
    },
    decrement() {
      this.$store.commit('decrement')
    }
  },
}
</script>

<style scoped>
.hello {
  text-align: center;
}

.hello span {
  display: inline-block;
  min-width: 4em;
  margin: 1em;
}
</style>