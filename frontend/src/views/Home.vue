<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>sup</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn to="/register">
          Register
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn to="/login">
          Log In
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn @click="logout">
          Log Out
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn to="/create-color">
          Create Color
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn to="/create-gym">
          Create Gym
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <h2>Gym Map:</h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-form>
          <v-text-field
            id="id_gym-name"
            v-model="gymName"
            label="Gym Name"
          />
          <v-btn
            id="submit_button"
            @click="openGymMap"
          >
            Open
          </v-btn>
        </v-form>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn
          color="error"
          @click="deleteAccountAndLogout"
        >
          Delete Account
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
/** @file index view with menu */

import {mapActions, mapMutations, mapState} from 'vuex';

export default {
  name: 'Index',
  data() {
    return {
      gymName: '',
    };
  },
  computed: {
    ...mapState(['user']),
  },
  methods: {
    ...mapMutations(['logout']),
    ...mapActions(['deleteAccountAndLogout']),
    /**
     * Redirects to gym map with name entered in text field
     */
    openGymMap() {
      this.$router.push(`/gym-map/${this.gymName}`);
    },
  },
};
</script>

<style scoped>

</style>
