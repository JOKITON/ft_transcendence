<template>
	<NavHome></NavHome>

  <!-- ---------------------------------------------------------------- -->
  <div class="container">
    <div class="main-body">
    

          <!-- /Breadcrumb -->
    
          <div class="row gutters-sm">
            <div class="col-md-4 mb-3">
              <div class="card">
                <div class="card-body">
                  <div class="d-flex flex-column align-items-center text-center">
                    <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="Admin" class="rounded-circle" width="150">
                    <div class="mt-3">
                      <h4>John Doe</h4>
                      <p class="text-secondary mb-1">Full Stack Developer</p>
                      <p class="text-muted font-size-sm">Bay Area, San Francisco, CA</p>
                      <button class="btn btn-primary">Follow</button>
                      <button class="btn btn-outline-primary">Message</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="col-md-8">
              <div class="card mb-3">
                <div class="card-body">
                  <div class="row">
                    <div class="col-sm-3">
                      <h6 class="mb-0">Full Name</h6>
                    </div>
                    <div class="col-sm-9 text-secondary">
                      Kenneth Valdez
                    </div>
                  </div>
                  <hr>
                  <div class="row">
                    <div class="col-sm-3">
                      <h6 class="mb-0">Email</h6>
                    </div>
                    <div class="col-sm-9 text-secondary">
                      fip@jukmuh.al
                    </div>
                  </div>
                  <hr>
                  <div class="row">
                    <div class="col-sm-3">
                      <h6 class="mb-0">Phone</h6>
                    </div>
                    <div class="col-sm-9 text-secondary">
                      (239) 816-9029
                    </div>
                  </div>
                  <hr>
                  <div class="row">
                    <div class="col-sm-3">
                      <h6 class="mb-0">Mobile</h6>
                    </div>
                    <div class="col-sm-9 text-secondary">
                      (320) 380-4539
                    </div>
                  </div>
                  <hr>
                  <div class="row">
                    <div class="col-sm-3">
                      <h6 class="mb-0">Address</h6>
                    </div>
                    <div class="col-sm-9 text-secondary">
                      Bay Area, San Francisco, CA
                    </div>
                  </div>
                  <hr>
                  <div class="row">
                    <div class="col-sm-12">
                      <a class="btn btn-info " target="__blank" href="https://www.bootdey.com/snippets/view/profile-edit-data-and-skills">Edit</a>
                    </div>
                  </div>
                </div>
              </div>

              <div class="row gutters-sm">
                <div class="col-sm-6 mb-3">
                  <div class="card h-100">
                    <div class="card-body">
                      <h6 class="d-flex align-items-center mb-3">Friends List</h6>
                      
						<ul class="list-group">
							<li class="list-group-item d-flex justify-content-between align-items-center">
							<span>
								<span class="status-indicator bg-success"></span>
								Jane Smith
							</span>
							<span class="badge bg-success">Online</span>
							</li>
							<li class="list-group-item d-flex justify-content-between align-items-center">
							<span>
								<span class="status-indicator bg-danger"></span>
								Mike Johnson
							</span>
							<span class="badge bg-danger">Offline</span>
							</li>
							<li class="list-group-item d-flex justify-content-between align-items-center">
							<span>
								<span class="status-indicator bg-success"></span>
								Emily Davis
							</span>
							<span class="badge bg-success">Online</span>
							</li>
							<li class="list-group-item d-flex justify-content-between align-items-center">
							<span>
								<span class="status-indicator bg-danger"></span>
								David Brown
							</span>
							<span class="badge bg-danger">Offline</span>
							</li>
						</ul>

                    </div>
                  </div>
                </div>
                <div class="col-sm-6 mb-3">
                  <div class="card h-100">
                    <div class="card-body card-body2">
                      <h6 class="d-flex align-items-center mb-3">Player Stats</h6>
                      <div class="d-flex flex-column">
							<div class="d-flex justify-content-between mb-3">
							<span>Victories:</span>
							<span>123</span>
							</div>
							<div class="d-flex justify-content-between mb-3">
							<span>Losses:</span>
							<span>45</span>
							</div>
							<div class="d-flex justify-content-between mb-3">
							<span>Games Played:</span>
							<span>168</span>
							</div>
							<div class="d-flex justify-content-between mb-3">
							<span>Total Points:</span>
							<span>9876</span>
							</div>
					  </div>
                    </div>
                  </div>
                </div>
              </div>



            </div>
          </div>

        </div>
    </div>
	  <!-- ---------------------------------------------------------------- -->

</template>

<script setup lang="ts">
import NavHome from './NavHome.vue'
// Este script está vacío ya que no se necesita funcionalidad para este ejemplo estático
</script>

<style scoped>
body{
    margin-top:20px;
    color: #1a202c;
    text-align: left;
    background-color: #e2e8f0;    
}
.main-body {
    padding: 15px;
}
.card {
    box-shadow: 0 1px 3px 0 rgba(0,0,0,.1), 0 1px 2px 0 rgba(0,0,0,.06);
}

.card {
    position: relative;
    display: flex;
    flex-direction: column;
    min-width: 0;
    word-wrap: break-word;
    background-color: #fff;
    background-clip: border-box;
    border: 0 solid rgba(0,0,0,.125);
    border-radius: .25rem;
}

.card-h {
	height: 40em;
}

.card-body {
    flex: 1 1 auto;
    min-height: 1px;
    padding: 1rem;
}

.gutters-sm {
    margin-right: -8px;
    margin-left: -8px;
}

.gutters-sm>.col, .gutters-sm>[class*=col-] {
    padding-right: 8px;
    padding-left: 8px;
}
.mb-3, .my-3 {
    margin-bottom: 1rem!important;
}

.bg-gray-300 {
    background-color: #e2e8f0;
}
.h-100 {
    height: 100%!important;
}
.shadow-none {
    box-shadow: none!important;
}




.friends-section {
  background-color: #fff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.friends-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.friend-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #ddd;
}

.friend-item:last-child {
  border-bottom: none;
}

.status-indicator {
  display: inline-block;
  width: 10px;
  height: 10px;
  margin-right: 10px;
  border-radius: 50%;
}

.online {
  background-color: green;
}

.offline {
  background-color: red;
}

.card-body2 {
  padding: 20px;
}

.d-flex {
  display: flex;
}

.justify-content-between {
  justify-content: space-between;
}



</style>
