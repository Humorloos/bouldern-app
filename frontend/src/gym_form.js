import {createAppInEl} from "@/util/create_app_utils";
import Modal from "@/components/Modal";
import GymForm from "@/components/GymForm";
import "vue-select/dist/vue-select.css";

// Create and mount our apps
createAppInEl({}, null, "#app", [GymForm, Modal]);
