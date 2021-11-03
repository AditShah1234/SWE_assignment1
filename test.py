from fastapi import FastAPI
from fastapi.testclient import TestClient
import requests
app = FastAPI()




class unittest:
    def test_read_main(self):
        response = requests.get("http://127.0.0.1:8000/")
     

        assert response.status_code == 200
    
    def test_read_co_ordinates(self):
        response = requests.get("http://127.0.0.1:8000/check_cord/231/")
      
    
    def test_api(self):
       
        response = requests.get("http://127.0.0.1:8000/co-ordinates-input?Name=das&X_axis=32&Y_axis=23")
      
        assert response.status_code == 200 
    
    def test_api_fun(self):
        
            response = requests.get("http://127.0.0.1:8000/co-ordinates-input?Name=das&X_axis=0&Y_axis=0")
            
            assert response.json()["Aleart"] == True
            response = requests.get("http://127.0.0.1:8000/co-ordinates-input?Name=das&X_axis=5&Y_axis=4")
            
            assert response.json()["Aleart"] == False

    def main(self):
        self.test_read_main()
        self.test_read_co_ordinates()
        self.test_api()
        self.test_api_fun()
if __name__ == "__main__":
    unittest = unittest()
    unittest.main()
