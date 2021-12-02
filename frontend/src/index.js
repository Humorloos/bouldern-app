import {createAppInEl} from "@/util/create_app_utils";
import Modal from "@/components/Modal";
import GymForm from "@/components/GymForm";

// Create and mount our apps
createAppInEl({}, null, "#app", [GymForm, Modal]);