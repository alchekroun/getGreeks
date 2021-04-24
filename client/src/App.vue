<template>
  <v-app>
    <v-app-bar
      absolute
      elevate-on-scroll
      app
    >
      <v-toolbar-title>GetGreeks</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text to="/">
        Home
      </v-btn>
      <v-btn text to="/about">
        About
      </v-btn>
    </v-app-bar>
    <v-main>
      <router-view/>
    </v-main>
    <v-footer>
      <v-col class="text-center" cols="12">
        {{ new Date().getFullYear() }} - <strong>Alex</strong>
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>

export default {
  name: 'App',
};
</script>

<style>
</style>
