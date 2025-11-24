import { instance } from './axios';

/**
 * Get current authenticated member profile
 * @param {string} token - Authentication token
 * @returns {Promise} Response with member data
 */
export const getCurrentMember = async (token) => {
  try {
    const response = await instance.get('/api/members/me', {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};
