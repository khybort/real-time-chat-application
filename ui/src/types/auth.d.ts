export interface LoginResponse {
  token: string;
}

export interface User {
  id: number;
  username: string;
  role: 'user' | 'manager';
}
