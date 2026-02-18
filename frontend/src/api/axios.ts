import axios from 'axios';
import {BASE_URL} from "./constants";


const instance = axios.create({ baseURL: BASE_URL, validateStatus: () => true });

instance.interceptors.request.use(
	(request) => {
		return request;
	},
	(error) => {
		return Promise.reject(error);
	},
);

export const Axios = () => instance;
