import axios from 'axios';

const baseURL =  'http://localhost:8081';

const instance = axios.create({ baseURL, validateStatus: () => true });

instance.interceptors.request.use(
	(request) => {
		return request;
	},
	(error) => {
		return Promise.reject(error);
	},
);

export const Axios = () => instance;
