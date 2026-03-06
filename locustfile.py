from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(3)
    def get_existing_link(self):
        with self.client.get("/OCki1KrOpt", catch_response=True, allow_redirects=False) as request:
            if request.status_code in [200, 302]:
                request.success()
            else:
                request.failure(f"Failed: {request.status_code}")
    
    @task(3)
    def get_non_existing_link(self):
        with self.client.get("/1234567890", catch_response=True) as request:
            if request.status_code == 404:
                request.success()
            else:
                request.failure(f"Failed: {request.status_code}")
    
    @task(3)
    def create_link(self):
        self.client.post("/shorten", json={'redirect_to': r"https://www.youtube.com/watch?v=bF1FmYhbph4&list=RDbF1FmYhbph4&start_radio=1"})
        
    