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
  { key: 'enderecoEletronico', label: 'E-mail', sortable: true },
  { key: 'representante', label: 'Representante', sortable: true }
];

// Sample data matching the ANS registry theme
const mockData = ref([
  { 
    id: 1,
    registroAns: '123456', 
    cnpj: '12.345.678/0001-90', 
    razaoSocial: 'Operadora de Saúde Exemplo S.A.', 
    nomeFantasia: 'Saúde Exemplo', 
    modalidade: 'Medicina de Grupo', 
    logradouro: 'Av. Paulista', 
    complemento: 'Andar 10', 
    bairro: 'Bela Vista', 
    cidade: 'São Paulo', 
    uf: 'SP', 
    cep: '01311-000', 
    ddd: '11', 
    telefone: '3456-7890', 
    fax: '3456-7891', 
    enderecoEletronico: 'contato@saudeexemplo.com.br', 
    representante: 'Maria Silva' 
  },
  { 
    id: 2,
    registroAns: '234567', 
    cnpj: '23.456.789/0001-01', 
    razaoSocial: 'Plano de Saúde Familiar Ltda', 
    nomeFantasia: 'Plano Familiar', 
    modalidade: 'Cooperativa Médica', 
    logradouro: 'Rua Augusta', 
    complemento: 'Sala 203', 
    bairro: 'Consolação', 
    cidade: 'São Paulo', 
    uf: 'SP', 
    cep: '01305-000', 
    ddd: '11', 
    telefone: '2345-6789', 
    fax: '2345-6780', 
    enderecoEletronico: 'atendimento@planofamiliar.com.br', 
    representante: 'João Santos' 
  },
  { 
    id: 3,
    registroAns: '345678', 
    cnpj: '34.567.890/0001-12', 
    razaoSocial: 'Cooperativa de Assistência à Saúde', 
    nomeFantasia: 'CoopSaúde', 
    modalidade: 'Cooperativa Médica', 
    logradouro: 'Av. Rebouças', 
    complemento: 'Bloco B', 
    bairro: 'Pinheiros', 
    cidade: 'São Paulo', 
    uf: 'SP', 
    cep: '05401-000', 
    ddd: '11', 
    telefone: '3344-5566', 
    fax: '3344-5567', 
    enderecoEletronico: 'contato@coopsaude.com.br', 
    representante: 'Ana Oliveira' 
  },
  { 
    id: 4,
    registroAns: '456789', 
    cnpj: '45.678.901/0001-23', 
    razaoSocial: 'Seguradora de Saúde Nacional S.A.', 
    nomeFantasia: 'Saúde Nacional', 
    modalidade: 'Seguradora Especializada em Saúde', 
    logradouro: 'Rua Oscar Freire', 
    complemento: 'Torre 1', 
    bairro: 'Jardim Paulista', 
    cidade: 'São Paulo', 
    uf: 'SP', 
    cep: '01426-000', 
    ddd: '11', 
    telefone: '3030-4040', 
    fax: '3030-4041', 
    enderecoEletronico: 'contato@saudenacional.com.br', 
    representante: 'Carlos Rodrigues' 
  },
  { 
    id: 5,
    registroAns: '567890', 
    cnpj: '56.789.012/0001-34', 
    razaoSocial: 'Administradora de Benefícios Saúde Total Ltda', 
    nomeFantasia: 'Saúde Total', 
    modalidade: 'Administradora de Benefícios', 
    logradouro: 'Av. Faria Lima', 
    complemento: 'Conj. 1502', 
    bairro: 'Itaim Bibi', 
    cidade: 'São Paulo', 
    uf: 'SP', 
    cep: '04538-000', 
    ddd: '11', 
    telefone: '2020-3030', 
    fax: '2020-3031', 
    enderecoEletronico: 'contato@saudetotal.com.br', 
    representante: 'Patricia Lima' 
  }
]);
</script>

<template>
  <div class="demo-container">
    <h1>Registro ANS</h1>
    <p class="description">Consulte informações sobre operadoras de planos de saúde registradas na ANS.</p>
    
    <TableComponent 
      :columns="columns" 
      :data="mockData" 
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