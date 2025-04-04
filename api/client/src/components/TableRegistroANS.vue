<script setup lang="ts">
import { ref } from 'vue';
import TableComponent from './TableComponent.vue';

// Define our column structure with column types
const columns = [
  { key: 'registroAns', label: 'Reg. ANS', sortable: true },
  { key: 'cnpj', label: 'CNPJ', sortable: true },
  { key: 'razaoSocial', label: 'Razão Social', sortable: true },
  { key: 'nomeFantasia', label: 'Nome Fantasia', sortable: true },
  { key: 'modalidade', label: 'Modalidade', sortable: true },
  { key: 'logradouro', label: 'Logradouro', sortable: true },
  { key: 'complemento', label: 'Complemento', sortable: true },
  { key: 'bairro', label: 'Bairro', sortable: true },
  { key: 'cidade', label: 'Cidade', sortable: true },
  { key: 'uf', label: 'UF', sortable: true },
  { key: 'cep', label: 'CEP', sortable: true },
  { key: 'ddd', label: 'DDD', sortable: true },
  { key: 'telefone', label: 'Telefone', sortable: true },
  { key: 'fax', label: 'Fax', sortable: true },
  { key: 'enderecoEletronico', label: 'Endereço Eletrônico', sortable: true },
  { key: 'representante', label: 'Representante', sortable: true }
];


</script>

<template>
  <div class="demo-container">
    <h1>Registro ANS</h1>
    <p class="description">Consulte informações sobre operadoras de planos de saúde registradas na ANS.</p>
    
    <TableComponent 
      :columns="columns" 
      :data="[]"
      :items-per-page-options="[5, 10, 20]" 
    />
  </div>
</template>

<style scoped>
.demo-container {
  width: 100%;
  margin: 0 auto;
}

h1 {
  color: #0091bd;
  margin-bottom: 10px;
  font-size: 32px;
  font-weight: 600;
}

.description {
  color: #718096;
  font-size: 16px;
  margin-bottom: 30px;
}

/* Add styles for table headers to align them in one line */
.table-header th {
  white-space: nowrap;
  text-align: left;
  padding: 10px;
}

/* Ensure DDD and Representante headers are aligned in one line */
th {
  white-space: nowrap;
}
</style>