import {createAppInEl} from '@/util/create_app_utils';
import GymMap from '@/components/GymMap';
import 'vue-select/dist/vue-select.css';

// Create and mount our apps
createAppInEl({}, null, '#app', [GymMap]);
