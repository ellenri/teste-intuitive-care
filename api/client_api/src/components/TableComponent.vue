<script lang="ts">
import { defineComponent, ref, computed, watch } from 'vue';

interface TableRow {
  id: number;
  [key: string]: any;
}

interface Column {
  key: string;
  label: string;
  sortable?: boolean;
  type?: 'text' | 'status' | 'date';
}

export default defineComponent({
  name: 'TableComponent',
  props: {
    columns: {
      type: Array as () => Column[],
      required: true
    },
    data: {
      type: Array as () => TableRow[],
      required: true
    },
    currentPage: {
      type: Number,
      default: 1
    },
    itemsPerPage: {
      type: Number,
      default: 10
    },
    itemsPerPageOptions: {
      type: Array as () => number[],
      default: () => [10, 25, 50]
    },
    totalItems: {
      type: Number,
      default: 0
    },
    totalPages: {
      type: Number,
      default: 0
    },
    searchQuery: {
      type: String,
      default: ''
    }
  },
  emits: ['page-change', 'items-per-page-change', 'search', 'clear-search'],
  setup(props, { emit }) {    
    const currentPage = computed({
      get: () => props.currentPage,
      set: (value) => emit('page-change', value)
    });
    
    const itemsPerPage = computed({
      get: () => props.itemsPerPage,
      set: (value) => emit('items-per-page-change', value)
    });
    
    // Ordenar
    const sortBy = ref('');
    const sortDirection = ref('asc');
    
    // Buscar
    const searchQuery = ref(props.searchQuery);
    
    // Watch para mudanças na propriedade de consulta de pesquisa
    watch(() => props.searchQuery, (newValue) => {
      searchQuery.value = newValue;
    });
    
    // Watch para mudanças na propriedade de consulta de pesquisa
    let searchTimeout: number | null = null;
    watch(searchQuery, (newValue) => {
      if (searchTimeout) {
        clearTimeout(searchTimeout);
      }
         
      searchTimeout = window.setTimeout(() => {
        emit('search', newValue);
      }, 500); 
    });
    
    const paginatedData = computed(() => {
      return props.data || [];
    });
    
    const getStatusClass = (status: string) => {
      const statusLower = status.toLowerCase();
      if (statusLower === 'completed') return 'status-completed';
      if (statusLower === 'scheduled') return 'status-scheduled';
      if (statusLower === 'waiting') return 'status-waiting';
      if (statusLower === 'cancelled') return 'status-cancelled';
      return 'status-default';
    };
      
    const handleSort = (key: string) => {
      if (sortBy.value === key) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
      } else {
        sortBy.value = key;
        sortDirection.value = 'asc';
      }
    };
        
    const changePage = (page: number) => {
      currentPage.value = page;
    };
     
    const changeItemsPerPage = (items: number) => {
      itemsPerPage.value = items;    
      currentPage.value = 1;
    };
      
    const formatDate = (dateString: string) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString();
    };
    
    return {
      currentPage,
      itemsPerPage,
      sortBy,
      sortDirection,
      searchQuery,
      paginatedData,
      totalPages: computed(() => props.totalPages),
      totalItems: computed(() => props.totalItems),
      getStatusClass,
      handleSort,
      changePage,
      changeItemsPerPage,
      formatDate
    };
  }
});
</script>

<template>
  <div class="table-container"> 
    <div class="table-controls">
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Buscar..." 
          class="search-input"
        />
        <div class="search-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
      </div>
    </div>
       
    <div class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th 
              v-for="column in columns" 
              :key="column.key"
              @click="column.sortable !== false ? handleSort(column.key) : null"
              :class="{ 
                sortable: column.sortable !== false,
                sorted: sortBy === column.key,
                asc: sortBy === column.key && sortDirection === 'asc',
                desc: sortBy === column.key && sortDirection === 'desc'
              }"
            >
              {{ column.label }}
              <span v-if="column.sortable !== false" class="sort-icon">
                <svg v-if="sortBy !== column.key" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M7 10l5 5 5-5"></path>
                </svg>
                <svg v-else-if="sortDirection === 'asc'" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M18 15l-6-6-6 6"></path>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M6 9l6 6 6-6"></path>
                </svg>
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in paginatedData" :key="row.id">
            <td v-for="column in columns" :key="column.key" :class="{ 'status-cell': column.type === 'status' }">
              <span v-if="column.type === 'status'" :class="['status-badge', getStatusClass(row[column.key])]">
                {{ row[column.key] }}
              </span>
              <span v-else-if="column.type === 'date'">
                {{ formatDate(row[column.key]) }}
              </span>
              <span v-else>
                {{ row[column.key] }}
              </span>
            </td>
          </tr>
          <tr v-if="paginatedData.length === 0">
            <td :colspan="columns.length" class="no-data">
              No data available
            </td>
          </tr>
        </tbody>
      </table>
    </div>
       
    <div class="pagination-container">
      <div class="items-per-page">
        <span>Mostrar:</span>
        <select v-model="itemsPerPage">
          <option v-for="option in itemsPerPageOptions" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>
      
      <div class="page-info">
        Mostrando {{ ((currentPage - 1) * itemsPerPage) + 1 }} a {{ Math.min(currentPage * itemsPerPage, totalItems) }} de {{ totalItems }} entradas
      </div>
      
      <div class="pagination-controls">
        <button 
          class="pagination-button" 
          @click="changePage(1)" 
          :disabled="currentPage === 1"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="11 17 6 12 11 7"></polyline>
            <polyline points="18 17 13 12 18 7"></polyline>
          </svg>
        </button>
        
        <button 
          class="pagination-button" 
          @click="changePage(currentPage - 1)" 
          :disabled="currentPage === 1"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          Anterior
        </button>
        
        <div class="page-buttons">
          <button 
            v-for="page in totalPages" 
            :key="page" 
            @click="changePage(page)" 
            class="page-button" 
            :class="{ active: currentPage === page }"
            v-show="page === 1 || page === totalPages || (page >= currentPage - 1 && page <= currentPage + 1)"
          >
            {{ page }}
          </button>
        </div>
        
        <button 
          class="pagination-button" 
          @click="changePage(currentPage + 1)" 
          :disabled="currentPage === totalPages || totalPages === 0"
        >
          Próximo
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
        
        <button 
          class="pagination-button" 
          @click="changePage(totalPages)" 
          :disabled="currentPage === totalPages || totalPages === 0"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="13 17 18 12 13 7"></polyline>
            <polyline points="6 17 11 12 6 7"></polyline>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.table-container {
  width: 100%;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  font-family: 'Inter', sans-serif;
}

.table-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #ffffff;
  border-bottom: 1px solid #edf2f7;
}

.search-container {
  flex: 1;
  max-width: 300px;
  position: relative;
}

.search-input {
  width: 100%;
  padding: 10px 15px 10px 40px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s;
  background-color: #f9fbfd;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #a0aec0;
}

.search-input:focus {
  border-color: #0091bd;
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 145, 189, 0.1);
  background-color: #ffffff;
}

.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background-color: #f9fbfd;
  padding: 15px 5px;
  text-align: left;
  font-weight: 600;
  color: #64748b;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #edf2f7;
  position: relative;
}

.data-table th.sortable {
  cursor: pointer;
  user-select: none;
}

.data-table th.sortable:hover {
  background-color: #edf2f7;
}

.data-table th.sorted {
  background-color: #e6f7fb;
  color: #0091bd;
}

.sort-icon {
  margin-left: 5px;
  vertical-align: middle;
}

.data-table td {
  padding: 16px 20px;
  border-bottom: 1px solid #edf2f7;
  color: #2d3748;
  font-size: 14px;
}

.data-table tr:hover td {
  background-color: #f7fafc;
}

.data-table tr:last-child td {
  border-bottom: none;
}

.status-cell {
  padding-top: 12px !important;
  padding-bottom: 12px !important;
}

.status-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  text-align: center;
  min-width: 90px;
}

.status-completed {
  background-color: #e6f7eb;
  color: #0a7f3d;
}

.status-scheduled {
  background-color: #e6f7fb;
  color: #0091bd;
}

.status-waiting {
  background-color: #fef6e6;
  color: #cb7e04;
}

.status-cancelled {
  background-color: #feeeee;
  color: #e12d39;
}

.status-default {
  background-color: #edf2f7;
  color: #4a5568;
}

.no-data {
  text-align: center;
  padding: 30px !important;
  color: #a0aec0;
}

.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #f9fbfd;
  border-top: 1px solid #edf2f7;
}

.items-per-page {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #4a5568;
}

.items-per-page select {
  padding: 6px 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background-color: white;
  color: #2d3748;
}

.pagination-controls {
  display: flex;
  gap: 5px;
  align-items: center;
}

.pagination-button {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 14px;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  color: #4a5568;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.pagination-button:hover:not(:disabled) {
  background-color: #f7fafc;
  border-color: #cbd5e0;
}

.pagination-button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.page-buttons {
  display: flex;
  gap: 5px;
}

.page-button {
  min-width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  color: #4a5568;
  font-size: 14px;
  transition: all 0.2s;
}

.page-button:hover {
  background-color: #f7fafc;
}

.page-button.active {
  background-color: #0091bd;
  color: white;
  border-color: #0091bd;
}

.page-info {
  font-size: 14px;
  color: #718096;
}

@media (max-width: 768px) {
  .table-controls, .pagination-container {
    flex-direction: column;
    gap: 15px;
  }
  
  .search-container {
    max-width: 100%;
  }
  
  .pagination-controls {
    order: 1;
  }
  
  .page-info {
    order: 3;
  }
  
  .items-per-page {
    order: 2;
  }
}
</style>