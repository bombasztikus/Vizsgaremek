<template>
    <nav class="navbar navbar-dark bg-dark">
        <form class="container-fluid justify-content-start">
            <RouterLink :to="{ name: 'home' }" class="btn btn-outline-primary me-2">Főoldal</RouterLink>
            <!-- <a href="{{ url_for('routes.rendeles') }}" class="btn btn-sm btn-outline-danger">Rendelés</a> -->
            <!-- {% if current_user.is_authenticated %}
            <li class="nav-item dropdown ms-aut">
                <a class="btn btn-sm btn-outline-danger" href="#" role="button" data-bs-toggle="dropdown"
                    aria-expanded="false">
                    Profil
                </a>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="{{ url_for('routes.kosar') }}">Kosár</a></li>
                    <li><a class="dropdown-item" href="{{ url_for('routes.out') }}">Kijelentkezés</a></li>
                </ul>
            </li>
            {% else %}
            <a href="{{ url_for('routes.reg') }}" class="btn btn-sm btn-outline-danger">Regisztráció</a>
            <a href="{{ url_for('routes.log') }}" class="btn btn-sm btn-outline-danger">Bejelentkezés</a>
            {% endif %} -->
        </form>
    </nav>
</template>
