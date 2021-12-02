import {createApp} from "vue/dist/vue.esm-bundler";
import {createStore} from "vuex";
import createPersistedState from "vuex-persistedstate";

import HelloWorld from "@/components/HelloWorld";


export const createAppInEl = () => {
    createApp({})
        .component('page-layout', HelloWorld)
        .mount('#app')
}

export const createSharedStore = (modules) => {
    return new createStore({
        plugins: [
            createPersistedState({
                paths: Object.entries(modules).map(
                    ([mName, m]) => 'persistentPaths' in m ? m.persistentPaths.map(path => mName + "." + path) : []
                ).flat(),
            })
        ],
        modules: modules,
        strict: process.env.NODE_ENV !== "production",
    });
}
