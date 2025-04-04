<script setup lang="ts">
import DemoTable from './components/TableRegistroANS.vue'
</script>

<template>
  <div class="app">
    <header>
      <div class="logo-container">
        <img alt="Intuitive Care logo" class="logo" src="./assets/logo.svg" width="500" />
      </div>
    </header>

    <main>
      <DemoTable />
    </main>

    <footer>
      <p>© 2025 Intuitive Care. Teste Ellen Ribeiro Borges.</p>
    </footer>
  </div>
</template>

<style>
/* Global styles */
:root {
  --primary-color: #0091bd;
  --secondary-color: #e6f7fb;
  --text-color: #2d3748;
  --light-text: #718096;
  --border-color: #edf2f7;
  --background-color: #f9fbfd;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

header {
  background-color: white;
  width: 100%;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.logo-container {
  display: flex;
  align-items: center;
  margin: 0 auto;
  width: 100%;
}

.logo {
  width: 200px;
  height: auto;
}

.company-name {
  margin-left: 15px;
  font-size: 24px;
  font-weight: 600;
  color: var(--primary-color);
}

main {
  flex: 1;
  padding: 20px;
}

footer {
  background-color: white;
  padding: 20px;
  text-align: center;
  font-size: 14px;
  color: var(--light-text);
  border-top: 1px solid var(--border-color);
}

@media (max-width: 768px) {
  .logo-container {
    flex-direction: column;
    text-align: center;
  }
  
  .company-name {
    margin-left: 0;
    margin-top: 10px;
  }
}
</style>
