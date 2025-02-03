<template>
    <div class="mt-5 row g-3 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 justify-content-center">
        <div class="card h-100 rounded-4 overflow-hidden col" style="max-width: 400px;">
            <form class="card-body d-flex flex-column">
                <div class="mb-3">
                    <label for="inputEmail" class="form-label">Email cím</label>
                    <input type="email" class="form-control" id="inputEmail">
                </div>
                <div class="mb-3">
                    <label for="inputPassword" class="form-label">Jelszó</label>
                    <input type="password" class="form-control" id="inputPassword">
                </div>
                <button type="submit" class="btn btn-primary">Bejelentkezés</button>
            </form>
        </div>
    </div>
</template>
