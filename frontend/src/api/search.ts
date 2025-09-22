import { Axios } from "./axios";
import { SEARCH_URL } from "./constants";


export type SearchRequest = {
    query: string;
    projectRepo: string;
}

export const getSearchResult = (searchRequest:SearchRequest) => {
    const params = {
        query: searchRequest.query,
        projectRepo: searchRequest.projectRepo,
    }
    return Axios().get(SEARCH_URL, { params });
};
