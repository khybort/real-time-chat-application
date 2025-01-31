import API from "./api";

export const login = async (username: string, password: string) => {
  const response = await API.post("/api/auth/login/", { username, password });
  localStorage.setItem("access", response.data.access);
  localStorage.setItem("refresh", response.data.refresh);
  localStorage.setItem("user", JSON.stringify(response.data.user));
  return response.data;
};

export const register = async (username: string, email: string ,password: string) => {
  return await API.post("/auth/register/", { username, email, password });
};

export const logout = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("user");
  window.location.href = "/login";
};
