import type { SearchCoverSchema } from "@/__generated__";
import { api } from "@/plugins/api.client.ts";

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
