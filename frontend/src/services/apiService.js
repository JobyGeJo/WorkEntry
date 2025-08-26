import axios from 'axios';

const apiClient = axios.create({
baseURL: '/api/v1', // The proxy will handle the redirect
withCredentials: true, // Crucial for sending session cookies
});

// Timesheet Services
const createTimesheet = (payload) => {
return apiClient.post('/timesheets', payload);
};

const getMyTimesheets = () => {
// The backend uses the session to identify the user
return apiClient.get('/timesheets');
};

// Admin Services
const getAllUsers = () => {
return apiClient.get('/users');
};

const getTimesheetsByUserId = (userId) => {
return apiClient.get(`/timesheets?user_id=${userId}`);
};

export default {
createTimesheet,
getMyTimesheets,
getAllUsers,
getTimesheetsByUserId,
};