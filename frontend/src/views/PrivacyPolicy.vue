<template>
  <app-view>
    <template #main>
      <v-container>
        <v-row>
          <v-col>
            <div
              class="text-h4"
              v-text=" $t('privacyPolicy.title') "
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <p
              class="text-body-2 text-justify"
              v-text="$t('privacyPolicy.introduction')"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <div
              class="text-subtitle-1"
              v-text=" $t('privacyPolicy.informationCollection.title') "
            />
            <p class="text-body-2 text-justify">
              {{ $t('privacyPolicy.informationCollection.body') }}
            </p>
            <ul>
              <li
                class="text-body-2 text-justify"
              >
                <a
                  href="https://www.google.com/policies/privacy/"
                  target="_blank"
                  rel="noopener noreferrer"
                >Google Play Services</a>
              </li>
            </ul>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <div
              class="text-subtitle-1"
              v-text="$t('privacyPolicy.logData.title')"
            />
            <p
              class="text-body-2 text-justify"
              v-text="$t('privacyPolicy.logData.body')"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <div
              class="text-subtitle-1"
              v-text="$t('privacyPolicy.cookies.title')"
            />
            <p
              class="text-body-2 text-justify"
              v-text="$t('privacyPolicy.cookies.body')"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <div
              class="text-subtitle-1"
              v-text="$t('privacyPolicy.serviceProviders.title')"
            />
            <p
              class="text-body-2 text-justify"
              v-text="$t('privacyPolicy.serviceProviders.introduction')"
            />
            <ul>
              <li
                class="text-body-2 text-justify"
              >
                {{
                  $t('privacyPolicy.serviceProviders.reasons.facilitateService')
                }}
              </li>
              <li
                class="text-body-2 text-justify"
              >
                {{
                  $t('privacyPolicy.serviceProviders.reasons.provideService')
                }}
              </li>
              <li
                class="text-body-2 text-justify"
              >
                {{
                  // eslint-disable-next-line max-len
                  $t('privacyPolicy.serviceProviders.reasons.serviceRelatedServices')
                }}
              </li>
              <li
                class="text-body-2 text-justify"
              >
                {{
                  // eslint-disable-next-line max-len
                  $t('privacyPolicy.serviceProviders.reasons.analysisAssistance')
                }}
              </li>
            </ul>
            <p
              class="text-body-2 text-justify"
              v-text="$t('privacyPolicy.serviceProviders.body')"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <div
              class="text-subtitle-1"
              v-text="$t('privacyPolicy.security.title')"
            />
            <p
              class="text-body-2 text-justify"
              v-text="$t('privacyPolicy.security.body')"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <div
              class="text-subtitle-1"
              v-text="$t('privacyPolicy.links.title')"
            />
            <p
              class="text-body-2 text-justify"
              v-text="$t('privacyPolicy.links.body')"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <div
              class="text-subtitle-1"
              v-text="$t('privacyPolicy.children.title')"
            />
            <p
              class="text-body-2 text-justify"
              v-text="$t('privacyPolicy.children.body')"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <div
              class="text-subtitle-1"
              v-text="$t('privacyPolicy.changes.title')"
            />
            <p
              class="text-body-2 text-justify"
              v-text="$t('privacyPolicy.changes.body')"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <div
              class="text-subtitle-1"
              v-text="$t('privacyPolicy.contact.title')"
            />
            <p
              class="text-body-2 text-justify"
              v-text="$t('privacyPolicy.contact.body',
                         {supportEmail: 'support@boulderholder.com'})"
            />
          </v-col>
        </v-row>
      </v-container>
    </template>
  </app-view>
</template>

<script>
/** @file privacy policy statement */
import AppView from '../components/AppView.vue';

export default {
  name: 'PrivacyPolicy',
  components: {AppView},
};
</script>

<style scoped>
li {
  margin-left: 20px;
}
</style>
