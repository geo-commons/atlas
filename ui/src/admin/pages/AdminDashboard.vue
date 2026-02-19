<template>
  <div class="container __admin __dashboard">
    <div>
      <div class="tw-mt-12">
        <h3>Algemeen</h3>
        <div class="buttons tw-mb-12">
          <router-link
            to="/configuration"
            class="button __tertiary __large"
            type="button"
            aria-label="Atlas configuratie"
          >
            <span class="button-icon tw-bg-orange-100">
              <CogIcon class="icon tw-text-orange-800" />
            </span>
            Atlas configuratie
          </router-link>
          <router-link
            to="/portal-configuration"
            class="button __tertiary __large"
            type="button"
            aria-label="Portaal configuratie"
          >
            <span class="button-icon tw-bg-orange-100">
              <i
                class="pi pi-home tw-text-orange-800 tw-text-5xl tw-w-6 tw-h-6 tw-flex tw-items-center tw-justify-center"
                style="font-size: 1.25rem"
              />
            </span>
            Portaal configuratie
          </router-link>
          <router-link
            to="/general-information"
            class="button __tertiary __large"
            type="button"
            aria-label="Algemene informatie"
          >
            <span class="button-icon tw-bg-orange-100">
              <InformationCircleIcon class="icon tw-text-orange-800" />
            </span>
            Algemene gegevens
          </router-link>
          <a
            href="/atlas/admin/docs/"
            target="_blank"
            rel="noopener noreferrer"
            class="button __tertiary __large"
            type="button"
            aria-label="Admin documentatie pagina"
          >
            <span class="button-icon tw-bg-orange-100">
              <BookIcon class="icon tw-text-orange-800" />
            </span>
            Admin documentatie
          </a>
        </div>
      </div>
      <div>
        <h3>Kaarten</h3>
        <div class="buttons tw-mb-12">
          <router-link to="/sources" class="button __tertiary __large" type="button" aria-label="Bronnen">
            <span class="button-icon tw-bg-amber-100">
              <SourceIcon class="icon tw-text-amber-800" />
            </span>
            Bronnen
          </router-link>
          <router-link to="/categories" class="button __tertiary __large" type="button" aria-label="Categorieën">
            <span class="button-icon tw-bg-amber-100">
              <CategoryIcon class="icon tw-text-amber-800" />
            </span>
            Categorieën
          </router-link>
          <router-link to="/metadatasets" class="button __tertiary __large" type="button" aria-label="Metadatasets">
            <span class="button-icon tw-bg-amber-100 tw-w-[40px] tw-h-[40px] tw-flex tw-items-center tw-justify-center">
              <i class="pi pi-tag tw-text-amber-800" style="font-size: 1.25rem" />
            </span>
            Metadatasets
          </router-link>
          <router-link to="/maps" class="button __tertiary __large" type="button" aria-label="Kaarten">
            <span class="button-icon tw-bg-amber-100">
              <MapIcon class="icon tw-text-amber-800" />
            </span>
            Kaarten
          </router-link>
          <router-link to="/layers" class="button __tertiary __large" type="button" aria-label="Kaartlagen">
            <span class="button-icon tw-bg-amber-100">
              <LayerIcon class="icon tw-text-amber-800" />
            </span>
            Kaartlagen
          </router-link>
          <router-link to="/themes" class="button __tertiary __large" type="button" aria-label="Thema's">
            <span class="button-icon tw-bg-amber-100">
              <BookIcon class="icon tw-text-amber-800" />
            </span>
            Thema's
          </router-link>
          <router-link to="/viewers" class="button __tertiary __large" type="button" aria-label="Viewers">
            <span class="button-icon tw-bg-amber-100">
              <ViewIcon class="icon tw-text-amber-800" />
            </span>
            Viewers
          </router-link>
        </div>
      </div>
      <div>
        <h3>Gebruikersbeheer</h3>
        <div class="buttons tw-mb-12">
          <router-link to="/users" class="button __tertiary __large" type="button" aria-label="Gebruikers">
            <span class="button-icon tw-bg-lime-100">
              <UserIcon class="icon tw-text-lime-800" />
            </span>
            Gebruikers
          </router-link>
          <router-link to="/groups" class="button __tertiary __large" type="button" aria-label="Groepen">
            <span class="button-icon tw-bg-lime-100">
              <GroupIcon class="icon tw-text-lime-800" />
            </span>
            Groepen
          </router-link>
        </div>
      </div>
      <div>
        <h3>Autorisatie</h3>
        <div class="buttons tw-mb-12">
          <router-link to="/authorizations" class="button __tertiary __large" type="button" aria-label="Autorisaties">
            <span class="button-icon tw-bg-emerald-100">
              <ShieldIcon class="icon tw-text-emerald-800" />
            </span>
            Autorisaties
          </router-link>
          <router-link to="/logs" class="button __tertiary __large" type="button" aria-label="Logs">
            <span class="button-icon tw-bg-emerald-100">
              <LogIcon class="icon tw-text-emerald-800" />
            </span>
            Logs
          </router-link>
        </div>
      </div>
      <div>
        <h3>Tabellen</h3>
        <div class="buttons tw-mb-12">
          <router-link to="/tables_old" class="button __tertiary __large" type="button" aria-label="Tabellen (old)">
            <span class="button-icon tw-bg-cyan-100">
              <TableIcon class="icon tw-text-cyan-800" />
            </span>
            Tabellen (old)
          </router-link>
          <router-link to="/tables" class="button __tertiary __large" type="button" aria-label="Tabellen">
            <span class="button-icon tw-bg-cyan-100">
              <TableIcon class="icon tw-text-cyan-800" />
            </span>
            Tabellen
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CogIcon from "@/assets/icons/cog-icon.svg";
import InformationCircleIcon from "@/assets/icons/information-circle-icon.svg";
import BookIcon from "../../assets/icons/book-icon.svg";
import CategoryIcon from "../../assets/icons/category-icon.svg";
import GroupIcon from "../../assets/icons/group-icon.svg";
import LayerIcon from "../../assets/icons/layer-icon.svg";
import MapIcon from "../../assets/icons/map-icon.svg";
import ShieldIcon from "../../assets/icons/shield-icon.svg";
import SourceIcon from "../../assets/icons/source-icon.svg";
import TableIcon from "../../assets/icons/table-icon.svg";
import LogIcon from "../../assets/icons/terminal-icon.svg";
import UserIcon from "../../assets/icons/user-icon.svg";
import ViewIcon from "../../assets/icons/view-icon.svg";

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
  gap: 14px;
  display: grid;
  grid-template-columns: repeat(3, minmax(240px, 1fr));
  row-gap: 14px;
  column-gap: 14px;
}

@media (min-width: 1200px) {
  .buttons {
    grid-template-columns: repeat(4, minmax(240px, 1fr));
  }
}

@media (max-width: 862px) {
  .buttons {
    grid-template-columns: repeat(2, minmax(240px, 1fr));
  }
}

@media (max-width: 620px) {
  .buttons {
    grid-template-columns: repeat(1, minmax(240px, 1fr));
  }
}

.container.__dashboard .button {
  justify-content: flex-start;
  padding: 14px;
  height: auto;
  gap: 14px;
}

.container.__dashboard .button-icon {
  border-radius: 100%;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
