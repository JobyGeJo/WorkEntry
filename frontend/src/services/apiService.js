import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api/v1',
  withCredentials: true,
});

// Timesheet Services
const createTimesheet = (payload) => apiClient.post('/timesheets', payload);
const getMyTimesheets = (params) => apiClient.get('/timesheets', { params });

// ADD THIS NEW FUNCTION
const getTimesheetById = (timesheetId) => {
  return apiClient.get(`/timesheets/${timesheetId}`);
};

// Admin Services
const getAllUsers = () => apiClient.get('/users');
const getTimesheetsByUserId = (userId, params) => {
  return apiClient.get(`/timesheets`, { params: { user_id: userId, ...params } });
};

export default {
  createTimesheet,
  getMyTimesheets,
  getTimesheetById, // <-- And export it here
  getAllUsers,
  getTimesheetsByUserId,
};