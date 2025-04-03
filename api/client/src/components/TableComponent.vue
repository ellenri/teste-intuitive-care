<script lang="ts">
import { defineComponent, ref, computed } from 'vue';

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
    itemsPerPageOptions: {
      type: Array as () => number[],
      default: () => [10, 25, 50]
    }
  },
  setup(props) {
    // Pagination
    const currentPage = ref(1);
    const itemsPerPage = ref(props.itemsPerPageOptions[0]);
    
    // Sorting
    const sortBy = ref('');
    const sortDirection = ref('asc');
    
    // Filters
    const filters = ref<{ [key: string]: string }>({});
    
    // Search
    const searchQuery = ref('');
    
    // Active Filters Count
    const activeFiltersCount = computed(() => {
      return Object.values(filters.value).filter(val => val && val.trim() !== '').length;
    });
    
    // Selected columns for filtering
    const selectedColumns = ref<string[]>([]);
    const toggleColumnSelection = (key: string) => {
      const index = selectedColumns.value.indexOf(key);
      if (index === -1) {
        selectedColumns.value.push(key);
      } else {
        selectedColumns.value.splice(index, 1);
      }
    };
    
    // Compute filtered data
    const filteredData = computed(() => {
      let result = [...props.data];
      
      // Apply search filter
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        result = result.filter(row => {
          return Object.values(row).some(value => 
            String(value).toLowerCase().includes(query)
          );
        });
      }
      
      // Apply column filters
      Object.entries(filters.value).forEach(([key, value]) => {
        if (value) {
          result = result.filter(row => 
            String(row[key]).toLowerCase().includes(value.toLowerCase())
          );
        }
      });
      
      // Apply sorting
      if (sortBy.value) {
        result.sort((a, b) => {
          const aValue = a[sortBy.value];
          const bValue = b[sortBy.value];
          
          if (aValue === bValue) return 0;
          
          const comparison = aValue > bValue ? 1 : -1;
          return sortDirection.value === 'asc' ? comparison : -comparison;
        });
      }
      
      return result;
    });
    
    // Compute paginated data
    const paginatedData = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value;
      const end = start + itemsPerPage.value;
      return filteredData.value.slice(start, end);
    });
    
    // Compute total pages
    const totalPages = computed(() => 
      Math.ceil(filteredData.value.length / itemsPerPage.value)
    );
    
    // Get status badge class based on status value
    const getStatusClass = (status: string) => {
      const statusLower = status.toLowerCase();
      if (statusLower === 'completed') return 'status-completed';
      if (statusLower === 'scheduled') return 'status-scheduled';
      if (statusLower === 'waiting') return 'status-waiting';
      if (statusLower === 'cancelled') return 'status-cancelled';
      return 'status-default';
    };
    
    // Handle sort change
    const handleSort = (key: string) => {
      if (sortBy.value === key) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
      } else {
        sortBy.value = key;
        sortDirection.value = 'asc';
      }
    };
    
    // Handle filter change
    const handleFilter = (key: string, value: string) => {
      filters.value = { ...filters.value, [key]: value };
    };
    
    // Clear all filters
    const clearFilters = () => {
      filters.value = {};
      searchQuery.value = '';
    };
    
    // Handle page change
    const changePage = (page: number) => {
      currentPage.value = page;
    };
    
    // Handle items per page change
    const changeItemsPerPage = (items: number) => {
      itemsPerPage.value = items;
      currentPage.value = 1; // Reset to first page
    };
    
    // Format date
    const formatDate = (dateString: string) => {
      const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };
    
    return {
      currentPage,
      itemsPerPage,
      sortBy,
      sortDirection,
      filters,
      searchQuery,
      activeFiltersCount,
      selectedColumns,
      filteredData,
      paginatedData,
      totalPages,
      getStatusClass,
      handleSort,
      handleFilter,
      clearFilters,
      changePage,
      changeItemsPerPage,
      toggleColumnSelection,
      formatDate
    };
  }
});
</script>

<template>
  <div class="table-container">
    <!-- Header Controls -->
    <div class="table-controls">
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Busqueda..." 
          class="search-input"
        />
        <div class="search-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
      </div>
      
      <div class="filter-toggle">
        <button class="filter-button" @click="selectedColumns = selectedColumns.length ? [] : columns.map(col => col.key)">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
          </svg>
          Filters
          <span v-if="activeFiltersCount > 0" class="filter-badge">{{ activeFiltersCount }}</span>
        </button>
        
        <button v-if="activeFiltersCount > 0" class="clear-button" @click="clearFilters">
          Clear All
        </button>
      </div>
    </div>
    
    <!-- Filter Panel -->
    <div class="filters-panel" v-if="selectedColumns.length > 0">
      <div class="filters-container">
        <div v-for="column in columns.filter(col => selectedColumns.includes(col.key))" :key="column.key" class="filter-item">
          <label>{{ column.label }}</label>
          <input 
            type="text" 
            v-model="filters[column.key]"
            @input="handleFilter(column.key, filters[column.key] || '')"
            :placeholder="`Filter by ${column.label.toLowerCase()}`"
            class="filter-input"
          />
        </div>
      </div>
    </div>
    
    <!-- Table -->
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
    
    <!-- Pagination -->
    <div class="pagination-container">
      <div class="items-per-page">
        <span>Mostrando</span>
        <select v-model="itemsPerPage" @change="changeItemsPerPage(itemsPerPage)">
          <option v-for="option in itemsPerPageOptions" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
        <span>entradas</span>
      </div>
      
      <div class="pagination-controls">
        <button 
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="pagination-button prev"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M15 18l-6-6 6-6"></path>
          </svg>
          anterior
        </button>
        
        <div class="page-buttons">
          <button 
            v-for="page in totalPages" 
            :key="page"
            @click="changePage(page)"
            :class="{ active: currentPage === page }"
            class="page-button"
          >
            {{ page }}
          </button>
        </div>
        
        <button 
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="pagination-button next"
        >
        próximo
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 18l6-6-6-6"></path>
          </svg>
        </button>
      </div>
      
      <div class="page-info">
        Mostrando {{ filteredData.length > 0 ? (currentPage - 1) * itemsPerPage + 1 : 0 }} a 
        {{ Math.min(currentPage * itemsPerPage, filteredData.length) }} 
        de {{ filteredData.length }} entradas
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

.filter-toggle {
  display: flex;
  gap: 10px;
  align-items: center;
}

.filter-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 15px;
  background-color: #f9fbfd;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-button:hover {
  background-color: #edf2f7;
}

.filter-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 10px;
  background-color: #0091bd;
  color: white;
  font-size: 11px;
  font-weight: 600;
}

.clear-button {
  padding: 10px 15px;
  background-color: transparent;
  border: none;
  font-size: 14px;
  color: #0091bd;
  cursor: pointer;
  font-weight: 500;
}

.clear-button:hover {
  text-decoration: underline;
}

.filters-panel {
  padding: 15px 20px;
  background-color: #f9fbfd;
  border-bottom: 1px solid #edf2f7;
}

.filters-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.filter-item {
  min-width: 200px;
  flex: 1;
}

.filter-item label {
  display: block;
  margin-bottom: 5px;
  font-size: 12px;
  font-weight: 500;
  color: #718096;
}

.filter-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.2s;
  background-color: #ffffff;
}

.filter-input:focus {
  border-color: #0091bd;
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 145, 189, 0.1);
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