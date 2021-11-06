<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light my-navbar">
    <div class="container-fluid">
      <router-link class="navbar-brand" :to="{ name: 'home'}">
        স্বপ্নের ঠিকানা
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
              aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="btn btn-outline-success" href="/accounts/logout/">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavbarComponent",
};
</script>

<style>
.my-navbar {
  border-bottom: 1px solid #ddd;
}
 .navbar-brand {
   font-weight: bold;
   font-size: 150%;
 }
 .navbar-brand:hover {
   color: #dc3545 !important;
 }
</style>