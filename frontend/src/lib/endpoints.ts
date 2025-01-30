import type { MealType, User } from './models';

export const API_BASE = import.meta.env.VITE_API_BASE_URL;

export const GET_ALL_MEALS = '/meals';
export const GET_MEALS = (type: MealType) => `/meals/${type}`;
export const GET_USER = (id: User['id']) => `/users/${id}`;
export const POST_LOGIN = '/login';
export const POST_REGISTER = '/register';
export const POST_MEALS = (type: MealType) => `/meals/${type}`;
