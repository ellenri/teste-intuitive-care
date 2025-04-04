<script setup lang="ts">
import { ref } from 'vue';
import TableComponent from './TableComponent.vue';
import { fetchData, searchData } from '../services/api';

const data = ref([]);
const columns = ref([]);
const currentPage = ref(1);
const itemsPerPage = ref(10);
const totalItems = ref(0);
const totalPages = ref(0);
const searchQuery = ref('');
const isSearching = ref(false);
const searchMode = ref(false);



const dataForTable = async () => {
  searchMode.value = false;
  try {
    const response = await fetchData(currentPage.value, itemsPerPage.value);
    console.log(response);
    data.value = response.data;
    columns.value = response.headers.map((header: string) => (
      {
        key: header,
        label: header,
        sortable: true
      }
    ));
    totalItems.value = response.total_items;
    totalPages.value = response.total_pages;
  } catch (error) {
    console.error('Erro ao buscar dados:', error);
  }
};

const handleSearch = async (query: string) => {
  searchQuery.value = query;
  if(!searchMode.value) {
    currentPage.value = 1;
  }
  searchMode.value = true;
  
  try {
    if (query && query.trim() !== '') {
      isSearching.value = true;
      // Pass current page and itemsPerPage to search
      const response = await searchData(query, currentPage.value, itemsPerPage.value); 
      // Safely update data and pagination
      if (response && Array.isArray(response.data)) {
        data.value = response.data;
        // currentPage.value = 1;
        totalItems.value = response.total_items;
        totalPages.value = response.total_pages;
      } 
    } else {
      // If search query is empty, fetch initial data
      isSearching.value = false;
      await dataForTable(); // Fetch default data
    }
  } catch (error) {
    console.error('Erro ao buscar resultados:', error);
    // Ensure data is reset on error to avoid inconsistent state
    data.value = [];
    totalItems.value = 0;
    totalPages.value = 0;
    currentPage.value = 1;
    isSearching.value = false;
  }
};

const handleClearSearch = () => {
  searchQuery.value = '';
  isSearching.value = false;
  dataForTable();
};

dataForTable();

const handlePageChange = (page: number) => {
  currentPage.value = page;
  
  if (isSearching.value && searchQuery.value) {
    handleSearch(searchQuery.value);
  } else {
    dataForTable();
  }
};

const handleItemsPerPageChange = (perPage: number) => {
  itemsPerPage.value = perPage;
  currentPage.value = 1; 
  
  if (isSearching.value && searchQuery.value) {
    handleSearch(searchQuery.value);
  } else {
    dataForTable();
  }
};

const mockData = ref([
  { 
    id: 1,
    Registro_ANS: '123456', 
    CNPJ: '12.345.678/0001-90', 
    Razao_Social: 'Operadora de Saúde Exemplo S.A.', 
    Nome_Fantasia: 'Saúde Exemplo', 
    Modalidade: 'Medicina de Grupo', 
    Data_Registro_ANS: '2022-01-01', 
    Logradouro: 'Av. Paulista', 
    Numero: '100', 
    Complemento: 'Andar 10', 
    Bairro: 'Bela Vista', 
    Cidade: 'São Paulo', 
    UF: 'SP', 
    CEP: '01311-000', 
    DDD: '11', 
    Telefone: '3456-7890', 
    Fax: '3456-7891', 
    Endereco_eletronico: 'contato@saudeexemplo.com.br', 
    Representante: 'Maria Silva', 
    Cargo_Representante: 'Diretora', 
    Regiao_de_Comercializacao: 'Sudeste'
  },
  { 
    id: 2,
    Registro_ANS: '234567', 
    CNPJ: '23.456.789/0001-01', 
    Razao_Social: 'Plano de Saúde Familiar Ltda', 
    Nome_Fantasia: 'Plano Familiar', 
    Modalidade: 'Cooperativa Médica', 
    Data_Registro_ANS: '2022-02-01', 
    Logradouro: 'Rua Augusta', 
    Numero: '200', 
    Complemento: 'Sala 203', 
    Bairro: 'Consolação', 
    Cidade: 'São Paulo', 
    UF: 'SP', 
    CEP: '01305-000', 
    DDD: '11', 
    Telefone: '2345-6789', 
    Fax: '2345-6780', 
    Endereco_eletronico: 'atendimento@planofamiliar.com.br', 
    Representante: 'João Santos', 
    Cargo_Representante: 'Gerente', 
    Regiao_de_Comercializacao: 'Sudeste'
  },
  { 
    id: 3,
    Registro_ANS: '345678', 
    CNPJ: '34.567.890/0001-12', 
    Razao_Social: 'Cooperativa de Assistência à Saúde', 
    Nome_Fantasia: 'CoopSaúde', 
    Modalidade: 'Cooperativa Médica', 
    Data_Registro_ANS: '2022-03-01', 
    Logradouro: 'Av. Rebouças', 
    Numero: '300', 
    Complemento: 'Bloco B', 
    Bairro: 'Pinheiros', 
    Cidade: 'São Paulo', 
    UF: 'SP', 
    CEP: '05401-000', 
    DDD: '11', 
    Telefone: '3344-5566', 
    Fax: '3344-5567', 
    Endereco_eletronico: 'contato@coopsaude.com.br', 
    Representante: 'Ana Oliveira', 
    Cargo_Representante: 'Diretora', 
    Regiao_de_Comercializacao: 'Sudeste'
  },
  { 
    id: 4,
    Registro_ANS: '456789', 
    CNPJ: '45.678.901/0001-23', 
    Razao_Social: 'Seguradora de Saúde Nacional S.A.', 
    Nome_Fantasia: 'Saúde Nacional', 
    Modalidade: 'Seguradora Especializada em Saúde', 
    Data_Registro_ANS: '2022-04-01', 
    Logradouro: 'Rua Oscar Freire', 
    Numero: '400', 
    Complemento: 'Torre 1', 
    Bairro: 'Jardim Paulista', 
    Cidade: 'São Paulo', 
    UF: 'SP', 
    CEP: '01426-000', 
    DDD: '11', 
    Telefone: '3030-4040', 
    Fax: '3030-4041', 
    Endereco_eletronico: 'contato@saudenacional.com.br', 
    Representante: 'Carlos Rodrigues', 
    Cargo_Representante: 'Gerente', 
    Regiao_de_Comercializacao: 'Sudeste'
  },
  { 
    id: 5,
    Registro_ANS: '567890', 
    CNPJ: '56.789.012/0001-34', 
    Razao_Social: 'Administradora de Benefícios Saúde Total Ltda', 
    Nome_Fantasia: 'Saúde Total', 
    Modalidade: 'Administradora de Benefícios', 
    Data_Registro_ANS: '2022-05-01', 
    Logradouro: 'Av. Faria Lima', 
    Numero: '500', 
    Complemento: 'Conj. 1502', 
    Bairro: 'Itaim Bibi', 
    Cidade: 'São Paulo', 
    UF: 'SP', 
    CEP: '04538-000', 
    DDD: '11', 
    Telefone: '2020-3030', 
    Fax: '2020-3031', 
    Endereco_eletronico: 'contato@saudetotal.com.br', 
    Representante: 'Patricia Lima', 
    Cargo_Representante: 'Diretora', 
    Regiao_de_Comercializacao: 'Sudeste'
  }
]);
</script>

<template>
  <div class="demo-container">
    <h1>Registro ANS</h1>
    <p class="description">Consulte informações sobre operadoras de planos de saúde registradas na ANS.</p>
    
    <TableComponent 
      :columns="columns" 
      :data="data" 
      :current-page="currentPage"
      :items-per-page="itemsPerPage"
      :items-per-page-options="[5, 10, 20]" 
      :total-items="totalItems"
      :total-pages="totalPages"
      :search-query="searchQuery"
      @page-change="handlePageChange"
      @items-per-page-change="handleItemsPerPageChange"
      @search="handleSearch"
      @clear-search="handleClearSearch"
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