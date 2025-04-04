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
      
      const response = await searchData(query, currentPage.value, itemsPerPage.value);       
      if (response && Array.isArray(response.data)) {
        data.value = response.data;       
        totalItems.value = response.total_items;
        totalPages.value = response.total_pages;
      } 
    } else {      
      isSearching.value = false;
      await dataForTable(); 
    }
  } catch (error) {
    console.error('Erro ao buscar resultados:', error); 
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
</script>

<template>
  <div class="demo-container">
    <h1>Operadoras Ativas ANS</h1>
    <p class="description">Consulte informações sobre operadoras ativas de saúde registradas na ANS.</p>
    
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

.table-header th {
  white-space: nowrap;
  text-align: left;
  padding: 10px;
}

th {
  white-space: nowrap;
}
</style>