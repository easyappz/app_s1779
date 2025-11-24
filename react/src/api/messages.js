import { instance } from './axios';

/**
 * Get messages from group chat
 * @param {string} token - Authentication token
 * @param {number} limit - Number of messages per page (optional)
 * @param {number} offset - Offset for pagination (optional)
 * @returns {Promise} Response with messages list
 */
export const getMessages = async (token, limit = 50, offset = 0) => {
  try {
    const response = await instance.get('/api/messages', {
      headers: {
        Authorization: `Token ${token}`,
      },
      params: {
        limit,
        offset,
      },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Send a new message to group chat
 * @param {string} text - Message text (1-5000 characters)
 * @param {string} token - Authentication token
 * @returns {Promise} Response with created message
 */
export const sendMessage = async (text, token) => {
  try {
    const response = await instance.post(
      '/api/messages',
      {
        text,
      },
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
