<template>
  <v-app-bar
    :elevation="0"
    class="bg-primary justify-center px-1"
    mode="shift"
    height="45"
  >
    <template #prepend>
      <navigation-home-btn />
    </template>

    <navigation-search-btn />
    <navigation-platforms-btn />
    <navigation-collections-btn />
    <v-divider
      opacity="0"
      class="mx-3"
      vertical
    />
    <navigation-upload-btn />
    <navigation-scan-btn />
    
    <template #append>
      <navigation-user-btn />
    </template>
  </v-app-bar>
</template>
