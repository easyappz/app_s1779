import { instance } from './axios';

/**
 * Register a new user
 * @param {string} username - Username (3-50 characters)
 * @param {string} password - Password (6-128 characters)
 * @returns {Promise} Response with token and user data
 */
export const register = async (username, password) => {
  try {
    const response = await instance.post('/api/auth/register', {
      username,
      password,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Login user
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise} Response with token and user data
 */
export const login = async (username, password) => {
  try {
    const response = await instance.post('/api/auth/login', {
      username,
      password,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Logout user
 * @param {string} token - Authentication token
 * @returns {Promise} Empty response on success
 */
export const logout = async (token) => {
  try {
    const response = await instance.post(
      '/api/auth/logout',
      {},
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};
