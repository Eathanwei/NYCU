import pandas as pd
import os

combined_df = pd.read_csv('combined_output.csv')

vegan_lacto_ovo = combined_df[(combined_df['is_vegan'] == True)&(combined_df['is_lacto_ovo'] == True)]
vegan_non_lacto_ovo = combined_df[(combined_df['is_vegan'] == True)&(combined_df['is_lacto_ovo'] == False)]
non_vegan_lacto_ovo = combined_df[(combined_df['is_vegan'] == False)&(combined_df['is_lacto_ovo'] == True)]
non_vegan_non_lacto_ovo = combined_df[(combined_df['is_vegan'] == False)&(combined_df['is_lacto_ovo'] == False)]

# 打印每一類的數量
print("Vegan and Lacto-Ovo:", len(vegan_lacto_ovo))
print("Vegan and Non-Lacto-Ovo:", len(vegan_non_lacto_ovo))
print("Non-Vegan and Lacto-Ovo:", len(non_vegan_lacto_ovo))
print("Non-Vegan and Non-Lacto-Ovo:", len(non_vegan_non_lacto_ovo))

# 可選：將每一類保存為單獨的 CSV 文件
vegan_lacto_ovo.to_csv('vegan_lacto_ovo.csv', index=False)
vegan_non_lacto_ovo.to_csv('vegan_non_lacto_ovo.csv', index=False)
non_vegan_lacto_ovo.to_csv('non_vegan_lacto_ovo.csv', index=False)
non_vegan_non_lacto_ovo.to_csv('non_vegan_non_lacto_ovo.csv', index=False)