// import './assets/main.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import 'bootstrap-icons/font/bootstrap-icons.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { faUtensils, faPizzaSlice, faMartiniGlassCitrus, faIceCream } from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(faUtensils, faPizzaSlice, faMartiniGlassCitrus, faIceCream)

const app = createApp(App);

app.component('font-awesome-icon', FontAwesomeIcon)

app.use(createPinia());
app.use(router);

app.mount('#app');
