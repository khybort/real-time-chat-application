import API from "./api";

export const fetchUserDetails = async () => {
  const response = await API.get("/users/me/");
  return response.data;
};
