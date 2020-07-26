import pandas as pd
import random

print("carregando...\n")
data_iterator = pd.read_csv("comments(5).csv", nrows=10000000)
number = random.randint(0, 999999)
target_age = 45
result = random.sample(range(0,9), 8)
print("\r" + str(result))

print(data_iterator.query('codes == @number').head(1))







    
