import type { SearchCoverSchema } from "@/__generated__";
import { api } from "@/plugins/api.client";

export const romApi = api;

async function searchCover({
  searchTerm,
}: {
  searchTerm: string;
}): Promise<{ data: SearchCoverSchema[] }> {
  return api.get("/search/cover", { params: { search_term: searchTerm } });
}

export default {
  searchCover,
};
