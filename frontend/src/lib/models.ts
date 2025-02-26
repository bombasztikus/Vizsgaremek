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
    price: number;
    calories: number;
    image_url: string | null;
    has_image_url: boolean;
    fallback_image_url: string;
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

export type CartItem = {
    productId: number;
    quantity: number;
    price: number;
}

export type OrderCreationItem = {
    id: number;
    quantity: number;
}

export type OrderItem = {
    order_id: number;
    meal_id: number;
    quantity: number;
    is_error: boolean;
}

export type Order = APIModel & {
    user_id: number;
    date_created: string;
    address: string;
    is_completed: boolean;
    items: OrderItem[];
};

export type MinifiedOrder = {
    address: string;
    date_created: string;
    id: number;
    is_completed: boolean;
    is_error: boolean;
    user_id: number;
};

export type OrdersResponse = {
    is_error: boolean;
    items: MinifiedOrder[];
}
