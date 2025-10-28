const API_BASE_URL = 'http://127.0.0.1:8000/api';

const apiService = {
  
  submitFoundItem: async (formData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/found-items/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Error from server');
      }

      return await response.json();
    } catch (error) {
      console.error('API error', error);
      throw error;
    }
  },

  //add more services like submitFoundItem
  
};
export default apiService;
