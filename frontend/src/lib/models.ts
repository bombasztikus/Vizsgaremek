export enum APIErrorCode {
    unknown_error = 'unknown_error',
    account_creation_error = 'account_creation_error',
    invalid_credentials = 'invalid_credentials',
    not_found = 'not_found',
    user_not_found = 'user_not_found',
    invalid_user_id = 'invalid_user_id',
    invalid_enum_value = 'invalid_enum_value',
    invalid_price = 'invalid_price',
    meal_creation_error = 'meal_creation_error',
    invalid_currency = 'invalid_currency',
    invalid_calories = 'invalid_calories',
    invalid_url = 'invalid_url',
    invalid_stars = 'invalid_stars',
    unauthorized = 'unauthorized',
    email_unavailable = 'email_unavailable',
    invalid_payload = 'invalid_payload',
    invalid_email = 'invalid_email',
    invalid_full_name = 'invalid_full_name',
    invalid_password = 'invalid_password',
}

export type APIError = {
    css_class: string;
    error: string;
    error_code: APIErrorCode;
    http_code: number;
    is_error: boolean;
};

type APIModel = {
    id: number;
    is_error: boolean;
};

export type User = APIModel & {
    email: string;
    full_name: string;
    is_employee: boolean;
};

export enum MealType {
    FOOD = 'FOOD',
    BEVERAGE = 'BEVERAGE',
    MENU = 'MENU',
    DESSERT = 'DESSERT',
}

export type Meal = APIModel & {
    name: string;
    price: string;
    currency: string;
    calories: number;
    image_url: string | null;
    description: string | null;
    stars: number;
    type: string;
    is_free: boolean;
    display_price: string;
};

export type MealsResponse = {
    items: Meal[];
    type_display_name: string | null;
    type: MealType | null;
    is_error: boolean;
};
