from locust import HttpUser, task

class LoadUser(HttpUser):
    @task
    def predict(self):
        self.client.post("/predict", json={"text":"book flight"})
