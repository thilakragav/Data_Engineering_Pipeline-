import pandas as pd

from pipeline.bronze_writer import save_to_bronze

df = pd.DataFrame({

    "id":[1,2,3],

    "name":["A","B","C"]

})

save_to_bronze(df,"test")