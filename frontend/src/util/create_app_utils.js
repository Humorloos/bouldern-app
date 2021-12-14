import {createApp} from 'vue/dist/vue.esm-bundler';
import {createStore} from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import $ from 'jquery';

export const createAppInEl = (options, store, selector, components) => {
  const app = createApp(options, convertDatasetToTyped($(selector).data()));
  if (store != null) {
    app.use(store);
  }
  components.forEach((component) => app.component(component.name, component));
  app.mount(selector);
  return app;
};

export const createSharedStore = (modules) => {
  return createStore({
    plugins: [
      createPersistedState({
        paths: Object.entries(modules).map(
            ([mName, m]) => 'persistentPaths' in m ? m.persistentPaths
                .map((path) => mName + '.' + path) : [],
        ).flat(),
      }),
    ],
    modules: modules,
    strict: process.env.NODE_ENV !== 'production',
  });
};

const datasetDatatypePostfix = 'Datatype';

const convertDatasetToTyped = (dataset) => {
  const keys = Object.keys(dataset);
  keys.forEach(function(key) {
    const datatypeKey = key + datasetDatatypePostfix;
    if (datatypeKey in dataset) {
      const datatype = dataset[datatypeKey];
      switch (datatype) {
        case 'String': // already string, do nothing
          break;
        case 'Number':
          dataset[key] = Number(dataset[key]);
          break;
        case 'Boolean':
          dataset[key] = dataset[key] === 'true';
          break;
        default: // do nothing
      }
      delete dataset[datatypeKey];
    }
  });
  return dataset;
};
