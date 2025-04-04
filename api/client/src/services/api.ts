import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000'; // URL base da sua API Flask

export const fetchData = async (page = 1, perPage = 20) => {
  try {
    const response = await axios.get(`${API_URL}/data`, {
      params: {
        page,
        per_page: perPage
      }
    });
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar dados:', error);
    throw error; // Rejeita a promise para que o componente possa lidar com o erro
  }
};

export const searchData = async (query: string) => {
  try {
    const response = await axios.get(`${API_URL}/search`, {
      params: {
        query
      }
    });
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar resultados:', error);
    throw error; // Rejeita a promise para que o componente possa lidar com o erro
  }
};