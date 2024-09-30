<template>
  <div class="container __admin">
    <h1>Atlas beheerpagina</h1>
    <div>
      <div>
        <h3>Algemene instellingen</h3>
        <div class="buttons">
          <router-link
            to="/configuration"
            class="button __tertiary __large"
            type="button"
            aria-label="Naar configuratie"
          >
            <CogIcon class="icon" />
            Configuratie
          </router-link>
          <router-link
            to="/general-information"
            class="button __tertiary __large"
            type="button"
            aria-label="Naar algemene informatie"
          >
            <InformationCircleIcon class="icon __medium" />
            Algemene gegevens
          </router-link>
        </div>
      </div>
      <div>
        <h3>Kaarten</h3>
        <div class="buttons">
          <router-link to="/sources" class="button __tertiary __large" type="button" aria-label="Naar bronnen">
            <SourceIcon class="icon" />
            Bronnen
          </router-link>
          <router-link to="/categories" class="button __tertiary __large" type="button" aria-label="Naar categorieën">
            <CategoryIcon class="icon" />
            Categorieën
          </router-link>
          <router-link to="/datasets" class="button __tertiary __large" type="button" aria-label="Naar datasets">
            <DatabaseIcon class="icon" />
            Datasets
          </router-link>
          <router-link to="/maps" class="button __tertiary __large" type="button" aria-label="Naar kaarten">
            <MapIcon class="icon" />
            Kaarten
          </router-link>
          <router-link to="/layers" class="button __tertiary __large" type="button" aria-label="Naar kaartlagen">
            <LayerIcon class="icon" />
            Kaartlagen
          </router-link>
          <router-link to="/themes" class="button __tertiary __large" type="button" aria-label="Naar thema's">
            <BookIcon class="icon" />
            Thema's
          </router-link>
          <router-link to="/viewers" class="button __tertiary __large" type="button" aria-label="Naar viewers">
            <ViewIcon class="icon" />
            Viewers
          </router-link>
        </div>
      </div>
      <div>
        <h3>Gebruikersbeheer</h3>
        <div class="buttons">
          <router-link to="/users" class="button __tertiary __large" type="button" aria-label="Naar gebruikers">
            <UserIcon class="icon" />
            Gebruikers
          </router-link>
          <router-link to="/groups" class="button __tertiary __large" type="button" aria-label="Naar groepen">
            <GroupIcon class="icon" />
            Groepen
          </router-link>
        </div>
      </div>
      <div>
        <h3>Autorisatie</h3>
        <div class="buttons">
          <router-link
            to="/authorizations"
            class="button __tertiary __large"
            type="button"
            aria-label="Naar autorisaties"
          >
            <ShieldIcon class="icon" />
            Autorisaties
          </router-link>
          <router-link to="/logs" class="button __tertiary __large" type="button" aria-label="Naar logs">
            <LogIcon class="icon" />
            Logs
          </router-link>
        </div>
      </div>
      <div>
        <h3>Tabellen</h3>
        <div class="buttons">
          <router-link to="/tables" class="button __tertiary __large" type="button" aria-label="Naar tabellen">
            <TableIcon class="icon" />
            Tabellen
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MapIcon from "../../assets/icons/map-icon.svg";
import SourceIcon from "../../assets/icons/source-icon.svg";
import LayerIcon from "../../assets/icons/layer-icon.svg";
import CategoryIcon from "../../assets/icons/category-icon.svg";
import UserIcon from "../../assets/icons/user-icon.svg";
import GroupIcon from "../../assets/icons/group-icon.svg";
import ViewIcon from "../../assets/icons/view-icon.svg";
import TableIcon from "../../assets/icons/table-icon.svg";
import BookIcon from "../../assets/icons/book-icon.svg";
import DatabaseIcon from "../../assets/icons/database-icon.svg";
import CogIcon from "@/assets/icons/cog-icon.svg";
import LogIcon from "../../assets/icons/terminal-icon.svg";
import ShieldIcon from "../../assets/icons/shield-icon.svg";
import InformationCircleIcon from "@/assets/icons/information-circle-icon.svg";

export default {
  name: "AdminDashboard",
  components: {
    InformationCircleIcon,
    CogIcon,
    MapIcon,
    SourceIcon,
    LayerIcon,
    CategoryIcon,
    UserIcon,
    GroupIcon,
    BookIcon,
    DatabaseIcon,
    ViewIcon,
    TableIcon,
    LogIcon,
    ShieldIcon,
  },
};
</script>

<style scoped>
h1 {
  font-size: var(--font-size-3xl);
}

h3 {
  font-size: var(--font-size-xl);
}

.buttons {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  row-gap: 14px;
  column-gap: 14px;
}

@media (max-width: 576px) {
  .buttons {
    grid-template-columns: 1fr;
  }
}
</style>
