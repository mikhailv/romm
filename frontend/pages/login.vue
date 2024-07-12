<script setup lang="ts">
definePageMeta({ layout: "secondary" });
import identityApi from "@/services/api/identity";
import { ref } from "vue";

// Props
const emitter = useNuxtApp().$emitter;
const router = useRouter();
const username = ref("");
const password = ref("");
const visiblePassword = ref(false);
const logging = ref(false);

async function login() {
  logging.value = true;
  await identityApi
    .login(username.value, password.value)
    .then(() => {
      const next = (router.currentRoute.value.query?.next || "/").toString();
      router.push(next);
    })
    .catch(({ response, message }) => {
      const errorMessage =
        response.data?.detail ||
        response.data ||
        message ||
        response.statusText;

      emitter?.emit("snackbarShow", {
        msg: `Unable to login: ${errorMessage}`,
        icon: "mdi-close-circle",
        color: "red",
      });
      console.error(
        `[${response.status} ${response.statusText}] ${errorMessage}`
      );
    })
    .finally(() => {
      logging.value = false;
    });
}
</script>

<template>
  <v-container class="main-secondary-container fill-height justify-center">
    <v-card class="translucent-dark py-8 px-5" width="500">
      <v-row no-gutters>
        <v-col>
          <v-img :src="`/images/isotipo.svg`" class="mx-auto" width="150" />

          <v-row class="text-white justify-center mt-2" no-gutters>
            <v-col cols="10" md="8">
              <v-form @submit.prevent>
                <v-text-field
                  v-model="username"
                  required
                  prepend-inner-icon="mdi-account"
                  type="text"
                  label="Username"
                  variant="underlined"
                  @keyup.enter="login()"
                  autocomplete="on"
                />
                <v-text-field
                  v-model="password"
                  required
                  prepend-inner-icon="mdi-lock"
                  :type="visiblePassword ? 'text' : 'password'"
                  label="Password"
                  variant="underlined"
                  :append-inner-icon="
                    visiblePassword ? 'mdi-eye-off' : 'mdi-eye'
                  "
                  @keyup.enter="login()"
                  @click:append-inner="visiblePassword = !visiblePassword"
                  autocomplete="on"
                />
                <v-btn
                  type="submit"
                  :disabled="logging || !username || !password"
                  :variant="!username || !password ? 'text' : 'flat'"
                  class="bg-terciary"
                  block
                  :loading="logging"
                  @click="login()"
                >
                  <span>Login</span>
                  <template #append>
                    <v-icon class="text-romm-accent-1"
                      >mdi-chevron-right-circle-outline</v-icon
                    >
                  </template>
                  <template #loader>
                    <v-progress-circular
                      color="romm-accent-1"
                      :width="2"
                      :size="20"
                      indeterminate
                    />
                  </template>
                </v-btn>
              </v-form>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>
